import csv
from typing import Protocol

import requests


class OutputWriter(Protocol):
    def write(self, data: dict) -> None:
        raise NotImplementedError


class CSVWriter(OutputWriter):
    def __init__(self, output_file) -> None:
        self.file = open(output_file, "w")
        self.line = 0
        self.writer = csv.writer(self.file)

    def write(self, data: dict) -> None:
        if self.line == 0:
            self.writer.writerow(data.keys())

        self.writer.writerow(data.values())
        self.file.flush()
        self.line += 1

    def __del__(self):
        self.file.close()


class HttpWriter(OutputWriter):
    def __init__(self, output_url) -> None:
        self.url = output_url
        self.session = requests.Session()

    def write(self, data: dict) -> None:
        self.session.post(self.url, json=data)

    def __del__(self):
        self.session.close()

class InternWriter(OutputWriter):
    """
    Writer, der eine Funktion übergeben bekommt, die die Flows verarbeitet. 
    So können in die Flows einem Script weiterverarbeitet werden.
    """
    def __init__(self, output_function):
        self.output_function = output_function
        
    def write(self, data):
        '''write to function instead of url or file'''
        self.output_function(data)
    
def output_writer_factory(output_mode, output) -> OutputWriter:
    match output_mode:
        case "url":
            return HttpWriter(output)
        case "csv":
            return CSVWriter(output)
        case "intern":
            return InternWriter(output)
        case _:
            raise RuntimeError("no output_mode provided")
