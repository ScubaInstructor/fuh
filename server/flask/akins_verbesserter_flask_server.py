from datetime import datetime, timedelta
from flask import Flask, request, render_template_string, jsonify, send_file, redirect, url_for
import uuid
from io import BytesIO
import json
import matplotlib.pyplot as plt
import numpy as np

import matplotlib
matplotlib.use('Agg')  # Verwende den Agg-Backend

app = Flask(__name__)

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
requests_log = []   # Log for storing request information

@app.route('/upload', methods=['POST'])
def upload():
    if ('file' in request.files and 
            'json' in request.files and 
            'probabilities' in request.files  and 
            'timestamp' in request.files and 
            'prediction' in request.files and 
            'sensor_name' in request.files and
            'sensor_port' in request.files and
            'partner_ip' in request.files and
            'partner_port' in request.files):
        # Process both file and JSON data
        file = request.files['file']
        json_data = json.loads(request.files['json'].read().decode('utf-8'))
        probabilities_data = json.loads(request.files['probabilities'].read().decode('utf-8'))
        timestamp_data = json.loads(request.files['timestamp'].read().decode('utf-8'))
        prediction = request.files['prediction'].read().decode('utf-8')
        sensor_name = request.files['sensor_name'].read().decode('utf-8')
        sensor_port = request.files['sensor_port'].read().decode('utf-8')
        partner_ip = request.files['partner_ip'].read().decode('utf-8')
        partner_port = request.files['partner_port'].read().decode('utf-8')
        # Generate unique IDs
        file_id = str(uuid.uuid4())
        df_id = str(uuid.uuid4())

        # Store file content
        filestore[file_id] = file.read()

        # Store JSON data 
        dataframes[df_id] = json_data

        # Store probabilities, predictions, sensor names, timestamp and has_been_seen
        probabilities_store[df_id] = probabilities_data
        predictions_store[df_id] = prediction
        sensor_names[df_id] = sensor_name
        timestamps[df_id] = timestamp_data['timestamp']  # Store the timestamp
        sensor_ports[df_id] = sensor_port
        partner_ips[df_id] = partner_ip
        partner_ports[df_id] = partner_port

        # Initialize has_been_seen for this ID to False
        has_been_seen[df_id] = False

        # Log the request
        requests_log.append({'file_id': file_id, 'dataframe_id': df_id})

        return jsonify({"file_id": file_id, "dataframe_id": df_id})
    else:
        return jsonify({"error": "Missing file or JSON data"}), 400

@app.route('/')
def index():
    current_time = datetime.now()
    timestamps_list = []
    counts = []

    # get the relevant timestamps 
    for entry in requests_log:
        entry_time = datetime.strptime(timestamps[entry['dataframe_id']], '%Y-%m-%dT%H:%M:%S.%f')
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
    plt.bar(time_bins[::-1], count_bins[::-1], width=0.00015)  # Set width for better visualisation
    plt.xlabel('Timestamps')
    plt.ylabel('Count of Flows')
    plt.title('Last 60 Minutes')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the image
    plt.savefig('static/timeline_chart.png')  # TODO make more consistent! Path must exist!
    plt.close()

    # Generate HTML content for all available timestamps with sensor names and predictions in a table format
    return render_template_string("""
        <html>
        <head>
            <title>Abnormal Flows</title>
            <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        </head>
        <body class="bg-gray-100">
            <div class="container mx-auto p-4">
                <h1 class="text-3xl font-bold mb-4">Abnormal Flows</h1>
                <h2 class="text-xl mb-4">Zeitstrahl der letzten 60 Minuten</h2>
                <img src="/static/timeline_chart.png" alt="Zeitstrahl" class="mb-4 rounded shadow-lg" />
                <table class="min-w-full bg-white border border-gray-300 rounded-lg shadow-md">
                    <thead>
                        <tr class="bg-gray-200 text-gray-600">
                            <th class="py-2 px-4 border-b">Date</th>
                            <th class="py-2 px-4 border-b">Sensor</th>
                            <th class="py-2 px-4 border-b">Predicted class</th>
                            <th class="py-2 px-4 border-b">Class</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for entry in requests %}
                            {% if not has_been_seen[entry.dataframe_id] %}
                                <tr class="hover:bg-gray-100">
                                    <td class="py-2 px-4 border-b"><a href="/details/{{ entry.dataframe_id }}" class="text-blue-500 hover:underline">{{ entry.timestamp }}</a></td>
                                    <td class="py-2 px-4 border-b">{{ entry.sensor_name }}</td>
                                    <td class="py-2 px-4 border-b">{{ entry.prediction }}</td>
                                    <td class="py-2 px-4 border-b">{{ entry.attack_class if entry.attack_class else "unclassified" }}</td>
                                </tr>
                            {% endif %}
                        {% endfor %}
                    </tbody>
                </table>
                <button onclick="location.href='/classified_requests'" class="mt-4 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">Show classified Flows</button>
            </div>
        </body>
        </html>
    """, requests=[{
        'timestamp': timestamps[entry['dataframe_id']],
        'sensor_name': sensor_names[entry['dataframe_id']],
        'prediction': predictions_store[entry['dataframe_id']],
        'attack_class': attack_classes.get(entry['dataframe_id'], None),
        'dataframe_id': entry['dataframe_id']
    } for entry in requests_log], has_been_seen=has_been_seen)


