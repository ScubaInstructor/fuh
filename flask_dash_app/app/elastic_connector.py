from elasticsearch import AsyncElasticsearch, AuthenticationException
from elasticsearch_dsl import AsyncSearch, connections
import asyncio
import pandas as pd #TODO not necessary
from datetime import datetime
from elasticsearch.exceptions import AuthenticationException
from pandas import DataFrame, concat, to_datetime
import dotenv
from os import getenv

# Load from .env File
dotenv.load_dotenv()
INDEX_NAME = "network_flows" # TODO extract from docker-compose
MODEL_INDEX_NAME = "model_properties"
# Load from "shared_secrets" docker volume
dotenv.load_dotenv(dotenv_path="/shared_secrets/server-api-key.env")
API_KEY = "ZlNxdjBwUUJCVVdKMnVFbFljcng6ZzdYQzA1anNRa21Ubjh5bmtnVktTdw=="

class CustomElasticsearchConnector:
    """
    A custom connector class for interacting with an Elasticsearch instance.

    Attributes:
        api_key (str): The API key for authentication.
        hosts (list): A list of Elasticsearch hosts.
        verify_certs (bool): Whether to verify SSL certificates.
    """

    def __init__(self, api_key:str=API_KEY, hosts:str=['https://localhost:9200'], verify_certs:bool=False):
        """
        Initializes the CustomElasticsearchConnector.

        Args:
            api_key (str): The API key for authentication.
            hosts (list): A list of Elasticsearch hosts.
            verify_certs (bool): Whether to verify SSL certificates.
        """
        self.hosts = hosts
        self.api_key = api_key
        self.verify_certs = verify_certs
        connections.create_connection(hosts=hosts, api_key=api_key, verify_certs=verify_certs, ssl_show_warn=False)
    
    async def get_all_flows(self, view:str="all", size:int=20, include_pcap:bool= False, flow_id:str=None):
        """
        Retrieves all flow documents from Elasticsearch. Optionally, only retrieves flows that have not been seen. 
        Run with asyncio.run(get_all_flows()). Will get the latest flows first.

        Args:
            view (str): all = all flows with a limt of 10000, seen = only seen flows, unseen = only unseen flows.
            size (int): The number of flows to retrieve. 10000 is the maximum of elastic search.
            include_pcap(bool) Include the Pcap Data containing the iindividual Packets of the flows

        Returns:
            DataFrame containing the flow data
        """
        async def _get_all_flows(self, view, size, include_pcap, flow_id):
           
            async with AsyncElasticsearch(hosts=self.hosts, api_key=self.api_key, verify_certs=self.verify_certs, ssl_show_warn=False) as client:
                # Define view query mapping
                view_queries = {
                    "seen": {"has_been_seen": "true"},
                    "unseen": {"has_been_seen": "false"},
                    "all": None
                }
                
                # Base search
                s = AsyncSearch(using=client, index=INDEX_NAME)
                
                

                # Add view filter if needed
                if view_queries.get(view):
                    s = s.query("match", **view_queries[view])
                else:
                    s = s.query("match_all")
                
                # Add flow_id filter if needed --> Overwrite has been seen criteria
                if flow_id:
                    s = s.query("match", flow_id=flow_id)

                # Add source filtering if pcap not needed
                if not include_pcap:
                    s = s.source(excludes=['pcap_data'])
                    
                # Add size and sorting
                s = s.extra(size=size).sort({"timestamp": {"order": "desc"}})
                
                # Process results
                df_list = []
                async for hit in s:
                    df_list.append(pd.DataFrame([hit.to_dict()]))
                if len(df_list) > 0:
                    df = pd.concat(df_list)
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                    # Convert string to boolean
                    df['has_been_seen'] = df['has_been_seen'].replace('true', True)
                    return df
                else: 
                    return DataFrame()
        return await _get_all_flows(self, view=view, size=size, include_pcap=include_pcap, flow_id=flow_id)
    
    async def legacy_get_all_flows(self, onlyunseen:bool=False, size:int=20):
        """
        Retrieves all flow documents from Elasticsearch. Optionally, only retrieves flows that have not been seen. 
        Run with asyncio.run(get_all_flows()). Will get the latest flows first.

        Args:
            onlyunseen (bool): If True, only retrieves flows that have not been seen.
            size (int): The number of flows to retrieve. If None all will be retrieved: Maximum is 10000 as this is set in elastic.

        Returns:
            Tuple containing various dictionaries with flow data:
                - id_store: Mapping of flow IDs to document IDs in Elasticsearch.
                - dataframes: Mapping of flow IDs to flow data.
                - filestore: Mapping of flow IDs to PCAP data.
                - probabilities_store: Mapping of flow IDs to probabilities.
                - predictions_store: Mapping of flow IDs to predictions.
                - sensor_names: Mapping of flow IDs to sensor names.
                - timestamps: Mapping of flow IDs to timestamps.
                - sensor_ports: Mapping of flow IDs to sensor ports.
                - partner_ips: Mapping of flow IDs to partner IPs.
                - partner_ports: Mapping of flow IDs to partner ports.
                - attack_classes: Mapping of flow IDs to attack classes.
                - has_been_seen: Mapping of flow IDs to seen status.
        """
        async def _legacy_get_all_flows(self, onlyunseen, size):
            dataframes = {}
            filestore = {}
            probabilities_store = {}
            predictions_store = {}
            sensor_names = {}
            timestamps = {}
            sensor_ports = {}
            partner_ips = {}
            partner_ports = {}
            attack_classes = {}
            has_been_seen = {}
            id_store = {}

            async with AsyncElasticsearch(hosts=self.hosts, api_key=self.api_key, verify_certs=self.verify_certs, ssl_show_warn=False) as client:
                if size:
                    if onlyunseen:
                        s = AsyncSearch(using=client, index=INDEX_NAME) \
                            .query("match", has_been_seen="false") \
                            .extra(size=size) \
                            .sort({"timestamp": {"order": "desc"}})
                    else:
                        s = AsyncSearch(using=client, index=INDEX_NAME).query("match_all") \
                            .extra(size=size) \
                            .sort({"timestamp": {"order": "desc"}})
                else: # size == None
                    if onlyunseen:
                        s = AsyncSearch(using=client, index=INDEX_NAME) \
                            .query("match", has_been_seen="false") \
                            .extra(size=10000) \
                            .sort({"timestamp": {"order": "desc"}})
                    else:
                        s = AsyncSearch(using=client, index=INDEX_NAME).query("match_all") \
                            .extra(size=10000) \
                            .sort({"timestamp": {"order": "desc"}})
                async for hit in s:
                    id = hit.flow_id
                    id_store[id] = hit.meta.id
                    dataframes[id] = hit.flow_data
                    partner_ips[id] = hit.partner_ip
                    sensor_names[id] = hit.sensor_name
                    predictions_store[id] = hit.prediction
                    probabilities_store[id] = dict(hit.probabilities)
                    partner_ports[id] = hit.partner_port
                    sensor_ports[id] = hit.sensor_port
                    timestamps[id] = hit.timestamp
                    has_been_seen[id] = hit.has_been_seen
                    attack_classes[id] = hit.attack_class
                    filestore[id] = hit.pcap_data

            return id_store, dataframes, filestore, probabilities_store, predictions_store, sensor_names, timestamps, sensor_ports, partner_ips, partner_ports, attack_classes, has_been_seen
        return await _legacy_get_all_flows(self, onlyunseen=onlyunseen, size=size)
     
    async def set_flow_as_seen(self, flow_id: str):
        """
        Marks a flow as seen in the Elasticsearch index.

        Args:
            flow_id (str): The ID of the flow to be marked as seen.

        Returns:
            None
        """
        async with AsyncElasticsearch(hosts=self.hosts, api_key=self.api_key, verify_certs=self.verify_certs, ssl_show_warn=False) as client:
            s = AsyncSearch(using=client, index=INDEX_NAME).query("match", flow_id=flow_id)
            async for hit in s:
                return await client.update(index=INDEX_NAME, refresh="wait_for", id=hit.meta.id, body={"doc": {"has_been_seen": "true"}})


    async def set_attack_class(self, flow_id: str, attack_class: str):
        """
        Sets the attack class for a specific flow in the Elasticsearch index.

        Args:
            flow_id (str): The ID of the flow to update.
            attack_class (str): The attack class to set for the flow.

        Returns:
            None
        """
        async with AsyncElasticsearch(hosts=self.hosts, api_key=self.api_key, verify_certs=self.verify_certs, ssl_show_warn=False) as client:
            s = AsyncSearch(using=client, index=INDEX_NAME).query("match", flow_id=flow_id)
            async for hit in s:
                return await client.update(index=INDEX_NAME, refresh="wait_for", id=hit.meta.id, body={"doc": {"attack_class": attack_class}})

    async def store_flow_data(self, data:dict):
        # Initialize Elasticsearch client
        async with AsyncElasticsearch(
            self.hosts,
            api_key=self.api_key,  # Authentication via API-key
            verify_certs=False,
            ssl_show_warn=False,
            request_timeout=30,
            retry_on_timeout=True
        ) as client:
            # Send to Elasticsearch
            return await client.index(index=INDEX_NAME, body=data)
    
    async def get_pcap_data(self, flow_id: str):
        """
        Gets the PCAP Data for a specific flow in the Elasticsearch index.

        Args:
            flow_id (str): The ID of the flow to get the pcap data from.

        Returns:
            The PCAP Data in Base 64 
        """
        async with AsyncElasticsearch(hosts=self.hosts, api_key=self.api_key, verify_certs=self.verify_certs, ssl_show_warn=False) as client:
            s = AsyncSearch(using=client, index=INDEX_NAME).query("match", flow_id=flow_id)
            async for hit in s:
                resp =  await client.get(index=INDEX_NAME,id=hit.meta.id)
                return resp.body['_source']['pcap_data']

    async def save_model_properties(self, hash_value: str, timestamp, own_flow_count:int, score:float) -> str:
        # Initialize Elasticsearch client
        async with AsyncElasticsearch(
            self.hosts,
            api_key=self.api_key,  # Authentication via API-key
            verify_certs=False,
            ssl_show_warn=False,
            request_timeout=30,
            retry_on_timeout=True
        ) as client:
            # Send to Elasticsearch
            data = {
                "model_hash": hash_value,
                "score": score,
                "timestamp": timestamp,
                "own_flow_count": own_flow_count
            }
            resp =  await client.index(index=MODEL_INDEX_NAME, body=data)
            return resp["_id"]

    async def get_model_properties(self, id:str) -> dict:
        async with AsyncElasticsearch(
            self.hosts,
            api_key=self.api_key,  # Authentication via API-key
            verify_certs=False,
            ssl_show_warn=False,
            request_timeout=30,
            retry_on_timeout=True
        ) as client:
            # get from Elasticsearch
            resp =  await client.get(index=MODEL_INDEX_NAME, id=id)
            return resp.body
        
    async def get_all_model_properties(self, size:int=20):
        """
        Retrieves all model properties from Elasticsearch. 

        Args:
            size (int): The number of models to retrieve data from. If None all will be retrieved: Maximum is 10000 as this is set in elastic.

        Returns:
            list of dicts containing id, modelhash, score, own flow count and timestamp 
        """
        async def _get_all_model_properties(self, size):
            properties_list = []
            async with AsyncElasticsearch(hosts=self.hosts, api_key=self.api_key, verify_certs=self.verify_certs, ssl_show_warn=False) as client:
                if size:
                    s = AsyncSearch(using=client, index=MODEL_INDEX_NAME) \
                        .query("match_all") \
                        .extra(size=size) \
                        .sort({"timestamp": {"order": "desc"}})
                else: # size == None
                    s = AsyncSearch(using=client, index=MODEL_INDEX_NAME) \
                        .query("match_all") \
                        .extra(size=10000) \
                        .sort({"timestamp": {"order": "desc"}})
                async for hit in s:
                    properties_list.append(DataFrame([hit.to_dict()]))
                resulting_df = concat(properties_list)
                resulting_df['timestamp'] = to_datetime(resulting_df['timestamp'])
            return resulting_df
        return await _get_all_model_properties(self, size=size)

