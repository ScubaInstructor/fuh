import threading  # Importiere das threading-Modul für die Verwendung von Threads
from cicflowmeter import sniffer  # Importiere den Sniffer von cicflowmeter
from cicflowmeter.flow import Flow
from queue import Queue  # Importiere die Queue-Klasse für Thread-sichere Warteschlangen
from scapy.sendrecv import AsyncSniffer  # Importiere den asynchronen Sniffer von Scapy
from dotenv import load_dotenv
import os
from joblib import load
from cicflowmeter.utilities import erstelle_datei, sende_BytesIO_datei_per_scp
from uuid import uuid4
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, line_buffering=True) # TODO entfernen
from sklearn.ensemble import RandomForestClassifier
from adapt import adapt_for_prediction
from pandas import DataFrame

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

INDOCKER = True # Nur für debugging

# Auslesen der INTERFACE-Variable
INTERFACE = os.getenv('INTERFACE')
REMOTE_HOST=os.getenv('REMOTE_HOST')
REMOTE_USER=os.getenv('REMOTE_USER')
REMOTE_PATH=os.getenv('REMOTE_PATH')
MYSSH_FILE=os.getenv('MYSSH_KEY')
if INDOCKER:
    LOCALPREFIX = "/app/"
else: 
    LOCALPREFIX = "/home/georg/Desktop/FaPra/python/fuh/sensor/"
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
        #self.queue.put({0: "this is the beginning"})  # Füge eine Startnachricht zur Warteschlange hinzu TODO entfernen
        self.start_receiver_worker()  # Starte den Worker für den Empfang von Daten
        
        self.snif.start()  # Starte den Sniffer
        try:
            self.snif.join()  # Warte, bis der Sniffer stoppt (blockierend)
        except KeyboardInterrupt:
            print("Exiting")  # Ausgabe bei Tastaturunterbrechung
            self.snif.stop()  # Stoppe den Sniffer
        finally:
            self.snif.join()  # Stelle sicher, dass der Sniffer vollständig gestoppt wird
    
    def output_function(self, data: Flow):
        '''Diese Funktion wird aufgerufen, wenn ein Paket empfangen wird'''
        self.queue.put(data)  # Füge die empfangenen Daten zur Warteschlange hinzu
        self.queue.join()  # Warte, bis alle Aufgaben in der Warteschlange bearbeitet sind

    def get_intern_sniffer(self) -> AsyncSniffer:
        '''Erstelle den internen Sniffer'''
        s: AsyncSniffer = sniffer.create_sniffer(input_file=None, input_interface=INTERFACE, output_mode="intern", output=self.output_function)
        # s.count = 10  # Für Testzwecke (kann verwendet werden, um die Anzahl der Pakete zu begrenzen)
        return s

    def start_receiver_worker(self):
        '''Starte den Worker in einem separaten Thread'''
        threading.Thread(target=self.worker, daemon=True).start()  # Starte einen neuen Thread für den Worker
    
    def worker(self):
        '''Die Arbeit, die in einem separaten Thread erledigt wird'''
        while True:
            item = self.queue.get()  # Hole ein Element aus der Warteschlange
            print(f'Working on {item}')  # Ausgabe zur Anzeige, dass an dem Element gearbeitet wird
            # Prognose erstellen
            flow = DataFrame([item[1]])
            flow = adapt_for_prediction(data=flow,scaler=self.scaler,ipca=self.ipca,ipca_size=IPCASIZE)
            prediction = self.model.predict(flow)
            #if prediction:
            if True: # TODO nur für debugging
                print("prediction true")
                # Verarbeite zu Datei
                id = str(uuid4())
                flow_bytesIO = erstelle_datei(item[0])  # das BytesIO Objekt das eine .pcap Datei ist
                remote_file_path = REMOTE_PATH + id + ".pcap"    # Einzigartiger Dateiname evtl ist Datum besser?
                print(remote_file_path)
                sende_BytesIO_datei_per_scp(pcap_buffer=flow_bytesIO,ziel_host=REMOTE_HOST,
                                            ziel_pfad=remote_file_path,username=REMOTE_USER,mySSHK=MYSSH_FILE)
                print(f'Finished {item} mit UUID:{id}')  # Ausgabe zur Anzeige, dass die Arbeit an dem Element abgeschlossen ist
            else:
                print(f'Finished {item}')  # Ausgabe zur Anzeige, dass die Arbeit an dem Element abgeschlossen ist
            self.queue.task_done()  # Markiere das Element als bearbeitet

if __name__ == "__main__":
    threading.stack_size(4096*4096) # TODO checke ob das nötig ist
    s = My_Sniffer()  # Erstelle eine Instanz des My_Sniffer
    s.start()  # Starte den Sniffer und beginne mit dem Überwachen der Pakete
