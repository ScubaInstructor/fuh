import asyncio
import hashlib
from os import getenv, makedirs
import os
from shutil import copyfile
import zipfile
from dotenv import load_dotenv
from elasticsearch import AsyncElasticsearch
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import joblib


from .elastic_connector import CustomElasticsearchConnector
from .modelhash_container import Modelhash_Container
# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
# Create Flask app
app = Flask(__name__)
APPPATH = "app/"
MODELPATH = "models/"
ZIPFILENAME = "model_scaler_ipca.zip"
MODELNAME = "model.pkl"
SCALERNAME = "scaler.pkl"
IPCANAME = "ipca.pkl"
MODELARCHIVEPATH = MODELPATH + "old_models"

# Initialize Elasticsearch connector and get data
cec = CustomElasticsearchConnector()
mc = Modelhash_Container(APPPATH+MODELPATH+MODELNAME)

def create_app():
    load_dotenv(dotenv_path="/dash/.env")
    app.secret_key = getenv('YOUR_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from .routes import main_routes
    from .auth import auth_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)

    # Initialize Dash app
    from .dash_app import init_dash_app
    init_dash_app(app)

    return app



async def load_initial_model_metrics_to_elastic() -> str:
    load_dotenv(dotenv_path="/usr/share/elasticsearch/.env") 
    HOSTS = ['https://es01:9200']
    MODEL_INDEX_NAME = getenv("MODEL_DATA_INDEX_NAME")

    load_dotenv(dotenv_path="/shared_secrets/server-api-key.env")
    API_KEY = getenv("ELASTIC_SERVER_KEY") 
    data = joblib.load(APPPATH+MODELPATH+"dict_with_initial_model_data.pkl")
    async with AsyncElasticsearch(
                HOSTS,
                api_key=API_KEY,  # Authentication via API-key
                verify_certs=False,
                ssl_show_warn=False,
                request_timeout=30,
                retry_on_timeout=True
            ) as client:
        resp = await client.index(index=MODEL_INDEX_NAME, body=data)
        return resp["_id"]

# upload initial model metrics to elasti, if this is the first startup
file_path = '/shared_secrets/upload_initial_model_metrics'
if os.path.exists(file_path):
    print("this is the first startup! I will upload the metrics of the initial model to elastic")
    elastic_id = asyncio.run(load_initial_model_metrics_to_elastic())
    files = [APPPATH +MODELPATH + MODELNAME, APPPATH +MODELPATH + SCALERNAME, APPPATH +MODELPATH + IPCANAME]
    
    # to store old models
    makedirs(APPPATH +MODELARCHIVEPATH, exist_ok = True)

    # create zipfile
    zf = zipfile.ZipFile("" + APPPATH +MODELPATH + ZIPFILENAME, "w")

    for f in files:
        # write file to zip
        zf.write(f)
    zf.close()
    # Copy the model to archive with the name of the ip of the elastic document
    copyfile(zf.filename, f"{APPPATH + MODELARCHIVEPATH}/{elastic_id}.zip")
    print(f"Deleting flag file: {file_path}")
    os.remove(file_path)


def restore_model_to_previous_version(elastic_id:str, mc: Modelhash_Container) -> None | FileNotFoundError:
    """ Extract the model with the specified id from the respective file in the archive folder and replace the current model.

    Args:
        elastic_id (str): the uuid for the model which should be used by the sensors from now on. 
    Returns:
        None if everything goes well or FileNotFoundError if the file doesn't exist
    
    """
    try:
        copyfile(f"{APPPATH + MODELARCHIVEPATH}/{elastic_id}.zip", APPPATH + MODELPATH + ZIPFILENAME)
        zf = zipfile.ZipFile(APPPATH + MODELPATH + ZIPFILENAME, "r")
        zf.extract(member=MODELNAME, path=APPPATH + MODELPATH)
        mc.set_hash(mc.compute_file_hash( APPPATH + MODELPATH + MODELNAME))
    except FileNotFoundError:
        print("Requested File not found")
        raise FileNotFoundError

         
def remove_model_zip_file_from_disk(elastic_id:str) -> bool:
    """remove the zipfile to this elastic uuid from filesystem.

    Args:
        elastic_id (str): the filename of the model to remove zipfile from
    Returns:
        bool: Success or no success
    """
    try:
        os.remove(f"{APPPATH + MODELARCHIVEPATH}/{elastic_id}.zip")
        return True
    except FileNotFoundError as fne:
        print(fne)
        return False