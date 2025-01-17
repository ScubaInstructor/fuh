import asyncio
import hashlib
import base64

from  threading import Thread
from requests import Response
from cicflowmeter import sniffer  
from httpWriter import HttpWriter
from cicflowmeter.flow import Flow
from queue import Queue  
from scapy.sendrecv import AsyncSniffer  
from scapy import interfaces
from scapy.all import get_if_addr
from dotenv import load_dotenv
import os
from joblib import load
from cicflowmeter.utilities import create_BytesIO_pcap_file, flow_to_json
from uuid import uuid4
from sklearn.ensemble import RandomForestClassifier
from pipelining_utilities import adapt_for_prediction
from pandas import DataFrame
from time import sleep
from elasticsearch import AuthenticationException, Elasticsearch
import json
from datetime import datetime

# Loading of the .env file
load_dotenv()

# For Debug Purpose
INDOCKER = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)
DEBUGGING = os.environ.get('DEBUGGING') == '1'
# Reading of the environmentvariables
SNIFFING_INTERFACE = os.getenv('SNIFFING_INTERFACE')
# Elastic
# ES_HOST = os.getenv('ES_HOST')  # Change this to your Elasticsearch host
# ES_PORT = int(os.getenv('ES_PORT'))        # Change this to your Elasticsearch port
# ES_INDEX = os.getenv('ES_INDEX')  # Index name for storing flow data
#Flask Server
SERVER_URL = os.getenv('SERVER_URL')
SERVER_TOKEN = os.getenv('SERVER_TOKEN')
# Get these values from your Elasticsearch installation
ES_API_KEY = os.getenv('ES_API_KEY')  # API key for access to elastic 
SENSOR_NAME = os.getenv('SENSOR_NAME')  # Unique name to identify this sensor


if INDOCKER:
    LOCALPREFIX = "/app/"
else: 
    LOCALPREFIX = os.getenv('LOCALPREFIX')
    LOCALPREFIX = "./fuh/sensor/" if LOCALPREFIX == None else LOCALPREFIX

# Load the 
MODELPATH = LOCALPREFIX + "model.pkl" 
SCALERPATH = LOCALPREFIX + "scaler.pkl"
IPCAPATH = LOCALPREFIX + "ipca_mit_size_34.pkl"
IPCASIZE = 34

