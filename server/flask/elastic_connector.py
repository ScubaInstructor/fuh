from time import sleep
from elasticsearch import Elasticsearch
from elasticsearch_dsl import AsyncSearch, Document, async_connections, AsyncUpdateByQuery
import asyncio

INDEX_NAME = "network_flows"
class Custom_Elastticsearch_Connector():
    
    def __init__(self, hosts: str = ['https://localhost:9200'], api_key:str="NERKY1JwUUJtbWlFNHp1Q3VFZFE6SERGZkJpZDRSTC1uZUpZZXhVQ2hBUQ==", verify_certs=False):
        '''Initialise the Elasticsearch connector'''
        self.hosts = hosts
        self.api_key = api_key
        async_connections.create_connection(hosts=hosts, api_key=api_key, verify_certs=verify_certs)


    def get_all_unseen_flows(self):
        
        dataframes = {}
        filestore = {}
        probabilities_store = {}
        predictions_store = {}
        sensor_names = {}
        timestamps = {}
        sensor_ports = {}
        partner_ips = {}
        partner_ports = {}
        attack_classes = {} # Store selected attack classes
        has_been_seen = {}  # Store if entries have been seen
        flow_id_store = {}  # Store flow ids

        async def get_unseen_flows():
            s = AsyncSearch(index=INDEX_NAME) \
                .query("match", has_been_seen="false")   \
                #.filter("term", category="search") \
                #.exclude("match", description="beta")
            async for hit in s:
                id = hit.id
                flow_id_store[id] = id
                dataframes[id] = hit.flow_data
                partner_ips[id] = hit.partner_ip
                sensor_names[id] = hit.sensor_name
                predictions_store[id] = hit.prediction
                probabilities_store[id] = dict(hit.probabilities)
                partner_ips[id] = hit.partner_ip        
                partner_ports[id] = hit.partner_port    
                sensor_ports[id] = hit.sensor_port      
                timestamps[id] = hit.timestamp
                has_been_seen[id] = hit.has_been_seen
                attack_classes[id] = hit.attack_class   
                filestore[id] = hit.pcap_data           
            return flow_id_store, dataframes, filestore, probabilities_store, predictions_store, sensor_names, timestamps, sensor_ports, partner_ips, partner_ports, attack_classes, has_been_seen

        return asyncio.run(get_unseen_flows())


    def set_flow_as_seen(self, flow_id:str):
        async def _set_flow_as_seen(flow_id):
            aubq = AsyncUpdateByQuery(index=INDEX_NAME).filter("term", id=flow_id) 
            aubq.script(source="ctx_source.has_been_seen = true")
            aubq.execute()
        asyncio.run(_set_flow_as_seen(flow_id=flow_id))

    def set_attack_class(self, flow_id:str, attack_class:str):
        async def _set_attack_class(flow_id, attack_class):
            s = AsyncUpdateByQuery(index=INDEX_NAME).filter("term", id=flow_id)
            s.update(body={"doc": {"attack_class": attack_class}})
        asyncio.run(_set_attack_class(flow_id=flow_id, attack_class=attack_class))
        
if __name__ == '__main__':
    # for testing purposes
    cec = Custom_Elastticsearch_Connector()
    a,b,c,d,e,f,g,h,i,j,k, i = cec.get_all_unseen_flows()
    print(i.get("034c6fe3-27ed-45ef-9714-18c35b5ca80b"))
    cec.set_flow_as_seen("034c6fe3-27ed-45ef-9714-18c35b5ca80b")
    sleep(5)
    a,b,c,d,e,f,g,h,i,j,k, i = cec.get_all_unseen_flows()
    print(i.get("034c6fe3-27ed-45ef-9714-18c35b5ca80b"))

