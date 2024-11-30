from cicflowmeter import flow
from scapy.utils import PcapWriter
from io import BytesIO, StringIO

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

def sende_BytesIO_datei_per_scp(pcap_buffer: BytesIO, ziel_host: str, ziel_pfad: str, username: str, mySSHK: str = '~/.ssh/id_rsa.pub'):
    """
    Sendet eine pcap-Datei per SCP an einen Zielhost.
    
    Args:
        pcap_buffer (io.BytesIO): Das BytesIO-Objekt mit den pcap-Daten.
        ziel_host (str): Der Hostname oder die IP-Adresse des Zielhosts.
        ziel_pfad (str): Der Pfad auf dem Zielhost, wohin die Datei gesendet werden soll.
    """
    import paramiko

    # Beispiel für die Verwendung von Paramiko für SCP
    ssh = paramiko.SSHClient()
    # Automatisch hostkey akzeptieren evtl zu unsicher?
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    # Verbinden mit dem Zielhost
    ssh.connect(ziel_host, username=username, key_filename=mySSHK)
    
    # SCP verwenden, um die Datei zu übertragen
    with ssh.open_sftp() as sftp:
        with sftp.file(ziel_pfad, 'wb') as remote_file:
            remote_file.write(pcap_buffer.getvalue())
    
    ssh.close()
