from flask import Flask, request, render_template_string, jsonify, send_file
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
    # Generate HTML content for all available timestamps with sensor names and predictions
    return render_template_string("""
        <html>
            <head>
                <title>Requests Log</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                    }
                    a {
                        display: block;
                        margin: 10px 0;
                        text-decoration: none;
                        color: #007BFF;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                </style>
            </head>
            <body>
                <h1>Requests Log</h1>
                {% for entry in requests %}
                    <a href="/details/{{ entry.dataframe_id }}">
                        {{ entry.timestamp }} - {{ entry.sensor_name }} - {{ entry.prediction }}
                    </a>
                {% endfor %}
            </body>
        </html>
    """, requests=[{
            'timestamp': timestamps[entry['dataframe_id']],
            'sensor_name': sensor_names[entry['dataframe_id']],
            'prediction': predictions_store[entry['dataframe_id']],
            'dataframe_id': entry['dataframe_id']
        } for entry in requests_log])

@app.route('/details/<df_id>')
def details(df_id):
    if df_id not in dataframes:
        return "DataFrame not found", 404

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
                    }
                    h1 {
                        margin-bottom: 20px;
                    }
                    .table-responsive {
                        overflow-x: auto; /* Enable horizontal scrolling */
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 20px;
                    }
                    th, td {
                        padding: 8px;
                        text-align: center;
                        border: 1px solid #ddd;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                    canvas {
                        max-width: 300px; /* Set a maximum width for the chart */
                        height: auto; /* Maintain aspect ratio */
                        margin-bottom: 10px; /* Add some space below the chart */
                    }
                </style>
            </head>
            <body>
                <h1>Details for {{ timestamp }}</h1>

                <h3>Prediction</h3>
                <p>{{ prediction }}</p>

                <h3>Sensor Name</h3>
                <p>{{ sensor_name }}</p>
                                  
                <!-- Download link for the PCAP file -->
                <h3>Download PCAP File</h3>
                <a href="{{ file_download_link }}">Download flow.pcap</a>
                                  
                <h3>Probabilities</h3>
                <div id="probabilities-table">
                    {% if probabilities %}
                        <pre>{{ probabilities | tojson(indent=4) }}</pre>
                    {% else %}
                        <p>No probabilities available.</p>
                    {% endif %}
                </div>

                <!-- Placeholder for the pie chart -->
                <canvas id="probabilities-chart" width="400" height="400"></canvas>

                

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
