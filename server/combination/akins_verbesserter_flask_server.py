import asyncio
from base64 import b64decode, b64encode
from datetime import datetime, timedelta, timezone
import hashlib
from pathlib import Path
from flask import Flask, request, jsonify, send_file, redirect, url_for, send_from_directory, flash,render_template
from io import BytesIO
import jwt
import matplotlib.pyplot as plt
from os.path import abspath, join
from os import getcwd, getenv, path, chmod
from geoip2fast import GeoIP2Fast, geoip2fast
import matplotlib
from time import sleep
from threading import Thread
from elastic_connector import CustomElasticsearchConnector, API_KEY, INDEX_NAME
from discord_bot import DiscordClient
from dotenv import load_dotenv
from retrainer import retrain

matplotlib.use('Agg') 
load_dotenv()


from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from forms import LoginForm

app = Flask(__name__)
SQLITE_PATH = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_PATH 
app.config['SECRET_KEY'] = getenv('YOUR_SECRET_KEY')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

global modelhash
modelhash: str = "" # the hash of the current model
global last_notification
last_notification = datetime.now()

# Discord stuff
DISCORD_NOTIFICATION_DELAY = 1 # number of hours for timedelay between notifications
TOKEN = getenv('DISCORD_TOKEN')
CHANNEL_ID = int(getenv('DISCORD_CHANNEL_ID'))
discord_client = DiscordClient(channel_id=CHANNEL_ID)
NOTIFICATION_ACTIVE = getenv('NOTIFICATION_ACTIVE') == '1'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    salt = db.Column(db.String(150), nullable=False)  # Salt for the password

# CReate the user database
with app.app_context():
    db.create_all()

def generate_env_file_for_sensors(user_id):
    '''
    Create an .env File for useage in the sensors, containing the JWT token and the elastic api key
    '''
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(seconds=1)
    }
    token = jwt.encode(payload, app.secret_key, algorithm='HS256')
    FLASK_PORT_NUMBER = getenv('FLASK_PORT_NUMBER')
    header_text="""# LOCAL CONFIGURATION 
SNIFFING_INTERFACE="" # This can be set to a specific network interface to listen to, else all interfaces are listened to 
DEBUGGING="1"   # Sends all Flows to server and be more noisy
SENSOR_NAME="Sensor"  # choose a meaningful name to identify this sensor

"""
    flask_line = f"""
# FLASK SERVER CONFIGURATION
SERVER_URL = \"http://localhost:{FLASK_PORT_NUMBER}\"\n"""
    token_line = f"SERVER_TOKEN = \"{token}\""
    filename = "/keys/.env"
    with open(filename, "w+") as f:
        f.write(header_text)    
        f.write(flask_line)
        f.write(token_line)
    chmod(filename, 0o776)
    print(f"{filename} file generated and written.\n")

def notify_users():
    global last_notification
    if last_notification < datetime.now() - timedelta(hours=DISCORD_NOTIFICATION_DELAY):
        discord_client.run(token=TOKEN)
        last_notification = datetime.now()

# Dictionaries to store dataframes, files, probabilities, predictions and timestamps with unique IDs
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
flow_ids = []   # Log for storing request information


try: 
    G = GeoIP2Fast(verbose=False)   
except geoip2fast.GeoIPError as ge:
    print(ge)
    G = False      
def update_geoip_database():
    global G
    while True:
        if not G:
            try: 
                G = GeoIP2Fast(verbose=False)   
                return
            except geoip2fast.GeoIPError as ge:
                print(ge)
                G = False
        else:     
            err = G.update_all()
            errors = [e['error'] == None for e in err]
            if all(errors):
                print("Geo IP database update complete.")
            else: 
                print("Geo IP database update failed.")
        sleep(4 * 60 * 60)  # Sleep for 4 hours

# Start the GeoIP database update in a separate thread
Thread(target=update_geoip_database, daemon=True).start()

CEC = CustomElasticsearchConnector() # run with standard ports and host


static_path = abspath(join(getcwd(), 'static/'))