class My_Sniffer():
    def __init__(self) -> None:
        '''Initialise the sniffer and create the threadsafe queue for the FLoe-items'''
        self.snif: AsyncSniffer = self.get_intern_sniffer()  # create an Instance of the sniffer 
        self.queue = Queue() 
        self.model: RandomForestClassifier = load(MODELPATH)
        self.model_hash = self.compute_file_hash(MODELPATH)
        self.ipca = load(IPCAPATH) if IPCAPATH else IPCAPATH
        self.scaler = load(SCALERPATH)
    
    def start(self):
        '''start sniffer and worker-thread'''
        worker_thread = self.start_receiver_worker()  # Start worker to deal with items in the queue
        if DEBUGGING:
            print("Starting sniffer")
        self.snif.start()  # Start the sniffer
        
        try:
            while True:
                sleep(1)  # to reduce cpu load # TODO check if necessary
                if worker_thread.is_alive():
                    pass
                else:   # the worker has stopped hopefully because of necessary model update
                    self.download_new_model()
                    sleep(5)
                    worker_thread = self.start_receiver_worker()
        except KeyboardInterrupt:
            print("Exiting")  
        finally:
            print("Stopping sniffer")
            self.snif.stop()  
            self.snif.join()  # wait to fully finish the sniffer
    
    def output_function(self, data: Flow):
        if DEBUGGING:
            print("out_func reached")
        '''this function will be called when a flow is completed and ready for further use'''
        self.queue.put(data)  # Füge die empfangenen Daten zur Warteschlange hinzu
        # self.queue.join()  # Warte, bis alle Aufgaben in der Warteschlange bearbeitet sind

    def get_intern_sniffer(self) -> AsyncSniffer:
        '''create intern sniffer'''
        if DEBUGGING:
            print(f"Creating sniffer on interface: {SNIFFING_INTERFACE}")
        s: AsyncSniffer = sniffer.create_sniffer(input_file=None, input_interface=SNIFFING_INTERFACE, output_mode="intern", output=self.output_function)
        # s.count = 10  # Für Testzwecke (kann verwendet werden, um die Anzahl der Pakete zu begrenzen)
        return s

    def start_receiver_worker(self) -> Thread:
        '''starting the worker thread'''
        threadname = "worker_thread"
        trd = Thread(target=self.worker, daemon=True, name=threadname)
        trd.start()  # Start a new thread for worker
        return trd

    def worker(self):
        '''
        the function which will be called to do the work on the flow
        Returns 
        '''
            
        while True:
            if DEBUGGING:
                print("hello from worker!")
            item: Flow = self.queue.get()  # Get a Flow item from the queue
            # item from type Flow. It contains all the packages it comprises.
            if DEBUGGING:
                print(f'Working on {item}')  
            # creating a prognosis on the Metadata
            flow_data: dict = DataFrame([item.get_data()])
            flow_data: DataFrame = adapt_for_prediction(data=flow_data,scaler=self.scaler,ipca=self.ipca,ipca_size=IPCASIZE)
            prediction = self.model.predict(flow_data) # returns a numpy ndarray
            proba = self.model.predict_proba(flow_data)

            if DEBUGGING:
                print(f"Prediction is: {prediction} with certainty of {proba.max()}")
            if prediction != ['BENIGN'] or proba.max() < 0.8 or proba.max() - proba.mean() < 0.6 or DEBUGGING:
                if DEBUGGING:
                    print("Flow will be sent")
                # getting the attack data to the server 
                flow_id = str(uuid4())
                # Create a PCAP file
                flow_bytesIO = create_BytesIO_pcap_file(item)  # the pcap file as BytesIO object  DEPRECATED

                # Encode PCAP file to base64 since elasticsearch does not support binary data DEPRECATED
                pcap_base64 = base64.b64encode(flow_bytesIO.getvalue()).decode('utf-8')

                # Encode Flow item  to Json for transfer to kibana
                # pcap_json = flow_to_json(item)
                
                # prepare the dict with the probabilities
                probabilities = {}
                for i in range(len(proba[0])):
                    probabilities[self.model.classes_[i]] = proba[0][i]
                
                # get ip and port numbers of flow
                my_ip = get_if_addr(interfaces.conf.iface)
                print(f"my_ip: {my_ip} {type(my_ip)}, dest_ip: {item.dest_ip} {type(item.dest_ip)}")
                if item.dest_ip == my_ip:
                    partner_ip = item.src_ip
                    sensor_port = item.dest_port
                    partner_port = item.src_port
                else: 
                    partner_ip = item.dest_ip
                    sensor_port = item.src_port
                    partner_port = item.dest_port
                try:
                # Prepare document for Elasticsearch
                    doc = {
                        
                        'flow_id': flow_id,
                        'sensor_name': SENSOR_NAME, # unique Sensorname
                        'sensor_port': sensor_port,
                        'partner_ip': partner_ip, # Ip of the other endpoint of the flow
                        'partner_port': partner_port,

                        'timestamp': datetime.now().isoformat(),
                        'prediction': prediction.tolist()[0],
                        'probabilities': probabilities,
                        'attack_class': "not yet classified",

                        'has_been_seen': False, # TODO Is this redundant, if we have the attack_class field?
                        'flow_data': item.get_data(),
                        'pcap_data': pcap_base64,  # Add the PCAP data as Base 64 encoded String

                        'model_hash' : self.model_hash

                    }   
                    if DEBUGGING:
                        print(f"Document to be sent: {doc}")                 
                    # send to flask
                    resp = json.loads(self.upload_to_flask_server(data=doc).text)
                    if "error" in resp:
                        if resp["error"] == "Invalid token":
                            if DEBUGGING:
                                print("Token is not valid")
                        elif resp["error"] == "Malformed data":
                            if DEBUGGING:
                                print("Data is not formed corretly!")
                    elif "update_error" in resp:
                        if DEBUGGING:
                            print("Update of model is needed \nshutting down the Worker thread!")
                        # start the model update and write new model.pkl file in the main thread and recreate a worker thread
                        return
                    else:
                        if DEBUGGING:
                            print("sent data to flask server")
                except AuthenticationException as ae:
                    print(f"Authentication error: {ae}")
                except Exception as e:
                    print(f"Error sending data to Server: {e}")
                if DEBUGGING:
                    print(f'Finished {item} mit UUID:{flow_id}')  
            else:
                if DEBUGGING:
                    print(f'Finished {item}')  
            self.queue.task_done()  # to mark the item done 

    def compute_file_hash(self, file_path: str) -> str:
        """Compute the hash of a file using the sha265 algorithm.
        
        Args:
            - file_path (str) = the path to the file
        
        Returns:
            str: The hash value
        """
        hash_func = hashlib.sha256()
        with open(file_path, 'rb') as file:
            # Read the file in chunks of 8192 bytes
            while chunk := file.read(8192):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()

    def upload_to_flask_server(self, data: dict) -> Response:
        """
        Upload the dict to the Flask server
        Args:    data (dict): this contains all the data to be sent to Flask
        Returns: 
        """
        async def _upload_to_flask_server(self, data:dict) -> Response:
            hw = HttpWriter(f"{SERVER_URL}/upload") 
            return hw.write(data=data, token=SERVER_TOKEN)
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError as e:
            if str(e).startswith('There is no current event loop in thread'):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            else:
                raise
        
        return loop.run_until_complete(_upload_to_flask_server(self, data=data))
        
    def download_new_model(self):
        """
            Download the new model and save it to model.pkl, replacing the old model.
        """
        async def _download_new_model(self):
            hw = HttpWriter(f"{SERVER_URL}/get_latest_model")
            return hw.download_file(token=SERVER_TOKEN)
        
        response =  asyncio.run(_download_new_model(self=self))
        with open("model.pkl", "wb") as f:
            f.write(response.content)

if __name__ == "__main__":
    s = My_Sniffer() 
    s.start()  
