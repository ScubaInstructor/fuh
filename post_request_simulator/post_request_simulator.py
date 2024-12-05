# post_request_simulator.py
from scapy.utils import PcapWriter
from io import BytesIO
import requests
import joblib
import numpy as np


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

def test_erstelle_post_request():
        attribs = {'src_ip': '192.168.178.71', 'dst_ip': '224.0.0.251', 'src_port': 5353, 'dst_port': 5353, 'protocol': 17, 'timestamp': '2024-12-04 19:40:29', 'flow_duration': 95.08313632011414, 'flow_byts_s': 26.06140369263143, 'flow_pkts_s': 0.18930801713775855, 'fwd_pkts_s': 0.18930801713775855, 'bwd_pkts_s': 0.0, 'tot_fwd_pkts': 18, 'tot_bwd_pkts': 0, 'totlen_fwd_pkts': 2478, 'totlen_bwd_pkts': 0, 'fwd_pkt_len_max': 161, 'fwd_pkt_len_min': 91, 'fwd_pkt_len_mean': np.float64(137.66666666666666), 'fwd_pkt_len_std': np.float64(32.99831645537222), 'bwd_pkt_len_max': 0, 'bwd_pkt_len_min': 0, 'bwd_pkt_len_mean': 0, 'bwd_pkt_len_std': np.float64(0.0), 'pkt_len_max': 161, 'pkt_len_min': 91, 'pkt_len_mean': np.float64(137.66666666666666), 'pkt_len_std': np.float64(32.99831645537222), 'pkt_len_var': np.float64(1088.888888888889), 'fwd_header_len': 144, 'bwd_header_len': 0, 'fwd_seg_size_min': 8, 'fwd_act_data_pkts': 18, 'flow_iat_mean': np.float64(5.593125665889067), 'flow_iat_max': 43.32627868652344, 'flow_iat_min': 0.2378673553466797, 'flow_iat_std': np.float64(10.261862173246321), 'fwd_iat_tot': 95.08313632011414, 'fwd_iat_max': 43.32627868652344, 'fwd_iat_min': 0.2378673553466797, 'fwd_iat_mean': np.float64(5.593125665889067), 'fwd_iat_std': np.float64(10.261862173246321), 'bwd_iat_tot': 0, 'bwd_iat_max': 0, 'bwd_iat_min': 0, 'bwd_iat_mean': 0, 'bwd_iat_std': 0, 'fwd_psh_flags': 0, 'bwd_psh_flags': 0, 'fwd_urg_flags': 0, 'bwd_urg_flags': 0, 'fin_flag_cnt': 0, 'syn_flag_cnt': 0, 'rst_flag_cnt': 0, 'psh_flag_cnt': 0, 'ack_flag_cnt': 0, 'urg_flag_cnt': 0, 'ece_flag_cnt': 0, 'down_up_ratio': 0.0, 'pkt_size_avg': 137.66666666666666, 'init_fwd_win_byts': 0, 'init_bwd_win_byts': 0, 'active_max': 0, 'active_min': 0, 'active_mean': 0, 'active_std': 0, 'idle_max': 43.32627868652344, 'idle_min': 8.010166883468628, 'idle_mean': np.float64(25.668222784996033), 'idle_std': np.float64(17.658055901527405), 'fwd_byts_b_avg': 325.5, 'fwd_pkts_b_avg': 4.5, 'bwd_byts_b_avg': 0, 'bwd_pkts_b_avg': 0, 'fwd_blk_rate_avg': 259.50278188187167, 'bwd_blk_rate_avg': 0, 'fwd_seg_size_avg': np.float64(137.66666666666666), 'bwd_seg_size_avg': 0, 'cwr_flag_count': 0, 'subflow_fwd_pkts': 18, 'subflow_bwd_pkts': 0, 'subflow_fwd_byts': 2478, 'subflow_bwd_byts': 0}
        flow = joblib.load("flow2.pkl")
        erstelle_post_request(data=[flow, attribs], output_url=REMOTE_URL)

if __name__ == "__main__":
     REMOTE_URL = "http://localhost:8888/upload"
     test_erstelle_post_request()