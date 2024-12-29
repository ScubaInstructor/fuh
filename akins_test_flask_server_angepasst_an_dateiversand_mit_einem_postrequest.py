from flask import Flask, request, render_template_string, jsonify, send_file, redirect, url_for
import pandas as pd
import uuid
from io import BytesIO
import json
from datetime import datetime

app = Flask(__name__)

# Dictionaries to store dataframes, files, probabilities, predictions and timestamps with unique IDs
dataframes = {}
filestore = {}
probabilities_store = {}
predictions_store = {}
sensor_names = {}
timestamps = {}
attack_classes = {}  # Store selected attack classes
requests_log = []  # Log for storing request information

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

        # Process JSON data into DataFrame
        df = pd.DataFrame([json_data])
        dataframes[df_id] = df

        # Store probabilities, predictions, sensor names, and timestamp
        probabilities_store[df_id] = probabilities_data
        predictions_store[df_id] = prediction_data
        sensor_names[df_id] = sensor_name_data
        timestamps[df_id] = timestamp_data['timestamp']  # Store the timestamp

        # Log the request
        requests_log.append({'file_id': file_id, 'dataframe_id': df_id})

        return jsonify({"file_id": file_id, "dataframe_id": df_id})
    else:
        return jsonify({"error": "Missing file or JSON data"}), 400

@app.route('/')
def index():
    # Generate HTML content for all available timestamps with sensor names and predictions in a table format
    return render_template_string("""
        <html>
            <head>
                <title>Requests Log</title>
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
                <h1>Requests Log</h1>
                <table>
                    <thead>
                        <tr>
                            <th>Datum</th>
                            <th>Sensor</th>
                            <th>Vorgeschlagene Klasse</th>
                            <th>Klasse</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for entry in requests %}
                            <tr>
                                <td><a href="/details/{{ entry.dataframe_id }}">{{ entry.timestamp }}</a></td>
                                <td>{{ entry.sensor_name }}</td>
                                <td>{{ entry.prediction }}</td>
                                <td>{{ entry.attack_class if entry.attack_class else "unklassifiziert" }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </body>
        </html>
    """, requests=[{
            'timestamp': timestamps[entry['dataframe_id']],
            'sensor_name': sensor_names[entry['dataframe_id']],
            'prediction': predictions_store[entry['dataframe_id']],
            'attack_class': attack_classes.get(entry['dataframe_id'], None),
            'dataframe_id': entry['dataframe_id']
        } for entry in requests_log])

@app.route('/details/<df_id>', methods=['GET', 'POST'])
def details(df_id):
    if df_id not in dataframes:
        return "DataFrame not found", 404

    if request.method == 'POST':
        selected_attack_class = request.form.get('selected_attack_class')
        
        # Save the selected attack class for later retrieval on the overview page
        attack_classes[df_id] = selected_attack_class
        
        return redirect(url_for('index'))  # Redirect to the overview page after selection
        
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
                            <option value="">Select...</option>
                            <option value="BENIGN">BENIGN</option>
                            <option value="BOT">BOT</option>
                            <option value="DOS">DOS</option>
                            <option value="WEB ATTACK">WEB ATTACK</option>
                        </select>
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

@app.route('/get_dataframe/<df_id>', methods=['GET'])
def get_dataframe(df_id):
    if df_id in dataframes:
        df = dataframes[df_id]
        df_json = df.to_dict(orient='records')
        return jsonify({"data": df_json})
    return jsonify({"error": "DataFrame not found"}), 404

@app.route('/download/<file_id>')
def download_file(file_id):
    if file_id in filestore:
        return send_file(
            BytesIO(filestore[file_id]),
            as_attachment=True,
            download_name=f"flow.pcap"  
        )
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
