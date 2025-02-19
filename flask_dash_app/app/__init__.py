import hashlib
from os import getenv
import os
from shutil import copyfile
import zipfile
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


from .elastic_connector import CustomElasticsearchConnector
from .modelhash_container import Modelhash_Container
# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
# Create Flask app
app = Flask(__name__)
APPPATH = "flask_dash_app/app/"
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
    load_dotenv()
    app.secret_key = getenv('your_secret_key')
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

# def compute_file_hash(file_path: str) -> str: # DEPRECATED as it is now in Container class
#         """Compute the hash of a file using the sha265 algorithm.
        
#         Args:
#             - file_path (str) = the path to the file
        
#         Returns:
#             str: The hash value
#         """
#         hash_func = hashlib.sha256()
#         with open(file_path, 'rb') as file:
#             # Read the file in chunks of 8192 bytes
#             while chunk := file.read(8192):
#                 hash_func.update(chunk)
        
#         return hash_func.hexdigest()

def restore_model_to_previous_version(elastic_id:str, mc: Modelhash_Container) -> None | FileNotFoundError:
    """ Extract the model, scaler and ipca with the specified model id from the respective file 
    in the archive folder and replace the current files.

    Args:
        elastic_id (str): the uuid for the model which should be used by the sensors from now on. 
    Returns:
        None if everything goes well or FileNotFoundError if the file doesn't exist
    
    """
    try:
        copyfile(f"{APPPATH + MODELARCHIVEPATH}/{elastic_id}.zip", APPPATH + MODELPATH + ZIPFILENAME)
        zf = zipfile.ZipFile(APPPATH + MODELPATH + ZIPFILENAME, "r")
        zf.extractall(path=APPPATH + MODELPATH)
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