def update_the_flowstore():
    global flow_ids, dataframes, filestore, probabilities_store, predictions_store, sensor_names, timestamps, sensor_ports, partner_ips, partner_ports, attack_classes, has_been_seen
    flow_ids, dataframes, filestore, probabilities_store, predictions_store, sensor_names, timestamps, sensor_ports, partner_ips, partner_ports, attack_classes, has_been_seen = asyncio.run(CEC.legacy_get_all_flows(onlyunseen=False))

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

def set_the_server_hash(filename:str):
    """
    set the current value of the hash of the model in global variable modelhash

    Args:
        filename (str): the filename of the model
    """
    global modelhash
    modelhash = compute_file_hash(filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create an instance of the form
    if form.validate_on_submit():  # Check if the form is submitted and valid, including CSRF
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password + user.salt): 
            login_user(user)
            return redirect(url_for('index'))  
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)  # Pass the form to the template

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/get_model_hash', methods=['GET'])
def get_model_hash():
    # check auth
    token = request.headers.get('Authorization').split()[1]
    try:
        payload = jwt.decode(token, app.secret_key, options={"verify_exp": False} , algorithms=['HS256'])
    except jwt.ExpiredSignatureError: # Not in use TODO check if neccessary
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    return jsonify({'message': 'Access granted', 'model_hash': modelhash})


@app.route('/upload', methods=['POST'])
def upload():
    # check auth
    token = request.headers.get('Authorization').split()[1]
    try:
        payload = jwt.decode(token, app.secret_key, options={"verify_exp": False} , algorithms=['HS256'])

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
            global modelhash 
            print("Serverhash: " + modelhash)
            if modelhash != sensor_hash:
                return jsonify({"update_error": "Model is out of date!"}), 400

            # receive data and store it in elastic
            doc = request.json
            asyncio.run(CEC.store_flow_data(data=doc))

            if NOTIFICATION_ACTIVE:
                notify_users() 
        else:
            return jsonify({"error": "Malformed data"}), 400

    except jwt.ExpiredSignatureError: # Not in use TODO check if neccessary
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    return jsonify({'message': 'Access granted', 'user_id': payload['user_id']})

@app.route('/')
@login_required
def index():
    current_time = datetime.now()
    timestamps_list = []
    counts = []
    update_the_flowstore()
    # get the relevant timestamps 
    for entry in flow_ids:
        entry_time = datetime.strptime(timestamps[entry], '%Y-%m-%dT%H:%M:%S.%f')
        if current_time - entry_time <= timedelta(minutes=60):
            timestamps_list.append(entry_time)
            counts.append(1)
        

    # create a list of timestamps and counters
    time_bins = [current_time - timedelta(minutes=i) for i in range(60)]
    count_bins = [0] * 60

    for timestamp in timestamps_list:
        for i in range(60):
            if timestamp >= (current_time - timedelta(minutes=i + 1)) and timestamp < (current_time - timedelta(minutes=i)):
                count_bins[i] += 1

    # Create barchart
    plt.figure(figsize=(10, 2))
    plt.bar(time_bins[::-1], count_bins[::-1], width=0.0005)  # Set width for better visualisation
    plt.xlabel('Timestamps')
    plt.ylabel('Count of Flows')
    plt.title('Last 60 Minutes')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the image
    
    plt.savefig(join(static_path,'timeline_chart.png'))  # TODO make more consistent! Path must exist!
    plt.close()

    # Generate HTML content for all available timestamps with sensor names and predictions in a table format
    return render_template('index.html', requests=[{
        'timestamp': timestamps[entry],
        'sensor_name': sensor_names[entry],
        'prediction': predictions_store[entry],
        'attack_class': attack_classes.get(entry, None),
        'dataframe_id': entry
    } for entry in flow_ids], has_been_seen=has_been_seen)



