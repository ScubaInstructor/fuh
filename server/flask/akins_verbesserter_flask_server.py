from base64 import b64decode
from datetime import datetime, timedelta
import glob
from flask import Flask, request, render_template_string, jsonify, send_file, redirect, url_for, send_from_directory, flash,render_template
import uuid
from io import BytesIO
import json
import matplotlib.pyplot as plt
from os.path import abspath, join
from os import getcwd, getenv
from geoip2fast import GeoIP2Fast
from flagpy import get_flag_img
import matplotlib
from time import sleep
from threading import Thread
from elastic_connector import get_all_unseen_flows, set_flow_as_seen
from dotenv import load_dotenv
matplotlib.use('Agg') 
load_dotenv()


from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from forms import LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' 
app.config['SECRET_KEY'] = getenv('your_secret_key')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    salt = db.Column(db.String(150), nullable=False)  # Salt for the password

# CReate the user database
with app.app_context():
    db.create_all()

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


G = GeoIP2Fast(verbose=False)
def update_geoip_database():
    while True:
        err = G.update_all()
        errors = [e['error'] == None for e in err]
        if all(errors):
            print("Geo IP database update complete.")
        else: 
            print("Geo IP database update failed.")
        sleep(4 * 60 * 60)  # Sleep for 4 hours

# Start the GeoIP database update in a separate thread
Thread(target=update_geoip_database, daemon=True).start()

static_path = abspath(join(getcwd(), 'static/'))

def update_the_flowstore():
    global flow_ids, dataframes, filestore, probabilities_store, predictions_store, sensor_names, timestamps, sensor_ports, partner_ips, partner_ports, attack_classes, has_been_seen
    flow_ids, dataframes, filestore, probabilities_store, predictions_store, sensor_names, timestamps, sensor_ports, partner_ips, partner_ports, attack_classes, has_been_seen = get_all_unseen_flows()

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


# @app.route('/upload', methods=['POST'])
# def upload():
#     if ('file' in request.files and 
#             'json' in request.files and 
#             'probabilities' in request.files  and 
#             'timestamp' in request.files and 
#             'prediction' in request.files and 
#             'sensor_name' in request.files and
#             'sensor_port' in request.files and
#             'partner_ip' in request.files and
#             'partner_port' in request.files):
#         # Process both file and JSON data
#         file = request.files['file']
#         json_data = json.loads(request.files['json'].read().decode('utf-8'))
#         probabilities_data = json.loads(request.files['probabilities'].read().decode('utf-8'))
#         timestamp_data = json.loads(request.files['timestamp'].read().decode('utf-8'))
#         prediction = request.files['prediction'].read().decode('utf-8')
#         sensor_name = request.files['sensor_name'].read().decode('utf-8')
#         sensor_port = request.files['sensor_port'].read().decode('utf-8')
#         partner_ip = request.files['partner_ip'].read().decode('utf-8')
#         partner_port = request.files['partner_port'].read().decode('utf-8')
#         # Generate unique IDs
#         file_id = str(uuid.uuid4())
#         df_id = str(uuid.uuid4())

#         # Store file content
#         filestore[file_id] = file.read()

#         # Store JSON data 
#         dataframes[df_id] = json_data

#         # Store probabilities, predictions, sensor names, timestamp and has_been_seen
#         probabilities_store[df_id] = probabilities_data
#         predictions_store[df_id] = prediction
#         sensor_names[df_id] = sensor_name
#         timestamps[df_id] = timestamp_data['timestamp']  # Store the timestamp
#         sensor_ports[df_id] = sensor_port
#         partner_ips[df_id] = partner_ip
#         partner_ports[df_id] = partner_port

#         # Initialize has_been_seen for this ID to False
#         has_been_seen[df_id] = False

#         # Log the request
#         requests_log.append({'file_id': file_id, 'dataframe_id': df_id})

#         return jsonify({"file_id": file_id, "dataframe_id": df_id})
#     else:
#         return jsonify({"error": "Missing file or JSON data"}), 400


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
            attack_classes[id] = selected_attack_class
            has_been_seen[id] = True
            set_flow_as_seen(id)
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
    ip_lookup = G.lookup(partner_ip)
    private_ip = ip_lookup.is_private
    flag_country_code = ip_lookup.country_code
    flag_country_name = ip_lookup.country_name
    # found = False
    # for file in glob.glob("*.png"):
    #     if file.split('.')[0] == flag_country_code:
    #         found = True
    #         break
    # if not found:
    #     if not ip_lookup.is_private:
    #         flag = get_flag_img(ip_lookup.country_name)
    #         flag_path = f'{static_path}/{ip_lookup.country_code}.png'
    #         flag.save(flag_path)
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
def some_function():
    classified_ids = [i for i in has_been_seen if has_been_seen[i]]
    trainingdata = [(dataframes[i] , attack_classes[i] ) for i in classified_ids]
    print(trainingdata)
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
    app.run(debug=True, port=8888)
