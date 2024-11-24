from cicflowmeter import sniffer
from queue import Queue
from scapy.sendrecv import AsyncSniffer
import threading

class My_Sniffer():
    def __init__(self) -> None:
        self.snif: AsyncSniffer = self.get_intern_sniffer()
        self.queue = Queue()
        self.queue
    
    def start(self):
        '''start the sniffer and the receiving worker'''
        self.queue.put({0:"this is the beginning"})
        # start the receiver
        self.start_receiver_worker()
        
        self.snif.start()
        try:
            self.snif.join()
        except KeyboardInterrupt:
            print("Exiting")
            self.snif.stop()
        finally:
            self.snif.join()
            self.queue.shutdown()
    
    def output_function(self, data):
        ''' This function will be invoked in the sniffer-writer, when packeg was received'''
        self.queue.put(data)
        self.queue.join()

    def get_intern_sniffer(self) -> AsyncSniffer:
        '''create the sniffer'''
        s = sniffer.create_sniffer(input_file=None, input_interface="enp12s0",output_mode="intern", output=self.output_function)
        #s.count = 10 # for testing only
        return s

    def start_receiver_worker(self):
        '''start the worker in a thread'''
        threading.Thread(target=self.worker, daemon=True).start()
   
    def worker(self):
        '''the work wich will be done on a seperate thread'''
        while True:
            item = self.queue.get()
            print(f'Working on {item}')
            print(f'Finished {item}')
            self.queue.task_done()    




if __name__ == "__main__":
    s = My_Sniffer()
    s.start()




    