@app.route('/details/<id>', methods=['GET', 'POST'])
@login_required
def details(id):
    global G
    update_the_flowstore()
    if id not in flow_ids:
        return "DataFrame not found", 404
    
    # The Submit button for classification
    if request.method == 'POST':
        if request.form['submit_button'] == "classify":
            selected_attack_class = request.form.get('selected_attack_class')

            # If it is an newly created class
            if selected_attack_class == "NEW_CLASS":
                new_class_name = request.form.get('new_class_name')
                selected_attack_class = new_class_name
            # attack_classes[id] = selected_attack_class
            # has_been_seen[id] = True
            asyncio.run(CEC.set_attack_class(flow_id=id, attack_class=selected_attack_class))
            asyncio.run(CEC.set_flow_as_seen(flow_id=id))
            # add new class to all unseen flows for possible prediction
            for entry in flow_ids:
                if has_been_seen[entry] == False:
                    unseen_flow_probabilities: dict = probabilities_store[entry]
                    unseen_flow_probabilities[selected_attack_class] = -1 # -1 prevents from being shown in the piechart!

            return redirect(url_for('index'))
        if request.form['submit_button'] == 'logout':
            return redirect(url_for('logout'))


    probabilities = probabilities_store.get(id, {})
    prediction = predictions_store.get(id, '')
    sensor_name = sensor_names.get(id, '')
    timestamp = timestamps.get(id, '')
    sensor_port = sensor_ports.get(id, '')
    partner_ip = partner_ips.get(id, '')
    partner_port = partner_ports.get(id, '')

    # Get the associated file ID to create a download link
    file_entry = filestore[id]
    file_download_link = f"/download/{id}" if file_entry else "#"

    # Create the flag for the ip-address
    if not G:
        try:
            G = GeoIP2Fast(verbose=False,)
        except geoip2fast.GeoIPError as ge:
            print(ge)
    if not G: 
        private_ip = True   #maybe not correct, but we can't lookup right now
        flag_country_code = "de" # just to set it 
    else:        
        ip_lookup = G.lookup(partner_ip)
        private_ip = ip_lookup.is_private
        flag_country_code = ip_lookup.country_code
        flag_country_name = ip_lookup.country_name
    
    return render_template('details.html', 
        probabilities=probabilities,
        prediction=prediction,
        sensor_name=sensor_name,
        timestamp=timestamp,
        file_download_link=file_download_link,
        sensor_port=sensor_port,
        partner_ip=partner_ip,
        partner_port=partner_port,
        flag_country_code=flag_country_code.lower(),
        private_ip=private_ip, # If Country flag must be used
        flag_country_name=flag_country_name # If Country flag must be used
        )



@app.route('/retrain')
@login_required
def retrain_button_pushed():
    stats = retrain()
    set_the_server_hash("model.pkl")
    print(stats)
    print("DEBUG: Button pushed")
    return redirect(url_for('index'))  # Back to index

@app.route('/download/<file_id>')
@login_required
def download_file(file_id):
    if file_id in filestore:
        return send_file(
            BytesIO(b64decode(filestore[file_id])),
            as_attachment=True,
            download_name=f"flow.pcap"  
        )
    return "File not found", 404

@app.route('/get_latest_model')
def get_latest_model():
    # check auth
    token = request.headers.get('Authorization').split()[1]
    try:
        jwt.decode(token, app.secret_key, options={"verify_exp": False} , algorithms=['HS256'])
        filename = "model_scaler_ipca.zip"
        if Path(filename).is_file():
            return send_file(
                filename,
                as_attachment=True,
                download_name=f"model_scaler_ipca.zip"  
            )
        return "File not found", 404
    except jwt.ExpiredSignatureError: # Not in use TODO check if neccessary
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

@app.route('/classified_requests')
@login_required
def classified_requests():
    # HTML for classified Flows
    return render_template('classified_requests.html', requests=[{
            'timestamp': timestamps[entry],
            'sensor_name': sensor_names[entry],
            'prediction': predictions_store[entry],
            'attack_class': attack_classes.get(entry, None),
            'dataframe_id': entry
        } for entry in flow_ids], has_been_seen=has_been_seen)


if __name__ == '__main__':
    generate_env_file_for_sensors("sensors")
    set_the_server_hash("datasources/model.pkl")
    print(f"modelhash is now {modelhash}")
    last_notification = datetime.now() - timedelta(hours=DISCORD_NOTIFICATION_DELAY)
    app.run(debug=True, host="0.0.0.0", port=8888)
