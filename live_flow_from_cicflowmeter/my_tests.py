from datetime import datetime
from io import BytesIO

from elasticsearch import BadRequestError, Elasticsearch
from sklearn.ensemble import RandomForestClassifier
from utilities import flow_to_json
from pipelining_utilities import adapt_for_prediction
import joblib
from my_sniffer import My_Sniffer
from scapy.sendrecv import AsyncSniffer as ASS
from cicflowmeter.writer import InternWriter, OutputWriter, output_writer_factory
from utilities import erstelle_datei, sende_BytesIO_datei_per_scp, erstelle_post_request
from scapy.utils import PcapReader
from cicflowmeter.flow import Flow
import os
import numpy as np
import pandas as pd


class Tests():    
        
    def test_class_of_sniffer(self):
        ms = My_Sniffer()
        assert isinstance(ms.get_intern_sniffer(), ASS)
    
    def test_intern_writer(self):
        self.data = 0
        def intern_test_function(a:dict):
            self.data = a[0]
        int_writer = output_writer_factory(output_mode="intern", output=intern_test_function)
        int_writer.write(data={0:4})
        assert self.data == 4

    def test_utilities_create_file(self):
        flow: Flow = joblib.load("flow2.pkl")
        print(flow.packets[0][0])
        pcap = erstelle_datei(flow)
        assert isinstance(pcap, BytesIO)
        reader = PcapReader(pcap)
        returning_flows = reader.read_all()
        for i in range(len(returning_flows)):
            assert returning_flows[i] == flow.packets[i][0] 
    
    def test_sende_per_scp(self):
        host = "localhost"
        path = os.getcwd()
        filename = path+"/"+"test.pcap" # Nur Linux wg '/'
        sshfile = os.path.expanduser('~')+"/.ssh/id_ed25519.pub"
        username = "georg"
        print(path)
        pcap_BytesIO = erstelle_datei(joblib.load("flow2.pkl"))
        sende_BytesIO_datei_per_scp(pcap_BytesIO, host, filename, username, sshfile)
        assert os.path.exists(filename) == True
        sent_reader = PcapReader(pcap_BytesIO)
        received_reader = PcapReader(filename)
        sent_flows = sent_reader.read_all()
        received_flows = received_reader.read_all()
        for i in range(len(sent_flows)):
            assert sent_flows[i] == received_flows[i]
        os.remove(filename)

    # works only with running flask server
    # def test_erstelle_post_request(self):
    #     attribs = {'src_ip': '192.168.178.71', 'dst_ip': '224.0.0.251', 'src_port': 5353, 'dst_port': 5353, 'protocol': 17, 'timestamp': '2024-12-04 19:40:29', 'flow_duration': 95.08313632011414, 'flow_byts_s': 26.06140369263143, 'flow_pkts_s': 0.18930801713775855, 'fwd_pkts_s': 0.18930801713775855, 'bwd_pkts_s': 0.0, 'tot_fwd_pkts': 18, 'tot_bwd_pkts': 0, 'totlen_fwd_pkts': 2478, 'totlen_bwd_pkts': 0, 'fwd_pkt_len_max': 161, 'fwd_pkt_len_min': 91, 'fwd_pkt_len_mean': np.float64(137.66666666666666), 'fwd_pkt_len_std': np.float64(32.99831645537222), 'bwd_pkt_len_max': 0, 'bwd_pkt_len_min': 0, 'bwd_pkt_len_mean': 0, 'bwd_pkt_len_std': np.float64(0.0), 'pkt_len_max': 161, 'pkt_len_min': 91, 'pkt_len_mean': np.float64(137.66666666666666), 'pkt_len_std': np.float64(32.99831645537222), 'pkt_len_var': np.float64(1088.888888888889), 'fwd_header_len': 144, 'bwd_header_len': 0, 'fwd_seg_size_min': 8, 'fwd_act_data_pkts': 18, 'flow_iat_mean': np.float64(5.593125665889067), 'flow_iat_max': 43.32627868652344, 'flow_iat_min': 0.2378673553466797, 'flow_iat_std': np.float64(10.261862173246321), 'fwd_iat_tot': 95.08313632011414, 'fwd_iat_max': 43.32627868652344, 'fwd_iat_min': 0.2378673553466797, 'fwd_iat_mean': np.float64(5.593125665889067), 'fwd_iat_std': np.float64(10.261862173246321), 'bwd_iat_tot': 0, 'bwd_iat_max': 0, 'bwd_iat_min': 0, 'bwd_iat_mean': 0, 'bwd_iat_std': 0, 'fwd_psh_flags': 0, 'bwd_psh_flags': 0, 'fwd_urg_flags': 0, 'bwd_urg_flags': 0, 'fin_flag_cnt': 0, 'syn_flag_cnt': 0, 'rst_flag_cnt': 0, 'psh_flag_cnt': 0, 'ack_flag_cnt': 0, 'urg_flag_cnt': 0, 'ece_flag_cnt': 0, 'down_up_ratio': 0.0, 'pkt_size_avg': 137.66666666666666, 'init_fwd_win_byts': 0, 'init_bwd_win_byts': 0, 'active_max': 0, 'active_min': 0, 'active_mean': 0, 'active_std': 0, 'idle_max': 43.32627868652344, 'idle_min': 8.010166883468628, 'idle_mean': np.float64(25.668222784996033), 'idle_std': np.float64(17.658055901527405), 'fwd_byts_b_avg': 325.5, 'fwd_pkts_b_avg': 4.5, 'bwd_byts_b_avg': 0, 'bwd_pkts_b_avg': 0, 'fwd_blk_rate_avg': 259.50278188187167, 'bwd_blk_rate_avg': 0, 'fwd_seg_size_avg': np.float64(137.66666666666666), 'bwd_seg_size_avg': 0, 'cwr_flag_count': 0, 'subflow_fwd_pkts': 18, 'subflow_bwd_pkts': 0, 'subflow_fwd_byts': 2478, 'subflow_bwd_byts': 0}
    #     flow = joblib.load("flow2.pkl")
    #     erstelle_post_request(data=[flow, attribs], output_url="http://localhost:8888/upload")

    def test_make_prediction(self):
        flow: Flow = joblib.load("flow1.pkl")
        flow: dict = pd.DataFrame([flow.get_data()])
        model: RandomForestClassifier = joblib.load("/home/georg/Desktop/FaPra/python/fuh/sensor/model.pkl")
        scaler = joblib.load("/home/georg/Desktop/FaPra/python/fuh/sensor/scaler.pkl")
        ipca = joblib.load("/home/georg/Desktop/FaPra/python/fuh/sensor/ipca_mit_size_34.pkl")
        flow_data: pd.DataFrame = adapt_for_prediction(data=flow,scaler=scaler,ipca=ipca,ipca_size=34)
        pred = model.predict(flow_data)
        prob = model.predict_proba(flow_data)
        assert pred == ["BENIGN"]
        assert prob.max() > 0.85
        assert prob.max() - prob.mean() > 0.6

    def test_upload_to_elastic(self):
        ES_INDEX = "pytest_index"
        es = Elasticsearch(
            f"https://localhost:9200",
            # api_key=ES_API_KEY,  # Authentication via API-key
            basic_auth=("elastic","elastic"),
            verify_certs=False,
            ssl_show_warn=False,
            request_timeout=30,
            retry_on_timeout=True
        )
        #es.indices.delete(index=ES_INDEX)
        flow: Flow = joblib.load("flow1.pkl")
        flow_data: dict = pd.DataFrame([flow.get_data()])
        try:
            es.indices.create(index=ES_INDEX)
        except BadRequestError as bre:
            print("Index already existent")
        pcap_json = flow_to_json(flow)
        #mapping = {"properties": {"pcap_data": {"dynamic": "false","properties": {"timestamp": {"type": "date"},"layers": {"properties": {"frame": {"properties": {"frame_frame_len": {"type": "long"},"frame_frame_protocols": {"type": "keyword"}}},"ip": {"properties": {"ip_ip_src": {"type": "ip"},"ip_ip_dst": {"type": "ip"}}},"udp": {"properties": {"udp_udp_srcport": {"type": "integer"},"udp_udp_dstport": {"type": "integer"}}}}}}}}}
        #es.indices.put_template(mappings = {"properties": {"ip":{"type":"ip"}}}, name="packets", index_patterns= "pytest_*")
        #es.indices.put_template(mappings = mapping, name="packets",index_patterns= "pytest_*")
        mapping = {"pcap_data": {"dynamic": "false","properties": {"timestamp": {"type": "date"},"layers": {"properties": {"frame": {"properties": {"frame_frame_len": {"type": "long"},"frame_frame_protocols": {"type": "keyword"}}},"ip": {"properties": {"ip_ip_src": {"type": "ip"},"ip_ip_dst": {"type": "ip"}}},"udp": {"properties": {"udp_udp_srcport": {"type": "integer"},"udp_udp_dstport": {"type": "integer"}}}}}}}}
        #es.indices.put_mapping(properties=mapping, index=ES_INDEX, )

        doc = {
            'pcap_data': pcap_json,  # Add the PCAP data as Json
            'id': 1234,
            'sensor_name': "pytest", # unique Sensorname
            'timestamp': datetime.now().isoformat(),
            'flow_data': flow.get_data(),
            'prediction': "TEST",
            'probabilities': {"a":0,"b":0,"c":1},
            'has_been_seen':False,
            'source_ip': flow.src_ip, 
            'pcap_metadata': {
                'packet_count': len(flow.packets)
            }                        
        }
        es.index(index=ES_INDEX, body=doc)
        es.indices.delete(index=ES_INDEX)

