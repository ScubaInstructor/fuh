from pathlib import Path
from flask import Blueprint, jsonify, render_template, redirect, request, send_file
from flask_login import login_required, current_user
import jwt
from . import db, app, MODELNAME, MODELPATH, ZIPFILENAME, mc, cec
#from elastic_connector import CustomElasticsearchConnector, API_KEY, INDEX_NAME
import asyncio
from flask import current_app
from .models import Sensor

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

@main_routes.route('/upload', methods=['POST'])
def upload():
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
        # check if request is well formed
        if ('flow_data' in request.json and 
                'pcap_data' in request.json and 
                'probabilities' in request.json  and 
                'timestamp' in request.json and 
                'prediction' in request.json and 
                'sensor_name' in request.json and
                'sensor_port' in request.json and
                'partner_ip' in request.json and
                'partner_port' in request.json and
                'has_been_seen'in request.json and
                'attack_class'in request.json and
                'flow_id' in request.json and
                'model_hash'in request.json):
            
            
            # check if hash is valid     
            sensor_hash = request.json["model_hash"]
            print("Sensorhash: " + sensor_hash)
            #global modelhash 
            print("Serverhash: " + mc.get_hash())
            if mc.get_hash() != sensor_hash:
                return jsonify({"update_error": "Model is out of date!"}), 400
            # receive data and store it in elastic
            doc = request.json
            asyncio.run(cec.store_flow_data(data=doc))
            
            #  Discord notification to do 
            # if NOTIFICATION_ACTIVE:
            #     notify_users() 
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
        if Path("app/" + filename).is_file():
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
