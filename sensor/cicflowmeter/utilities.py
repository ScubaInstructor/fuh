import json
import requests
from cicflowmeter import flow
from scapy.utils import PcapWriter
from io import BytesIO
from scapy.all import rdpcap
from subprocess import run


class HttpWriter:
    """
    A class for sending HTTP POST requests.

    This class maintains a session for repeated requests to a specific URL.
    """

    def __init__(self, output_url) -> None:
        """
        Initialise the HttpWriter.

        Args:
            output_url (str): The URL to which the requests should be sent.
        """
        self.url = output_url
        self.session = requests.Session()

    def write(self, flow) -> None:
        """
        Sends two POST requests: one for JSON data (flow data) and one for file data (pcap file data).

        Args:
            data (list):A list with two elements:
                - data[0]: File data (pcap file as BytesIO)
                - data[1]: JSON-Data (Metadata)
        """
        self.session.post(self.url, files={"file": create_BytesIO_pcap_file(flow)})
        self.session.post(self.url, json=flow.get_data())

    def __del__(self):
        self.session.close()


def create_post_request(flow, output_url: str):
    """
    Creates and sends a POST request with the given data.

    Args:
        data (list): A list with two elements
            - data[0]: Flow-Object from which packets should be extracted
            - data[1]: The metadata from the flow on which a prediction can be made.
        output_url (str): The URL to send the request to

    This function extracts the first element of each package and sends it along with the metadata.
    """
    httpwriter = HttpWriter(output_url=output_url)
    # Sends a POST request with:
    # - the flow as JSON data (metadata)
    # - A list of packets without the direction as file data
    httpwriter.write(flow)


def create_BytesIO_pcap_file(flow: flow.Flow) -> BytesIO:
    """
    Creates a pcap file from a Flow object and returns it as a BytesIO object.

    Args:
        flow (flow): A flow object with packet data.

    Returns:
        io.BytesIO: A BytesIO object that contains the pcap data.
    """
    packete = [p[0] for p in flow.packets]

    pcap_buffer = BytesIO()

    # Writing the packets to the BytesIO object
    pktdump = PcapWriter(pcap_buffer)
    for pkt in packete:
        pktdump.write(pkt)

    # Reset the pointer in the BytesIO object
    pcap_buffer.seek(0)

    return pcap_buffer


def flow_to_json(flow) -> str:
    """
    Create Json out of a Flow objeckt with the help of tshark.

    Args:
        flow ([Flow]): The Flow objekt to be transformed

    Returns:
        str: the created Json

    """
    pcap_datei = create_BytesIO_pcap_file(flow=flow)
    command = ["tshark", "-T", "ek", "-r", "-"]  # maybe switch to ek instead of json
    json_packages_bytes = run(command, input=pcap_datei.getvalue(), capture_output=True)
    json_packages_string = json_packages_bytes.stdout.decode("utf-8")
    # json_packages_json = json.dumps(json_packages_string) # remove as it is double encoded else
    return json_packages_string
