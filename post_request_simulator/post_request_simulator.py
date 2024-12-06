# post_request_simulator.py
from scapy.utils import PcapWriter
from io import BytesIO
import requests
import joblib
import numpy as np
from scapy.all import rdpcap
import json

class HttpWriter():
    """
    Eine Klasse zum Senden von HTTP POST-Anfragen.

    Diese Klasse verwaltet eine Session für wiederholte Anfragen an eine bestimmte URL.
    """

    def __init__(self, output_url) -> None:
        """
        Initialisiert den HttpWriter.

        Args:
            output_url (str): Die URL, an die die Anfragen gesendet werden sollen.
        """
        self.url = output_url
        self.session = requests.Session()
      
    def write(self, data: list) -> None:
        """
        Sendet einen einzigen POST-Request mit Datei- und JSON-Daten.

        Args:
            data (list): Eine Liste mit zwei Elementen:
                - data[0]: Datei-Daten (pcap-Datei als Json)
                - data[1]: JSON-Daten (Metadaten)
        """
        files = {
            'file_json': ('flow.pcap', data[0], 'application/vnd.tcpdump.pcap'),
            'metadata_json': ('data.json', json.dumps(data[1]), 'application/json')
        }
        self.session.post(self.url, files=files)

    def __del__(self):
        self.session.close()

def erstelle_post_request(flow, output_url: str):
    """
    Erstellt und sendet einen POST-Request mit den gegebenen Daten.

    Args:
        flow (Flow) der Flow aus dem die Packete extrahiert und in Json umgewandelt, zusammen mit den Metadaten versendet werden.
        output_url (str): Die URL, an die die Anfrage gesendet werden soll

    Diese Funktion extrahiert die Packete des Flows und sendet sie zusammen mit den Metadaten im Json Format.
    """
    httpwriter = HttpWriter(output_url=output_url)
    # Sendet einen POST-Request mit:
    # - den Flow als JSON-Daten (Metadaten)
    # - Eine Liste der packets ohne die Richtung als Datei-Daten
    metadata = flow.get_data()
    pcap_json = pcap_to_json(erstelle_datei(flow=flow))
    httpwriter.write([pcap_json, metadata])

def erstelle_datei(flow) -> BytesIO:
    """
    Erstellt eine pcap-Datei aus einem Flow-Objekt und gibt sie als BytesIO-Objekt zurück.
    
    Args:
        flow (flow): Ein Flow-Objekt mit Paketdaten.
    
    Returns:
        io.BytesIO: Ein BytesIO-Objekt, das die pcap-Daten enthält.
    """ 
    packete = [p[0] for p in flow.packets]
    
    pcap_buffer = BytesIO()

    # Schreiben der Pakete in das BytesIO-Objekt
    pktdump = PcapWriter(pcap_buffer)
    for pkt in packete:
        pktdump.write(pkt)

    # Zurücksetzen des Zeigers im BytesIO-Objekt
    pcap_buffer.seek(0)

    return pcap_buffer


def pcap_to_json(pcap_file):
    packets = rdpcap(pcap_file)
    packet_list = []
    
    for packet in packets:
        packet_dict = {}
        for field_name, value in packet.fields.items():
            packet_dict[field_name] = str(value)
        packet_list.append(packet_dict)
    
    json_data = json.dumps(packet_list, indent=4)
    return json_data

def test_erstelle_post_request():
        flow = joblib.load("post_request_simulator/flow1.pkl")
        erstelle_post_request(flow=flow, output_url=REMOTE_URL)



if __name__ == "__main__":
     REMOTE_URL = "http://localhost:8888/upload"
     test_erstelle_post_request()