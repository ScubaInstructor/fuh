from dotenv import load_dotenv
import jwt
from os import getcwd, getenv, path, chmod
from datetime import datetime, timedelta, timezone
from flask import current_app

# Access secret key using current_app
def get_secret_key():
    with current_app.app_context():
        return current_app.secret_key

def generate_env_file_for_sensors(user_id):
    '''
    Create an .env File for useage in the sensors, containing the JWT token and the elastic api key
    '''
    key = get_secret_key()
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(seconds=1)
    }
    token = jwt.encode(payload, key, algorithm='HS256')
    load_dotenv(dotenv_path="/dash/.env")
    FLASK_PORT_NUMBER = getenv('FLASK_PORT_NUMBER')
    header_text=f'''# LOCAL CONFIGURATION 
SNIFFING_INTERFACE="" # This can be set to a specific network interface to listen to, else all interfaces are listened to 
DEBUGGING="1"   # Sends all Flows to server and be more noisy
SENSOR_NAME="{user_id}"  # choose a meaningful name to identify this sensor

'''
    flask_line = f"""
# FLASK SERVER CONFIGURATION
SERVER_URL = \"http://localhost:{FLASK_PORT_NUMBER}\"\n"""
    token_line = f"SERVER_TOKEN = \"{token}\""
    env_content = header_text + flask_line + token_line

    # filename = "/keys/.env"
    # with open(filename, "w+") as f:
    #     f.write(header_text)    
    #     f.write(flask_line)
    #     f.write(token_line)
    # chmod(filename, 0o776)
    #print(f"{filename} file generated and written.\n")
    return env_content