from pathlib import Path
from flask import Blueprint, jsonify, render_template, redirect, request, send_file
from flask_login import login_required, current_user
import jwt
from . import db, app,APPPATH, MODELNAME, MODELPATH, SCALERNAME, IPCANAME, ZIPFILENAME, mc, cec
#from elastic_connector import CustomElasticsearchConnector, API_KEY, INDEX_NAME
import asyncio
import pandas as pd
from joblib import load
from flask import current_app
from datetime import datetime, timedelta
from .models import Sensor
from .pipelining_utilities import adapt_for_prediction
import dotenv
from os import getenv
from .discord_bot import DiscordClient


# Discord stuff
dotenv.load_dotenv(dotenv_path="flask_dash_app/.env") 
DISCORD_NOTIFICATION_DELAY = 1 # number of hours for timedelay between notifications
TOKEN = getenv('DISCORD_TOKEN')
CHANNEL_ID = int(getenv('DISCORD_CHANNEL_ID'))
discord_client = DiscordClient(channel_id=CHANNEL_ID)
NOTIFICATION_ACTIVE = getenv('NOTIFICATION_ACTIVE') == '1'
last_notification = datetime.now() - timedelta(hours=DISCORD_NOTIFICATION_DELAY)

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
@login_required
def home():
    return redirect('/inbox/')

@main_routes.route('/inbox')
@login_required
def dashboard():
    print(f"User authenticated: {current_user.is_authenticated}")  # Debugging
    #return render_template('dashboard.html', username=current_user.username)
    return redirect('/inbox/')


@main_routes.route('/get_model_hash', methods=['GET'])
def get_model_hash():
    # check auth
    token = request.headers.get('Authorization').split()[1]
    
    try:
        payload = jwt.decode(token, app.secret_key, options={"verify_exp": False} , algorithms=['HS256'])
        # Check if sensor name is known
        sensor_name = payload['user_id']
        with current_app.app_context():
            registered_sensors = Sensor.query.all()
            reg_sensor_names = [sensor.name for sensor in registered_sensors]
            if sensor_name not in reg_sensor_names:
                return jsonify({"error": "Sensor doesn't exists"}), 401
    except jwt.ExpiredSignatureError: # Not in use TODO check if neccessary
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    # Everything is well and we return the hash
    # TODO insert hash and add the respective functions and variables
    return jsonify({'message': 'Access granted', 'model_hash': mc.get_hash()})

def notify_users():
    global last_notification
    if last_notification < datetime.now() - timedelta(hours=DISCORD_NOTIFICATION_DELAY):
        discord_client.run(token=TOKEN)
        last_notification = datetime.now()

@main_routes.route('/upload', methods=['POST'])
def upload():
    # Route where unclassified Flows and PCAP Data is sent to

    # Instantiate model parameters
    model = load(APPPATH + MODELPATH + MODELNAME)
    scaler = load(APPPATH + MODELPATH + SCALERNAME)
    ipca = load(APPPATH + MODELPATH + IPCANAME)

    # Sensor Authentification
    #token = request.headers.get('Authorization').split()[1]
    token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(token, app.secret_key, options={"verify_exp": False} , algorithms=['HS256'])
        # Check if sensor name is known
        sensor_name = payload['user_id']
        with current_app.app_context():
            registered_sensors = Sensor.query.all()
            reg_sensor_names = [sensor.name for sensor in registered_sensors]
            if sensor_name not in reg_sensor_names:
                return jsonify({"error": "Sensor doesn't exists"}), 401
        # check if request is well formed

        if ('flow_data' in request.json and 
                'pcap_data' in request.json and 
                'timestamp' in request.json and 
                'sensor_name' in request.json and
                'src_prt' in request.json and
                'src_ip' in request.json and
                'dst_prt' in request.json and
                'dst_ip' in request.json and
                'flow_id' in request.json):
            
            doc = request.json
            # remove flow_ex not needed
            doc.pop('flow_ex', None)
            # adapt for prediction
            flow_data = pd.DataFrame([request.json['flow_data']])
            flow_data = adapt_for_prediction(flow_data,scaler,ipca,34)

            # # predict
            prediction = model.predict(flow_data)
            
            # # get probabilites
            proba = model.predict_proba(flow_data)

            # prepare the dict with the probabilities

            probabilities = {}

            for i in range(len(proba[0])):
                probabilities[model.classes_[i]] = proba[0][i]
            
            # Prepare dict for upload
            doc.update({
                        'prediction': prediction.tolist()[0],
                        'probabilities': probabilities,
                        'attack_class': "not yet classified",
                        'has_been_seen': False, # TODO Is this redundant, if we have the attack_class field?
                        'flow_data': request.json["flow_data"],
                        'model_hash' : mc.get_hash()
                    })  
            # receive data and store it in elastic
            #doc = request.json

            timestamp = datetime.strptime(doc['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            doc['timestamp'] = timestamp.isoformat()


            asyncio.run(cec.store_flow_data(data=doc))
            
            #  Discord notification to do 
            if NOTIFICATION_ACTIVE:
                notify_users() 
        else:
            return jsonify({"error": "Malformed data"}), 400

    except jwt.ExpiredSignatureError: # Not in use TODO check if neccessary
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    return jsonify({'message': 'Access granted', 'user_id': payload['user_id']})

@main_routes.route('/get_latest_model')
def get_latest_model():
    # check auth
    token = request.headers.get('Authorization').split()[1]
    try:
        payload = jwt.decode(token, app.secret_key, options={"verify_exp": False} , algorithms=['HS256'])
        # Check if sensor name is known
        sensor_name = payload['user_id']
        with current_app.app_context():
            registered_sensors = Sensor.query.all()
            reg_sensor_names = [sensor.name for sensor in registered_sensors]
            if sensor_name not in reg_sensor_names:
                return jsonify({"error": "Sensor doesn't exists"}), 401
        filename = MODELPATH + ZIPFILENAME  
        if Path("flask_dash_app/app/" + filename).is_file():    # TODO this will be different in Dockercontainer
            return send_file(
                filename,
                as_attachment=True,
                download_name=ZIPFILENAME 
            )
        return "File not found", 404
    except jwt.ExpiredSignatureError: # Not in use TODO check if neccessary
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
