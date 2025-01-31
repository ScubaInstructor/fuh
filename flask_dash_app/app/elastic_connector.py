from elasticsearch import AsyncElasticsearch, AuthenticationException
from elasticsearch_dsl import AsyncSearch, connections
import asyncio
import pandas as pd
from elasticsearch.exceptions import AuthenticationException
INDEX_NAME = "network_flows" # TODO make this comnfigured from .env file 
MODEL_INDEX_NAME = "model_properties"

class CustomElasticsearchConnector:
    """
    A custom connector class for interacting with an Elasticsearch instance.

    Attributes:
        hosts (list): A list of Elasticsearch hosts.
        api_key (str): The API key for authentication.
        verify_certs (bool): Whether to verify SSL certificates.
    """

    def __init__(self, hosts=['https://localhost:9200'], api_key="VFFIcnM1UUJPWkFRTElWZUprWnA6TjJ4b1paS0RUOGlmVnhLNXQ1cUx0Zw==", verify_certs=False):
        """
        Initializes the CustomElasticsearchConnector.

        Args:
            hosts (list): A list of Elasticsearch hosts.
            api_key (str): The API key for authentication.
            verify_certs (bool): Whether to verify SSL certificates.
        """
        try:
            # Create connection
            connections.create_connection(
                hosts=hosts, 
                api_key=api_key, 
                verify_certs=verify_certs, 
                ssl_show_warn=False
            )
            
            # Test connection
            client = AsyncElasticsearch(
                hosts=hosts,
                api_key=api_key,
                verify_certs=verify_certs
            )
            
            # Run connection test
            if not asyncio.run(self._test_connection(client)):
                raise ConnectionError("Failed to connect to Elasticsearch")
                
            self.hosts = hosts
            self.api_key = api_key
            self.verify_certs = verify_certs
            
        except Exception as e:
            print(f"Elasticsearch connection failed: {e}")
            raise ConnectionError(f"Could not establish connection: {e}")

    async def _test_connection(self, client) -> bool:
        """Test if Elasticsearch connection is working."""
        try:
            await client.ping()
            return True
        except Exception:
            return False
        

    async def get_all_flows(self, view="all", size=10, include_pcap=False, flow_id=None):
        """
        Retrieves all flow documents from Elasticsearch. Optionally, only retrieves flows that have not been seen. Run with asyncio.run(get_all_flows())

        Args:
            view (str): all = all flows, seen = only seen flows, unseen = only unseen flows.
            size (int): The number of flows to retrieve.
            include_pcap (bool): Whether to include the pcap_data field in the results

        Returns:
            Dataframe containing the requested flows.
        """
        async def _get_all_flows(self, view="all", size=10, include_pcap=False, flow_id=None):
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
                
                df = pd.concat(df_list)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                # Convert string to boolean
                df['has_been_seen'] = df['has_been_seen'].replace('true', True)
                return df
            
        return await _get_all_flows(self, view=view, size=size, include_pcap=include_pcap, flow_id=flow_id)
    
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
    FLOWID = "2d980e5c-c998-4707-8b94-86eeb4a1ac81"
    API_KEY = "WU1uNldaUUJyMFU1enNoeW5PUFI6dWs5RHRUOHhUQ3FXd1B3Um43WG43Zw=="
    
    cec = CustomElasticsearchConnector()
    
    try:
        df = asyncio.run(cec.get_all_flows(size=10, include_pcap=True))
    except Exception as e:
        print(e)
    # #asyncio.run(cec.set_flow_as_seen(flow_id=FLOWID))
    # asyncio.run(cec.set_attack_class(flow_id=FLOWID, attack_class="BOT"))
    # flows1 = asyncio.run(cec.get_all_flows(view="seen"))
    # flows2 = asyncio.run(cec.get_all_flows(view="unseen"))
    # #assert flows1[-2][FLOWID] == "BOT"
    # #assert flows1[-1][FLOWID] == "true"

    # print(len(flows1))
    # print(len(flows2))

    # flows = asyncio.run(cec.get_all_flows(view=True, size=2))
    # print(len(flows))