if __name__ == '__main__':
    # TODO remove as this for testing only
    # FLOWID = "56e58dfb-e260-44f5-9603-d7c22ed4f364"
    # API_KEY = "WU1uNldaUUJyMFU1enNoeW5PUFI6dWs5RHRUOHhUQ3FXd1B3Um43WG43Zw=="
    cec = CustomElasticsearchConnector()
    # flows = asyncio.run(cec.get_all_flows(onlyunseen=True))
    # #print(flows[0])
    # asyncio.run(cec.set_flow_as_seen(flow_id=FLOWID))
    # asyncio.run(cec.set_attack_class(flow_id=FLOWID, attack_class="BOT"))
    # flows1 = asyncio.run(cec.get_all_flows(onlyunseen=False))
    # #assert flows1[-2][FLOWID] == "BOT"
    # #assert flows1[-1][FLOWID] == "true"

    # print(len(flows1[0]))
    # print(len(flows[0]))
    # from elastic_transport import ConnectionError as ce
    # try:
    #     #model= asyncio.run(cec.get_all_model_properties(size=20))
    #     flows = asyncio.run(cec.get_all_flows(view="all", size=2))    
    #     print(flows)
    # except ce:
    #     print("Errorhandling")
    # pcap = asyncio.run(cec.get_pcap_data("2bb98524-e362-42bd-bcd4-b095423b7e14"))
    # print(pcap)
    # from datetime import datetime
    # import asyncio
    # cec = CustomElasticsearchConnector()
    # uuid = asyncio.run(cec.save_model_properties(hash_value="123456890", timestamp=datetime.now(), own_flow_count=10, score=0.99))
    # print(asyncio.run(cec.get_model_properties(uuid)))
    # print(asyncio.run(cec.get_all_model_properties()))
    x = asyncio.run(cec.get_all_flows(view="seen", size=10000))
    print(len(x))
    