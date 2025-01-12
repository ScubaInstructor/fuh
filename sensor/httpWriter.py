from  requests import Session


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
        self.session = Session()
    
    def notify(self, token):
        """
        Notify the server about the new data.

        Args:
            token (str): the authentication token for the server.

        Returns:
            none:
        """
        headers = {'Authorization': f'Bearer {token}'}
        return self.session.post(self.url, headers=headers)