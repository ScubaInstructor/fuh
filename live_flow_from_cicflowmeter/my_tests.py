from io import BytesIO
import joblib
from my_sniffer import My_Sniffer
from scapy.sendrecv import AsyncSniffer as ASS
from cicflowmeter.writer import InternWriter, OutputWriter, output_writer_factory
from utilities import erstelle_datei, sende_BytesIO_datei_per_scp
from scapy.utils import PcapReader
from cicflowmeter.flow import Flow
import os


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