@app.route('/details/<df_id>', methods=['GET', 'POST'])
def details(df_id):
    if df_id not in dataframes:
        return "DataFrame not found", 404
    
    # The Submit button for classification
    if request.method == 'POST':
        selected_attack_class = request.form.get('selected_attack_class')

        # If it is an newly created class
        if selected_attack_class == "NEW_CLASS":
            new_class_name = request.form.get('new_class_name')
            selected_attack_class = new_class_name
        
        attack_classes[df_id] = selected_attack_class
        has_been_seen[df_id] = True
        # add new class to all unseen flows for possible prediction
        for entry in requests_log:
            if has_been_seen[entry['dataframe_id']] == False:
                probabilities: dict = probabilities_store[entry['dataframe_id']]
                probabilities[selected_attack_class] = -1

        return redirect(url_for('index'))


    probabilities = probabilities_store.get(df_id, {})
    prediction = predictions_store.get(df_id, '')
    sensor_name = sensor_names.get(df_id, '')
    timestamp = timestamps.get(df_id, '')
    sensor_port = sensor_ports.get(df_id, '')
    partner_ip = partner_ips.get(df_id, '')
    partner_port = partner_ports.get(df_id, '')

    # Get the associated file ID to create a download link
    file_entry = next((entry for entry in requests_log if entry['dataframe_id'] == df_id), None)
    file_download_link = f"/download/{file_entry['file_id']}" if file_entry else "#"

    return render_template_string("""
        <html>
        <head>
            <title>Details for {{ timestamp }}</title>
            <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body class="bg-gray-100">
            <div class="container mx-auto p-4">
                <h1 class="text-xl font-bold mb-4">Details for {{ timestamp }}</h1>

                <div class="flex">
                    <div class="left-column flex-1 pr-4">

                        <h3 class="text-lg font-semibold mt-4">Prediction</h3>
                        <p>{{ prediction }}</p>

                        <h3 class="text-lg font-semibold mt-4">Sensor Name</h3>
                        <p>{{ sensor_name }}</p>
                        <!-- Dynamische Probabilities-Tabelle -->
                        <h3 class="text-lg font-semibold mt-4">Probabilities</h3>
                        {% if probabilities %}
                            <table class="min-w-full max-w-4xl mx-auto bg-white border border-gray-300 rounded-lg shadow-md mt-4">
                                <thead>
                                    <tr class="bg-gray-200 text-gray-600">
                                        <th class="py-2 px-4 border-b">Class</th>
                                        <th class="py-2 px-4 border-b">Probability</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for key, value in probabilities.items() %}
                                        {% if value >= 0 %}
                                            <tr class="hover:bg-gray-100">
                                                <td class="py-2 px-4 border-b">{{ key }}</td>
                                                <td class="py-2 px-4 border-b">{{ value }}</td>
                                            </tr>
                                        {% endif %}
                                    {% endfor %}
                                </tbody>
                            </table>
                        {% else %}
                            <p>No probabilities available.</p>
                        {% endif %}

                        <h3 class="mt-6">Download PCAP File</h3>
                        <a href="{{ file_download_link }}" class="inline-block bg-blue-500 text-white 
                                font-bold py-2 px-4 rounded hover:bg-blue-600">Download flow.pcap</a>
                        
                        <!-- Dropdown menu for selecting attack class -->
                        <form method="POST" class="mt-4">
                            <label for="selected_attack_class" class="block text-sm font-medium text-gray-700">Select Attack Class:</label>
                            <select name="selected_attack_class" id="selected_attack_class" class="mt-1 block w-full p-2 border border-gray-300 rounded-md">
                                <option value="" disabled selected>Select...</option>
                                {% for key, value in probabilities.items() %}
                                    <option value="{{ key }}">{{ key }}</option>
                                {% endfor %}
                                <option value="NEW_CLASS">Create New Class</option>
                            </select><br />

                            <!-- Input field for new class if selected -->
                            <div id="new-class-input" style="display:none;">
                                <label for="new_class_name" class="block text-sm font-medium text-gray-700 mt-2">New Class Name:</label><br />
                                <input type="text" name="new_class_name" id="new_class_name" placeholder="Enter new class name" class="mt-1 block w-full p-2 border border-gray-300 rounded-md"/>
                            </div>

                            <!-- Submit button -->
                            <button type="submit" class="mt-4 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">Submit</button>
                        </form>
                        <!-- JavaScript to show/hide new class input based on dropdown selection -->
                        <script type="text/javascript">
                            const selectElement = document.getElementById('selected_attack_class');
                            const newClassInputDiv = document.getElementById('new-class-input');
                            
                            selectElement.addEventListener('change', function() {
                                if (this.value === 'NEW_CLASS') {
                                    newClassInputDiv.style.display = 'block';
                                } else {
                                    newClassInputDiv.style.display = 'none';
                                }
                            });
                        </script>

                    </div>

                    <div class="right-column w-1/3">
                        
                         <table class="min-w-full bg-white border border-gray-300 rounded-lg shadow-md mt-4"> 
                            <thead> 
                                <tr class="bg-gray-200 text-gray-600"> 
                                    <th class="py-2 px-4 border-b">{{sensor_name}}</th> 
                                    <th class="py-2 px-4 border-b">{{partner_ip}}</th> 
                                </tr>
                            </thead> 
                            <tbody> 
                                <tr class="hover:bg-gray-100"> 
                                    <td class="py-2 px-4 border-b">{{sensor_port}}</td>  
                                    <td class="py-2 px-4 border-b">{{partner_port}}</td> 
                                </tr>
                            </tbody> 
                        </table>          
                        
                        <!-- Canvas for Pie Chart -->
                        <div class="mt-6">
                            <canvas id="probabilities-chart" width="300" height="300"></canvas>
                        </div>

                    
                    
                                  
                    <!-- JavaScript to create the pie chart -->
                    <script>
                        const probabilitiesData = {{ probabilities | tojson }};
                        const filteredEntries = Object.entries(probabilitiesData).filter(([key, value]) => value >= 0); //Don't use newly created classes!
                        const labels = filteredEntries.map(entry => entry[0]); // Labels
                        const dataValues = filteredEntries.map(entry => entry[1]); // Values

                        const ctx = document.getElementById('probabilities-chart');
                        const chart = new Chart(ctx, {
                            type: 'pie',
                            data: {
                                labels: labels,
                                datasets: [{
                                    label: 'Probability Distribution',
                                    data: dataValues,
                                    backgroundColor: [
                                        'rgba(255, 99, 132, 0.2)',
                                        'rgba(54, 162, 235, 0.2)',
                                        'rgba(255, 206, 86, 0.2)',
                                        'rgba(75, 192, 192, 0.2)',
                                        'rgba(153, 102, 255, 0.2)',
                                        'rgba(255, 159, 64, 0.2)'
                                    ],
                                    borderColor: [
                                        'rgba(255, 99, 132, 1)',
                                        'rgba(54, 162, 235, 1)',
                                        'rgba(255, 206, 86, 1)',
                                        'rgba(75, 192, 192, 1)',
                                        'rgba(153, 102, 255, 1)',
                                        'rgba(255, 159, 64, 1)'
                                    ],
                                    borderWidth: 1
                                }]
                            },
                            options: {
                                responsive: true,
                                plugins: {
                                    legend: {
                                        position: 'top',
                                    },
                                    title: {
                                        display: true,
                                        text: 'Probability Distribution'
                                    }
                                }
                            }
                        });
                    </script>
                </div>
                                  
        </body>
        </html>
    """, probabilities=probabilities,
       prediction=prediction,
       sensor_name=sensor_name,
       timestamp=timestamp,
       file_download_link=file_download_link,
       sensor_port=sensor_port,
       partner_ip=partner_ip,
       partner_port=partner_port)




