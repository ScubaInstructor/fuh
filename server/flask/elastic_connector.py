from elasticsearch import Elasticsearch
from elasticsearch_dsl import AsyncSearch, async_connections
import asyncio


def get_all_unseen_flows(hosts=['https://localhost:9200'], api_key="OU4xeVFaUUJSV1RkZXBRSHpXczQ6SGUwRzFhSDZUN0Njc3JMYVNUekttUQ==", verify_certs=False):
    async_connections.create_connection(hosts=hosts, api_key=api_key, verify_certs=verify_certs)
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

    async def get_unseen_flows():
        s = AsyncSearch(index="network_flows") \
            .query("match", has_been_seen="false")   \
            #.filter("term", category="search") \
            #.exclude("match", description="beta")
        async for hit in s:
            id = hit.id
            dataframes[id] = hit.flow_data
            #partner_ips[id] = hit.partner_ip
            sensor_names[id] = hit.sensor_name
            predictions_store[id] = hit.prediction
            probabilities_store[id] = hit.probabilities
            #partner_ips[id] = hit.partner_ip        # TODO set in Sensor
            #partner_ports[id] = hit.partner_port    # TODO set in Sensor
            #sensor_ports[id] = hit.sensor_port      # TODO set in Sensor
            timestamps[id] = hit.timestamp
            has_been_seen[id] = hit.has_been_seen
            #attack_classes[id] = hit.attack_class   # TODO set in Sensor
            #filestore[id] = hit.pcap_data           # TODO set in Sensor
        return dataframes, filestore, probabilities_store, predictions_store, sensor_names, timestamps, sensor_ports, partner_ips, partner_ports, attack_classes, has_been_seen
        #return dataframes,sensor_names,timestamps,has_been_seen,predictions_store,probabilities_store

    return asyncio.run(get_unseen_flows())

#dataframes, filestore, probabilities_store, predictions_store, sensor_names, timestamps, sensor_ports, partner_ips, partner_ports, attack_classes, has_been_seen  = get_all_unseen_flows()
a,b,c,d,e,f,g,h,i,j,k = get_all_unseen_flows()
print(b)