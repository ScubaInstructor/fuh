from io import BytesIO
import joblib
from my_sniffer import My_Sniffer
from scapy.sendrecv import AsyncSniffer as ASS
from cicflowmeter.writer import InternWriter, OutputWriter, output_writer_factory
from utilities import erstelle_datei


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
        flow = joblib.load("flow2.pkl")
        assert isinstance(BytesIO, erstelle_datei(flow))