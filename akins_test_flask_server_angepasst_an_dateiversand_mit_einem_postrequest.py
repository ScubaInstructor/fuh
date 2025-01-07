from datetime import datetime
from flask import Flask, request, render_template_string, jsonify, send_file, redirect, url_for
import uuid
from io import BytesIO
import json
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

# Dictionaries to store dataframes, files, probabilities, predictions and timestamps with unique IDs
dataframes = {}
filestore = {}
probabilities_store = {}
predictions_store = {}
sensor_names = {}
timestamps = {}
attack_classes = {} # Store selected attack classes
has_been_seen = {}  # Store if entries have been seen
requests_log = []   # Log for storing request information

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files and 'json' in request.files and 'probabilities' in request.files and 'timestamp' in request.files and 'prediction' in request.files and 'sensor_name' in request.files:
        # Process both file and JSON data
        file = request.files['file']
        json_data = json.loads(request.files['json'].read().decode('utf-8'))
        probabilities_data = json.loads(request.files['probabilities'].read().decode('utf-8'))
        timestamp_data = json.loads(request.files['timestamp'].read().decode('utf-8'))
        prediction_data = request.files['prediction'].read().decode('utf-8')
        sensor_name_data = request.files['sensor_name'].read().decode('utf-8')

        # Generate unique IDs
        file_id = str(uuid.uuid4())
        df_id = str(uuid.uuid4())

        # Store file content
        filestore[file_id] = file.read()

        # Store JSON data 
        dataframes[df_id] = json_data

        # Store probabilities, predictions, sensor names, timestamp and has_been_seen
        probabilities_store[df_id] = probabilities_data
        predictions_store[df_id] = prediction_data
        sensor_names[df_id] = sensor_name_data
        timestamps[df_id] = timestamp_data['timestamp']  # Store the timestamp
        
        # Initialize has_been_seen for this ID to False
        has_been_seen[df_id] = False

        # Log the request
        requests_log.append({'file_id': file_id, 'dataframe_id': df_id})

        return jsonify({"file_id": file_id, "dataframe_id": df_id})
    else:
        return jsonify({"error": "Missing file or JSON data"}), 400

