import json
import requests
from cicflowmeter import flow
from scapy.utils import PcapWriter
from io import BytesIO
import paramiko

def erstelle_datei(flow: flow.Flow) -> BytesIO:
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

def sende_BytesIO_datei_per_scp(pcap_buffer: BytesIO, ziel_host: str, ziel_pfad: str, username: str, mySSHK: str = '/app/sshkey'):
    """
    Sendet eine pcap-Datei per SCP an einen Zielhost.
    
    Args:
        pcap_buffer (io.BytesIO): Das BytesIO-Objekt mit den pcap-Daten.
        ziel_host (str): Der Hostname oder die IP-Adresse des Zielhosts.
        ziel_pfad (str): Der Pfad auf dem Zielhost, wohin die Datei gesendet werden soll.
    """
    # Beispiel für die Verwendung von Paramiko für SCP
    ssh = paramiko.SSHClient()
    # Automatisch hostkey akzeptieren evtl zu unsicher?
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    try:
        # Verbinden mit dem Zielhost
        ssh.connect(ziel_host, username=username, key_filename=mySSHK, banner_timeout=30)
        
        # SCP verwenden, um die Datei zu übertragen
        with ssh.open_sftp() as sftp:
            with sftp.file(ziel_pfad, 'wb') as remote_file:
                remote_file.write(pcap_buffer.getvalue())
    except paramiko.ssh_exception.AuthenticationException as ae:
        print("Authentication failed.")    
        print(ae)
    except paramiko.ssh_exception.SSHException as se:
        print("Timeout Fehler!")    
        print(se)

    ssh.close()

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
        Sendet zwei POST-Anfragen: eine für JSON-Daten (Flow-Daten) und eine für Datei-Daten (pcap-Dateie-Daten).

        Args:
            data (list): Ein Liste mit zwei Elementen:
                - data[0]: Datei-Daten (pcap-Datei als BytesIO)
                - data[1]: JSON-Daten (Metadaten)
        """
        self.session.post(self.url, files={'file': data[0]})
        self.session.post(self.url, json=data[1])
        


    def __del__(self):
        self.session.close()

def erstelle_post_request(data: list, output_url: str):
    """
    Erstellt und sendet einen POST-Request mit den gegebenen Daten.

    Args:
        data (list): Eine Liste mit zwei Elementen:
            - data[0]: Flow-Object aus dem die Packete extrahiert werden sollen.
            - data[1]: Flow (nur die reduzierten Daten)
        output_url (str): Die URL, an die die Anfrage gesendet werden soll

    Diese Funktion extrahiert das erste Element jedes Pakets und sendet es zusammen mit den Metadaten.
    """
    httpwriter = HttpWriter(output_url=output_url)
    # Sendet einen POST-Request mit:
    # - den Flow als JSON-Daten (Metadaten)
    # - Eine Liste der packets ohne die Richtung als Datei-Daten
    httpwriter.write([erstelle_datei(data[0]), data[1]])

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