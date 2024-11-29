from io import BytesIO
import joblib
from my_sniffer import My_Sniffer
from scapy.sendrecv import AsyncSniffer as ASS
from cicflowmeter.writer import InternWriter, OutputWriter, output_writer_factory
from utilities import erstelle_datei
from scapy.utils import PcapReader
from cicflowmeter.flow import Flow


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
        assert reader.read_all()[0] == flow.packets[0][0] 