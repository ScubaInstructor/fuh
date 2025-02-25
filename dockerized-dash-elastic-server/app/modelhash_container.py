import hashlib


class Modelhash_Container:
    """
    Class to hold the model hash
    """

    def __init__(self, filename: str):
        """create the Container

        Args:
            filename (str): the filename of the model
        """
        self.filename = filename
        self.model_hash = self.compute_file_hash(filename)

    def set_hash(self, hash: str):
        """set the model hash

        Args:
            hash (str): the new model hash
        """
        self.model_hash = hash

    def get_hash(self) -> str:
        """
            get the current model hash

        Returns:
            str: the model hash
        """
        return self.model_hash

    def refresh_hash(self):
        """
        set a new hashvalue for the initial set file
        """
        self.model_hash = self.compute_file_hash(self.filename)

    def compute_file_hash(self, file_path: str) -> str:
        """Compute the hash of a file using the sha265 algorithm.

        Args:
            - file_path (str) = the path to the file

        Returns:
            str: The hash value
        """
        hash_func = hashlib.sha256()
        with open(file_path, "rb") as file:
            # Read the file in chunks of 8192 bytes
            while chunk := file.read(8192):
                hash_func.update(chunk)

        return hash_func.hexdigest()
