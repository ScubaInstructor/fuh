from cicflowmeter import sniffer  # Importiere den Sniffer von cicflowmeter
from queue import Queue  # Importiere die Queue-Klasse für Thread-sichere Warteschlangen
from scapy.sendrecv import AsyncSniffer  # Importiere den asynchronen Sniffer von Scapy
import threading  # Importiere das threading-Modul für die Verwendung von Threads

INTERFACE = "enp12s0"  # Definiere das Netzwerk-Interface, das überwacht werden soll

class My_Sniffer():
    def __init__(self) -> None:
        '''Initialisiere den Sniffer und die Warteschlange'''
        self.snif: AsyncSniffer = self.get_intern_sniffer()  # Erstelle eine Instanz des Sniffers
        self.queue = Queue()  # Erstelle eine Thread-sichere Warteschlange
    
    def start(self):
        '''Starte den Sniffer und den Empfangs-Worker'''
        # self.queue.put({0: "this is the beginning"})  # Füge eine Startnachricht zur Warteschlange hinzu
        self.start_receiver_worker()  # Starte den Worker für den Empfang von Daten
        
        self.snif.start()  # Starte den Sniffer
        try:
            self.snif.join()  # Warte, bis der Sniffer stoppt (blockierend)
        except KeyboardInterrupt:
            print("Exiting")  # Ausgabe bei Tastaturunterbrechung
            self.snif.stop()  # Stoppe den Sniffer
        finally:
            self.snif.join()  # Stelle sicher, dass der Sniffer vollständig gestoppt wird
    
    def output_function(self, data):
        '''Diese Funktion wird aufgerufen, wenn ein Paket empfangen wird'''
        self.queue.put(data)  # Füge die empfangenen Daten zur Warteschlange hinzu
        self.queue.join()  # Warte, bis alle Aufgaben in der Warteschlange bearbeitet sind

    def get_intern_sniffer(self) -> AsyncSniffer:
        '''Erstelle den internen Sniffer'''
        s = sniffer.create_sniffer(input_file=None, input_interface=INTERFACE, output_mode="intern", output=self.output_function)
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
            print(f'Finished {item}')  # Ausgabe zur Anzeige, dass die Arbeit an dem Element abgeschlossen ist
            self.queue.task_done()  # Markiere das Element als bearbeitet

if __name__ == "__main__":
    s = My_Sniffer()  # Erstelle eine Instanz des My_Sniffer
    s.start()  # Starte den Sniffer und beginne mit dem Überwachen der Pakete
