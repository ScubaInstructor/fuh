import json
from requests import Response, Session


class HttpWriter:
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
        self.session = Session()

    def notify(self, token):
        """
        Notify the server about the new data.

        Args:
            token (str): the authentication token for the server.

        Returns:
            none:
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.session.post(self.url, headers=headers)

    def write(self, data: dict, token: str) -> Response:
        """
        Sends a single POST-Request with all the Data to the Server.

        Args:
            data (dict): A dict of elements to be transferred containing
                - flow_id = the flow_id,
                - sensor_name = AN unique name for the sensor
                - sensor_port = the port of the sensor
                - partner_ip = Ip of the other endpoint of the flow
                - partner_port = the port of the partner
                - timestamp = the timestamp of the flow
                - prediction = the prediction of the flow
                - probabilities = probabilities
                - attack_class = The class a flow has been classified as
                - has_been_seen = A boolean indicating if the flow has been seen before
                - flow_data = th flow data for retraining a model
                - pcap_data = the PCAP data as Base 64 encoded String
                - model_hash = The hash of the model in use
            token (str): the authentication token
        Returns: Response: The response from the post request
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.session.post(self.url, json=data, headers=headers)

    def download_file(self, token: str):
        headers = {"Authorization": f"Bearer {token}"}
        return self.session.get(self.url, headers=headers)

    def get_model_hash(self, token):
        headers = {"Authorization": f"Bearer {token}"}
        resp = json.loads(self.session.get(self.url, headers=headers).text)
        return resp["model_hash"]
