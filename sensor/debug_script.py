

# from time import sleep
# import threading
# from cicflowmeter.flow_session import FlowSession
# from scapy.all import sniff
# from queue import Queue
# from cicflowmeter.flow import Flow

# from queue import Queue
# from dotenv import load_dotenv
# import os


# load_dotenv()

# # Auslesen der Environment-Variable
# SNIFFING_INTERFACE = os.getenv('SNIFFING_INTERFACE')





# def startsniffing(qu: Queue):
#     setattr(FlowSession, "output_mode", "intern")
#     def output_function(s, data: Flow):
#         print(data)
#         qu.put(data)
#     setattr(FlowSession, "output", output_function)
#     sniff(session=FlowSession, iface=SNIFFING_INTERFACE)


# def counter(qu:Queue, n:int):
#     for i in range(n):
#         qu.put(i)



# # Retrieve a single page and report the URL and contents
# def watch(qu):
#     while True:
#         item = qu.get()
#         print(item)
#         qu.task_done()
#         qu.join()


# q = Queue()

# from concurrent.futures import ThreadPoolExecutor
# executor = ThreadPoolExecutor()
# f1 = executor.submit(watch, q)
# f2 = executor.submit(startsniffing, q)



# from time import sleep
# import threading
# from cicflowmeter.flow_session import FlowSession
# from scapy.all import sniff
# from queue import Empty, Queue
# from cicflowmeter.flow import Flow
# from dotenv import load_dotenv
# import os

# load_dotenv()
# # Auslesen der Environment-Variable
# SNIFFING_INTERFACE = os.getenv('SNIFFING_INTERFACE')

# def startsniffing(qu: Queue):
#     setattr(FlowSession, "output_mode", "intern")
#     def output_function(s, data: Flow):
#         with threading.Lock():  # Verwenden des Lock-Kontextmanagers
#             print(data)
#             qu.put(data)
#     setattr(FlowSession, "output", output_function)
#     try:
#         sniff(session=FlowSession, iface=SNIFFING_INTERFACE)
#     except Exception as e:
#         print(f"Error while sniffing: {e}")


# def counter(qu: Queue, n: int):
#     for i in range(n):
#         qu.put(i)

# # Retrieve a single page and report the URL and contents
# def watch(qu: Queue):
#     while True:
#         with threading.Lock():
#             try:
#                 item = qu.get(timeout=1)
#                 print(item)
#                 qu.task_done()
#             except Empty:
#                 continue  # Wenn die Queue leer ist, einfach weitermachen
            

# # Hauptteil, der Threads manuell erstellt und startet
# q = Queue()

# # Thread für die Sniffing-Funktion

# # Thread für die watch-Funktion
# watch_thread = threading.Thread(target=watch, args=(q,), daemon=True)
# watch_thread.start()

# startsniffing(q)


# from time import sleep
# import multiprocessing
# from cicflowmeter.flow_session import FlowSession
# from scapy.all import sniff
# from queue import Empty
# from cicflowmeter.flow import Flow
# from dotenv import load_dotenv
# import os

# load_dotenv()
# # Auslesen der Environment-Variable
# SNIFFING_INTERFACE = os.getenv('SNIFFING_INTERFACE')

# global q 
# q = multiprocessing.Queue()

# setattr(FlowSession, "output_mode", "intern")
# def output_function(s, data: Flow):
#     # Diese Funktion wird durch sniffing aufgerufen, um das Ergebnis in die Queue zu legen
#     q.put(data)  # Die Queue muss im Multiprocessing-Modus verwendet werden

# setattr(FlowSession, "output", output_function)

# def startsniffing():   
#     try:
#         sniff(session=FlowSession, iface=SNIFFING_INTERFACE)
#     except Exception as e:
#         print(f"Error while sniffing: {e}")



# # Retrieve a single page and report the URL and contents
# def watch(qu: multiprocessing.Queue):
#     while True:
#         try:
#             item = q.get(timeout=1)
#             print(item)
#             #qu.task_done()
#         except Empty:
#             continue  # Wenn die Queue leer ist, einfach weitermachen


# # Hauptteil, der Prozesse manuell erstellt und startet
# #if __name__ == "__main__":
# # q = multiprocessing.Queue()

# # Prozess für die watch-Funktion
# watch_process = multiprocessing.Process(target=watch, args=(q,))
# watch_process.start()

# # Prozess für die Sniffing-Funktion
# sniffing_process = multiprocessing.Process(target=startsniffing)
# sniffing_process.start()

# Optional: Prozess für das Zählen und Hinzufügen von Daten zur Queue
#counter_process = multiprocessing.Process(target=counter, args=(q, 10))
#counter_process.start()

# Warten, dass alle Prozesse beendet sind
# sniffing_process.join()
# watch_process.join()
#counter_process.join()

# multiThreading und -processeing versucht klappt nicht...







# from cicflowmeter.flow_session import FlowSession
# from scapy.all import AsyncSniffer
# from time import sleep

# setattr(FlowSession, "output_mode", "intern")

# def output_function(s, pkt):
#     print(f"Received packet: {pkt}")

# setattr(FlowSession, "output", output_function)

# sniffer = AsyncSniffer(session=FlowSession, iface="enp12s0")
# sniffer.start()
# sleep(2)
# sniffer.stop()


import joblib
import pandas as pd
from pipelining_utilities import adapt_for_prediction
from sklearn.ensemble import RandomForestClassifier

flow = joblib.load("/home/georg/Desktop/FaPra/python/fuh/live_flow_from_cicflowmeter/flow2.pkl")
flow_data: dict = pd.DataFrame([flow.get_data()])
model: RandomForestClassifier = joblib.load("/home/georg/Desktop/FaPra/python/fuh/sensor/model.pkl")
scaler = joblib.load("/home/georg/Desktop/FaPra/python/fuh/sensor/scaler.pkl")
ipca = joblib.load("/home/georg/Desktop/FaPra/python/fuh/sensor/ipca_mit_size_34.pkl")
flow_data: pd.DataFrame = adapt_for_prediction(data=flow_data,scaler=scaler,ipca=ipca,ipca_size=34)
pred = model.predict(flow_data)
prob = model.predict_proba(flow_data)
d = {}
for i in range(len(prob[0])):
    d[model.classes_[i]] = prob[0][i]
print(d)