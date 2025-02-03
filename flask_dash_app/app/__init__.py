import hashlib
from os import getenv
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
# Create Flask app
app = Flask(__name__)
MODELNAME = "flask_dash_app/models/model.pkl"
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
