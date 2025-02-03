import hashlib
from os import getenv
from shutil import copyfile
import zipfile
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from joblib import dump

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
# Create Flask app
app = Flask(__name__)
MODELPATH = "flask_dash_app/models/"
ZIPFILENAME = "model_scaler_ipca.zip"
MODELNAME = "model.pkl"
MODELARCHIVEPATH = MODELPATH + "old_models"
model_hash:str = "" # the hash of the current model 


def create_app():
    load_dotenv()
    app.secret_key = getenv('your_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
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
    restore_model_to_previous_version("test")
    return app

def compute_file_hash(file_path: str) -> str:
        """Compute the hash of a file using the sha265 algorithm.
        
        Args:
            - file_path (str) = the path to the file
        
        Returns:
            str: The hash value
        """
        hash_func = hashlib.sha256()
        with open(file_path, 'rb') as file:
            # Read the file in chunks of 8192 bytes
            while chunk := file.read(8192):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()

def restore_model_to_previous_version(elastic_id:str) -> None | FileNotFoundError:
    """ Extract the model with the specified id from the respective file in the archive folder and replace the current model.

    Args:
        elastic_id (str): the uuid for the model which should be used by the sensors from now on. 
    Returns:
        None if everything goes well or FileNotFoundError if the file doesn't exist
    
    """
    global model_hash
    try:
        copyfile(f"{MODELARCHIVEPATH}/{elastic_id}.zip", MODELPATH + ZIPFILENAME)
        zf = zipfile.ZipFile(MODELPATH + ZIPFILENAME, "r")
        zf.extract(member=MODELNAME, path=MODELPATH)
        model_hash = compute_file_hash(MODELPATH + MODELNAME)
    except FileNotFoundError:
        print("Requested File not found")
        raise FileNotFoundError