@app.route('/')
def index():

    # get the relevant timestamps 
    current_time = datetime.now()
    recent_requests = [entry for entry in requests_log if 
                    current_time - datetime.strptime(timestamps[entry['dataframe_id']], '%Y-%m-%d %H:%M:%S.%f') <= timedelta(minutes=60)]

    # create a list of timestamps and counters
    timestamps_list = [datetime.strptime(timestamps[entry['dataframe_id']], '%Y-%m-%d %H:%M:%S.%f') for entry in recent_requests]
    counts = np.arange(1, len(timestamps_list) + 1)

    # CReate barchart
    plt.figure(figsize=(10, 5))
    plt.bar(timestamps_list, counts, width=0.01)  # Breite anpassen für bessere Sichtbarkeit
    plt.xlabel('Timestamps')
    plt.ylabel('Anzahl der Requests')
    plt.title('Requests in den letzten 60 Minuten')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the image
    plt.savefig('static/timeline_chart.png')  # Stelle sicher, dass der Pfad existiert
    plt.close()


    # Generate HTML content for all available timestamps with sensor names and predictions in a table format
    return render_template_string("""
        <html>
            <head>
                <title>Abnormal Flows</title>
                
                <h2>Zeitstrahl der letzten 60 Minuten</h2>
                <img src="/static/timeline_chart.png" alt="Zeitstrahl" />

                <style>
                    body {
                        font-family: Arial, sans-serif;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                    }
                    th, td {
                        padding: 10px;
                        text-align: left;
                        border: 1px solid #ddd;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                    a {
                        color: #007BFF;
                        text-decoration: none;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                </style>
            </head>
            <body>
                <h1>Abnormal Flows</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Sensor</th>
                            <th>Predicted Class</th>
                            <th>Class</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for entry in requests %}
                            {% if not has_been_seen[entry.dataframe_id] %}
                                <tr>
                                    <td><a href="/details/{{ entry.dataframe_id }}">{{ entry.timestamp }}</a></td>
                                    <td>{{ entry.sensor_name }}</td>
                                    <td>{{ entry.prediction }}</td>
                                    <td>{{ entry.attack_class if entry.attack_class else "unclassified" }}</td>
                                </tr>
                            {% endif %}
                        {% endfor %}
                    </tbody>
                </table>
                <button onclick="location.href='/classified_requests'" style="margin-top: 20px;">Show classified Flows</button>
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

    if request.method == 'POST':
        selected_attack_class = request.form.get('selected_attack_class')
        
        # Save the selected attack class for later retrieval on the overview page
        if selected_attack_class == "NEW_CLASS":
            new_class_name = request.form.get('new_class_name')
            attack_classes[df_id] = new_class_name
        else:
            attack_classes[df_id] = selected_attack_class        
        
        has_been_seen[df_id] = True         # Mark this request as seen
        return redirect(url_for('index'))   # Redirect to the overview page after selection
        
    probabilities = probabilities_store.get(df_id, {})
    prediction = predictions_store.get(df_id, '')
    sensor_name = sensor_names.get(df_id, '')
    timestamp = timestamps.get(df_id, '')

    # Get the associated file ID to create a download link
    file_entry = next((entry for entry in requests_log if entry['dataframe_id'] == df_id), None)
    file_download_link = f"/download/{file_entry['file_id']}" if file_entry else "#"

    return render_template_string("""
        <html>
            <head>
                <title>Details for {{ timestamp }}</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex; /* Use flexbox for layout */
                    }
                    .left-column {
                        flex: 1; /* Take up remaining space */
                        padding-right: 20px; /* Add some space between columns */
                    }
                    .right-column {
                        width: 300px; /* Fixed width for the chart column */
                    }
                    h1 {
                        margin-bottom: 20px;
                    }
                    canvas {
                        max-width: 100%; /* Ensure the chart fits within its container */
                        height: auto; /* Maintain aspect ratio */
                    }
                </style>
            </head>
            <body>
                <div class="left-column">
                    <h1>Details for {{ timestamp }}</h1>

                    <h3>Prediction</h3>
                    <p>{{ prediction }}</p>

                    <h3>Sensor Name</h3>
                    <p>{{ sensor_name }}</p>

                    <h3>Probabilities</h3>
                    <div id="probabilities-table">
                        {% if probabilities %}
                            <pre>{{ probabilities | tojson(indent=4) }}</pre>
                        {% else %}
                            <p>No probabilities available.</p>
                        {% endif %}
                    </div>

                    <!-- Dropdown menu for selecting attack class -->
                    <form method="POST">
                        <label for="selected_attack_class">Select Attack Class:</label>
                        <select name="selected_attack_class" id="selected_attack_class">
                            <option value="" disabled selected>Select...</option>
                            <option value="BENIGN">BENIGN</option>
                            <option value="BOT">BOT</option>
                            <option value="DOS">DOS</option>
                            <option value="WEB ATTACK">WEB ATTACK</option>
                            <!-- Option to create a new class -->
                            <option value="NEW_CLASS">Create New Class</option> 
                        </select><br />
                        
                        <!-- Input field for new class if selected -->
                        <div id="new-class-input" style="display:none;">
                            <label for="new_class_name">New Class Name:</label><br />
                            <input type="text" name="new_class_name" id="new_class_name" placeholder="Enter new class name" />
                        </div>
                                  
                        <button type="submit">Submit</button>
                    </form>

                    <!-- Download link for the PCAP file -->
                    <h3>Download PCAP File</h3>
                    <a href="{{ file_download_link }}">Download flow.pcap</a>
                </div>

                <div class="right-column">
                    <!-- Placeholder for the pie chart -->
                    <canvas id="probabilities-chart" width="300" height="300"></canvas>
                </div>
                
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

                <script>
                    // Prepare data for pie chart (assuming probabilities are in key-value pairs)
                    const probabilitiesData = {{ probabilities | tojson }};
                    
                    const labels = Object.keys(probabilitiesData);
                    const dataValues = Object.values(probabilitiesData);

                    // Create pie chart
                    const ctx = document.getElementById('probabilities-chart');
                    
                    const chart = new Chart(ctx, {
                        type: 'pie',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Probabilities',
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

            </body>
        </html>
    """, probabilities=probabilities,
       prediction=prediction,
       sensor_name=sensor_name,
       timestamp=timestamp,
       file_download_link=file_download_link)

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
                <title>Klassifizierte Anfragen</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                    }
                    th, td {
                        padding: 10px;
                        text-align: left;
                        border: 1px solid #ddd;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h1>Classified Flows</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Sensor</th>
                            <th>Predicted Class</th>
                            <th>Class</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for entry in requests %}
                            {% if has_been_seen[entry.dataframe_id] %}
                                <tr>
                                    <td><a href="/details/{{ entry.dataframe_id }}">{{ entry.timestamp }}</a></td>
                                    <td>{{ entry.sensor_name }}</td>
                                    <td>{{ entry.prediction }}</td>
                                    <td>{{ entry.attack_class if entry.attack_class else "unklassifiziert" }}</td>
                                </tr>
                            {% endif %}
                        {% endfor %}
                    </tbody>
                </table>
                <button onclick="location.href='/'" style="margin-top: 20px;">Start Page</button>
                <button onclick="location.href='/retrain'" style="margin-bottom: 20px;">Retrain</button>
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
