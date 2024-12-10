import threading

from cicflowmeter import sniffer  # Importiere den Sniffer von cicflowmeter
from cicflowmeter.flow import Flow
from queue import Queue  # Importiere die Queue-Klasse für Thread-sichere Warteschlangen
from scapy.sendrecv import AsyncSniffer  # Importiere den asynchronen Sniffer von Scapy
from dotenv import load_dotenv
import os
from joblib import load
from cicflowmeter.utilities import erstelle_datei, sende_BytesIO_datei_per_scp, erstelle_post_request
from uuid import uuid4
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, line_buffering=True) # TODO entfernen
from sklearn.ensemble import RandomForestClassifier
from adapt import adapt_for_prediction
from pandas import DataFrame
from time import sleep

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

# For Debug Purpose
INDOCKER = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)
DEBUGGING =  os.environ.get('DEBUGGING', False)
# Auslesen der Environment-Variable
SNIFFING_INTERFACE = os.getenv('SNIFFING_INTERFACE')
REMOTE_HOST=os.getenv('REMOTE_HOST')
REMOTE_USER=os.getenv('REMOTE_USER')
REMOTE_PATH=os.getenv('REMOTE_PATH')
MYSSH_FILE=os.getenv('MYSSH_KEY')
OUTPUT_URL=os.getenv('OUTPUT_URL')
if INDOCKER:
    LOCALPREFIX = "/app/"
else: 
    LOCALPREFIX = os.getenv('LOCALPREFIX')
MYSSH_FILE = LOCALPREFIX + MYSSH_FILE
MODELPATH = LOCALPREFIX + "model.pkl" 
SCALERPATH = LOCALPREFIX + "scaler.pkl"
IPCAPATH = LOCALPREFIX + "ipca_mit_size_34.pkl"
IPCASIZE = 34

class My_Sniffer():
    def __init__(self) -> None:
        '''Initialisiere den Sniffer und die Warteschlange'''
        self.snif: AsyncSniffer = self.get_intern_sniffer()  # Erstelle eine Instanz des Sniffers
        self.queue = Queue()  # Erstelle eine Thread-sichere Warteschlange
        self.model: RandomForestClassifier = load(MODELPATH)
        self.ipca = load(IPCAPATH) if IPCAPATH else IPCAPATH
        self.scaler = load(SCALERPATH)
    
    def start(self):
        '''Starte den Sniffer und den Empfangs-Worker'''
        self.start_receiver_worker()  # Starte den Worker für den Empfang von Daten
        if DEBUGGING:
            print("Starting sniffer")
        self.snif.start()  # Starte den Sniffer
        
        try:
            while True:
                sleep(1)  # Kurze Pause, um CPU-Auslastung zu reduzieren
        except KeyboardInterrupt:
            print("Exiting")  # Ausgabe bei Tastaturunterbrechung
        finally:
            print("Stopping sniffer")
            self.snif.stop()  # Stoppe den Sniffer
            self.snif.join()  # Warte, bis der Sniffer vollständig gestoppt ist
    
    def output_function(self, data: Flow):
        if DEBUGGING:
            print("out_func")
        '''Diese Funktion wird aufgerufen, wenn ein Flow empfangen wird'''
        self.queue.put(data)  # Füge die empfangenen Daten zur Warteschlange hinzu
        # self.queue.join()  # Warte, bis alle Aufgaben in der Warteschlange bearbeitet sind

    def get_intern_sniffer(self) -> AsyncSniffer:
        '''Erstelle den internen Sniffer'''
        if DEBUGGING:
            print(f"Creating sniffer on interface: {SNIFFING_INTERFACE}")
        s: AsyncSniffer = sniffer.create_sniffer(input_file=None, input_interface=SNIFFING_INTERFACE, output_mode="intern", output=self.output_function)
        # s.count = 10  # Für Testzwecke (kann verwendet werden, um die Anzahl der Pakete zu begrenzen)
        return s

    def start_receiver_worker(self):
        '''Starte den Worker in einem separaten Thread'''
        threading.Thread(target=self.worker, daemon=True).start()  # Starte einen neuen Thread für den Worker
    
    def worker(self):
        '''Die Arbeit, die in einem separaten Thread erledigt wird'''
        while True:
            if DEBUGGING:
                print("hello from worker!")
            item = self.queue.get()  # Hole ein Element aus der Warteschlange
            # item ist der Flow, inclusive aller Packete!
            if DEBUGGING:
                print(f'Working on {item}')  # Ausgabe zur Anzeige, dass an dem Element gearbeitet wird
            # Prognose auf Metadaten erstellen
            flow_data = DataFrame([item.get_data()])
            flow_data = adapt_for_prediction(data=flow_data,scaler=self.scaler,ipca=self.ipca,ipca_size=IPCASIZE)
            prediction = self.model.predict(flow_data)
            if DEBUGGING:
                print(f"Prediction ist: {prediction}")
            if prediction != ['BENIGN'] or DEBUGGING:
                if DEBUGGING:
                    print("prediction true")
                # Verarbeite zu Datei TODO hier muss die richtige Methode noch rein.
                id = str(uuid4())
                # flow_bytesIO = erstelle_datei(item[0])  # das BytesIO Objekt das eine .pcap Datei ist
                # remote_file_path = REMOTE_PATH + id + ".pcap"    # Einzigartiger Dateiname evtl ist Datum besser?
                # sende_BytesIO_datei_per_scp(pcap_buffer=flow_bytesIO,ziel_host=REMOTE_HOST,
                #                            ziel_pfad=remote_file_path,username=REMOTE_USER,mySSHK=MYSSH_FILE)
                erstelle_post_request(flow=item,output_url=OUTPUT_URL)
                if DEBUGGING:
                    print(f'Finished {item} mit UUID:{id}')  # Ausgabe zur Anzeige, dass die Arbeit an dem Element abgeschlossen ist
            else:
                if DEBUGGING:
                    print(f'Finished {item}')  # Ausgabe zur Anzeige, dass die Arbeit an dem Element abgeschlossen ist
            self.queue.task_done()  # Markiere das Element als bearbeitet


if __name__ == "__main__":
    # threading.stack_size(4096*4096) # TODO checke ob das nötig ist
    s = My_Sniffer()  # Erstelle eine Instanz des My_Sniffer
    s.start()  # Starte den Sniffer und beginne mit dem Überwachen der Pakete
