from dash import Dash, html, dcc
from flask_login import current_user
from flask import redirect, url_for, request
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import os
import elasticsearch
import logging
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Loading of the .env file
load_dotenv()
# Elastic
ES_HOST = os.getenv("ES_HOST")  # Change this to your Elasticsearch host
ES_PORT = int(os.getenv("ES_PORT"))  # Change this to your Elasticsearch port
ES_INDEX = os.getenv("ES_INDEX")  # Index name for storing flow data
# Get these values from your Elasticsearch installation
ES_API_KEY = os.getenv("ES_API_KEY")  # API key for access to elastic
SENSOR_NAME = os.getenv("SENSOR_NAME")  # Unique name to identify this sensor


try:
    # Initialize Elasticsearch client
    es = Elasticsearch(
        f"{ES_HOST}:{ES_PORT}",
        api_key=ES_API_KEY,  # Authentication via API-key
        verify_certs=False,
        ssl_show_warn=False,
        request_timeout=30,
        retry_on_timeout=True,
    )

    # # Verify index exists
    # if not es.indices.exists(index=ES_INDEX):
    #     logger.error(f"Index {ES_INDEX} does not exist")
    #     raise Exception(f"Index {ES_INDEX} not found")

    # Build search query
    s = Search(using=es, index=ES_INDEX)

    # Debug: Print total documents in index
    response = s.execute()
    logger.debug(f"Total documents in index: {response.hits.total.value}")

    # Get sample document to verify structure
    sample = es.search(index=ES_INDEX, size=1)
    # logger.debug(f"Sample document structure: {sample['hits']['hits'][0] if sample['hits']['hits'] else 'No documents found'}")

    # Modify search to match your document structure
    s = (
        Search(using=es, index=ES_INDEX)
        .extra(size=10)
        .source(["id", "flow_data", "prediction"])
    )  # Specify fields to return

    response = s.execute()

    # Print results with more detail
    df_list = []
    for hit in response:
        logger.info(f"Document ID: {hit.meta.id}")
        logger.info(f"Source data: {hit.to_dict()}")
        df_list.append(pd.DataFrame([hit.to_dict()["prediction"]]))

    df = pd.concat(df_list)
    print(df)

except elasticsearch.AuthorizationException as e:
    print(f"Authorization error: {e}")
    print("Please check your API key permissions")
except elasticsearch.ConnectionError as e:
    print(f"Connection error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