@app.route('/retrain')
def some_function():
    classified_ids = [i for i in has_been_seen if has_been_seen[i]]
    trainingdata = [(dataframes[i] , attack_classes[i] ) for i in classified_ids]
    print(trainingdata)
    print("DEBUG: Button pushed")
    return redirect(url_for('index'))  # Back to index

# @app.route('/get_dataframe/<df_id>', methods=['GET'])
# def get_dataframe(df_id):
#     if df_id in dataframes:
#         df = dataframes[df_id]
#         df_json = df.to_dict(orient='records')
#         return jsonify({"data": df_json})
#     return jsonify({"error": "DataFrame not found"}), 404

@app.route('/download/<file_id>')
def download_file(file_id):
    if file_id in filestore:
        return send_file(
            BytesIO(filestore[file_id]),
            as_attachment=True,
            download_name=f"flow.pcap"  
        )
    return "File not found", 404

@app.route('/classified_requests')
def classified_requests():
    # HTML for classified Flows
    return render_template_string("""
        <html>
            <head>
                <title>Already classified anomalies</title>
                <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
            </head>
            <body class="bg-gray-100">
                <div class="container mx-auto p-4">
                    <h1 class="text-3xl font-bold mb-4">Already classified anomalies</h1>
                    <table class="min-w-full bg-white border border-gray-300 rounded-lg shadow-md">
                        <thead>
                            <tr class="bg-gray-200 text-gray-600">
                                <th class="py-2 px-4 border-b">Date</th>
                                <th class="py-2 px-4 border-b">Sensor</th>
                                <th class="py-2 px-4 border-b">Predicted class</th>
                                <th class="py-2 px-4 border-b">Class</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for entry in requests %}
                                {% if has_been_seen[entry.dataframe_id] %}
                                    <tr class="hover:bg-gray-100">
                                        <td class="py-2 px-4 border-b"><a href="/details/{{ entry.dataframe_id }}" class="text-blue-500 hover:underline">{{ entry.timestamp }}</a></td>
                                        <td class="py-2 px-4 border-b">{{ entry.sensor_name }}</td>
                                        <td class="py-2 px-4 border-b">{{ entry.prediction }}</td>
                                        <td class="py-2 px-4 border-b">{{ entry.attack_class if entry.attack_class else "unklassifiziert" }}</td>
                                    </tr>
                                {% endif %}
                            {% endfor %}
                        </tbody>
                    </table>
                    <button onclick="location.href='/'" class="mt-4 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">Start Page</button>
                    <button onclick="location.href='/retrain'" class="mt-4 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">Retrain</button>
                </div>
            </body>
        </html>
    """, requests=[{
            'timestamp': timestamps[entry['dataframe_id']],
            'sensor_name': sensor_names[entry['dataframe_id']],
            'prediction': predictions_store[entry['dataframe_id']],
            'attack_class': attack_classes.get(entry['dataframe_id'], None),
            'dataframe_id': entry['dataframe_id']
        } for entry in requests_log], has_been_seen=has_been_seen)


if __name__ == '__main__':
    app.run(debug=True, port=8888)
