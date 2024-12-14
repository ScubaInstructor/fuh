import threading
import base64
from cicflowmeter import sniffer  
from cicflowmeter.flow import Flow
from queue import Queue  
from scapy.sendrecv import AsyncSniffer  
from dotenv import load_dotenv
import os
from joblib import load
from cicflowmeter.utilities import create_BytesIO_pcap_file, flow_to_json
from uuid import uuid4
from sklearn.ensemble import RandomForestClassifier
from pipelining_utilities import adapt_for_prediction
from pandas import DataFrame
from time import sleep
from elasticsearch import Elasticsearch
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
ES_HOST = os.getenv('ES_HOST')  # Change this to your Elasticsearch host
ES_PORT = int(os.getenv('ES_PORT'))        # Change this to your Elasticsearch port
ES_INDEX = os.getenv('ES_INDEX')  # Index name for storing flow data
# Get these values from your Elasticsearch installation
ES_USERNAME = os.getenv('ES_USERNAME')  # Replace with your elastic user password
ES_PASSWORD = os.getenv('ES_PASSWORD')  # Default superuser

if INDOCKER:
    LOCALPREFIX = "/app/"
else: 
    LOCALPREFIX = os.getenv('LOCALPREFIX')

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
        self.ipca = load(IPCAPATH) if IPCAPATH else IPCAPATH
        self.scaler = load(SCALERPATH)
    
    def start(self):
        '''start sniffer and worker-thread'''
        self.start_receiver_worker()  # Starte den Worker für den Empfang von Daten
        if DEBUGGING:
            print("Starting sniffer")
        self.snif.start()  # Starte den Sniffer
        
        try:
            while True:
                sleep(1)  # to reduce cpu load # TODO check if necessary
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

    def start_receiver_worker(self):
        '''starting the worker thread'''
        threading.Thread(target=self.worker, daemon=True).start()  # Start a new thread for worker
    
    def worker(self):
        '''the function which will be called to do the work on the flow'''
        # Initialize Elasticsearch client
        es = Elasticsearch(
            f"{ES_HOST}:{ES_PORT}",
            basic_auth=(ES_USERNAME, ES_PASSWORD),  # Add authentication
            verify_certs=False,
            ssl_show_warn=False,
            request_timeout=30,
            retry_on_timeout=True
        )
        
        # Create index if it doesn't exist
        if not es.indices.exists(index=ES_INDEX):
            es.indices.create(index=ES_INDEX, ignore=400)
            print(f"Created new index: {ES_INDEX}")
            
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

            if DEBUGGING:
                print(f"Prediction ist: {prediction}")
            if prediction != ['BENIGN'] or DEBUGGING:
                if DEBUGGING:
                    print("prediction true")
                # getting the attack data to the server TODO hier muss die richtige Methode noch rein.
                id = str(uuid4())
                # Create a PCAP file
                # flow_bytesIO = create_BytesIO_pcap_file(item)  # the pcap file as BytesIO object  DEPRECATED
                # Encode PCAP file to base64 since elasticsearch does not support binary data DEPRECATED
                # pcap_base64 = base64.b64encode(flow_bytesIO.getvalue()).decode('utf-8')
                # Encode Flow item  to Json for transfer to kibana
                pcap_json = flow_to_json(item)
                
                try:
                # Prepare document for Elasticsearch
                    doc = {
                        'id': id,
                        'timestamp': datetime.now().isoformat(),
                        'flow_data': item.get_data(),
                        'prediction': prediction.tolist()[0],
                        'source_ip': item.src_ip,
                        'pcap_data': pcap_json,  # Add the PCAP data as Json
                        'pcap_metadata': {
                            'packet_count': len(item.packets)
                        }                        
                    }                    
                    # Send to Elasticsearch
                    es.index(index=ES_INDEX, body=doc)
                    print(f"Data sent to Elasticsearch successfully")
                except Exception as e:
                    print(f"Error sending data to Elasticsearch: {e}")

                if DEBUGGING:
                    print(f'Finished {item} mit UUID:{id}')  
            else:
                if DEBUGGING:
                    print(f'Finished {item}')  
            self.queue.task_done()  # to mark the item done 


if __name__ == "__main__":
    s = My_Sniffer() 
    s.start()  
