from flask import Flask, request, render_template_string, jsonify, send_file
import pandas as pd
import uuid
from io import BytesIO
import json
from datetime import datetime

app = Flask(__name__)

# Dictionaries to store dataframes, files, predictions and timestamps with unique IDs
dataframes = {}
filestore = {}
predictions_store = {}
timestamps = {}
requests_log = []  # Log for storing request information

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files and 'json' in request.files and 'predictions' in request.files and 'timestamp' in request.files:
        # Process both file and JSON data
        file = request.files['file']
        json_data = json.loads(request.files['json'].read().decode('utf-8'))
        predictions_data = json.loads(request.files['predictions'].read().decode('utf-8'))
        timestamp_data = json.loads(request.files['timestamp'].read().decode('utf-8'))

        # Generate unique IDs
        file_id = str(uuid.uuid4())
        df_id = str(uuid.uuid4())

        # Store file content
        filestore[file_id] = file.read()

        # Process JSON data into DataFrame
        df = pd.DataFrame([json_data])
        dataframes[df_id] = df

        # Store predictions and timestamp
        predictions_store[df_id] = predictions_data
        timestamps[df_id] = timestamp_data['timestamp']  # Store the timestamp

        # Log the request
        requests_log.append({'file_id': file_id, 'dataframe_id': df_id})

        return jsonify({"file_id": file_id, "dataframe_id": df_id})
    else:
        return jsonify({"error": "Missing file or JSON data"}), 400

@app.route('/')
def index():
    # Generate HTML content for all available dataframes and files
    request_entries = []
    for entry in requests_log:
        dataframe_link = f'<a href="javascript:void(0);" onclick="fetchData(\'{entry["dataframe_id"]}\')">DataFrame</a>'
        file_link = f'<a href="/download/{entry["file_id"]}">Download</a>'
        
        # Create a link to view predictions
        predictions_link = f'<a href="javascript:void(0);" onclick="showPredictions(\'{entry["dataframe_id"]}\')">View Predictions</a>'
        
        request_entries.append({
            'dataframe_link': dataframe_link,
            'file_link': file_link,
            'predictions_link': predictions_link,
            'dataframe_id': entry["dataframe_id"],  # Store dataframe ID for later use
            'predictions': predictions_store.get(entry["dataframe_id"], {}),  # Store predictions for display
            'timestamp': timestamps.get(entry["dataframe_id"], '')  # Get the timestamp for display
        })

    return render_template_string("""
        <html>
            <head>
                <title>Real-Time DataFrames and Files</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                <style>
                    body {
                        display: flex;
                        justify-content: space-between;
                    }
                    .sidebar {
                        width: 20%; /* Increased width for the sidebar */
                        border-right: 1px solid #ccc;
                        padding: 10px;
                    }
                    .content {
                        width: 75%;
                        padding: 10px;
                    }
                    a {
                        display: block;
                        margin-bottom: 5px;
                        text-decoration: none;
                        color: #007BFF;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                    .table-responsive {
                        overflow-x: auto; /* Enable horizontal scrolling */
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                    }
                    th, td {
                        padding: 8px;
                        text-align: center;
                        border: 1px solid #ddd;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <div class="sidebar">
                    <h3>Requests Log</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Timestamp</th> <!-- Moved Timestamp column to the left -->
                                <th>DataFrame</th>
                                <th>File</th>
                                <th>Predictions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for entry in request_entries %}
                                <tr>
                                    <td>{{ entry.timestamp }}</td> <!-- Display the timestamp -->
                                    <td>{{ entry.dataframe_link | safe }}</td>
                                    <td>{{ entry.file_link | safe }}</td>
                                    <td>{{ entry.predictions_link | safe }}</td> <!-- Link to view predictions -->
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                <div class="content">
                    <h3>DataFrame Details</h3>
                    <div id="dataframe-table" class="table-responsive">Select a DataFrame to view it here.</div>

                    <h3>Predictions Details</h3>
                    <div id="predictions-table">Select a prediction link to view it here.</div> <!-- Placeholder for predictions -->
                    
                    <!-- Placeholder for the pie chart -->
                    <canvas id="predictions-chart" width="400" height="400" style="display:none;"></canvas> 
                </div>
                <script>
                    // Function to fetch and display a DataFrame
                    function fetchData(df_id) {
                        fetch('/get_dataframe/' + df_id)
                            .then(response => response.json())
                            .then(data => {
                                let df = data.data;
                                let tableHTML = '<table><thead><tr>';

                                // Create table headers
                                Object.keys(df[0]).forEach(key => {
                                    tableHTML += '<th>' + key + '</th>';
                                });
                                tableHTML += '</tr></thead><tbody>';

                                // Create table rows
                                df.forEach(row => {
                                    tableHTML += '<tr>';
                                    Object.values(row).forEach(value => {
                                        tableHTML += '<td>' + value + '</td>';
                                    });
                                    tableHTML += '</tr>';
                                });

                                tableHTML += '</tbody></table>';
                                document.getElementById('dataframe-table').innerHTML = tableHTML;
                            });
                    }

                    // Function to show Predictions and draw pie chart
                    function showPredictions(df_id) {
                        let predictionsData = {{ request_entries | tojson }};
                        
                        // Find the selected prediction entry based on dataframe ID
                        let selectedPredictions = predictionsData.find(entry => entry.dataframe_id === df_id);
                        
                        if (selectedPredictions && selectedPredictions.predictions) {
                            let predsHTML = '<pre>' + JSON.stringify(selectedPredictions.predictions, null, 4) + '</pre>';
                            document.getElementById('predictions-table').innerHTML = predsHTML;

                            // Prepare data for pie chart (assuming predictions are in key-value pairs)
                            const labels = Object.keys(selectedPredictions.predictions);
                            const dataValues = Object.values(selectedPredictions.predictions);

                            // Create pie chart
                            const ctx = document.getElementById('predictions-chart');
                            ctx.style.display = 'block'; // Show the canvas
                            
                            const chart = new Chart(ctx, {
                                type: 'pie',
                                data: {
                                    labels: labels,
                                    datasets: [{
                                        label: 'Predictions',
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
                                            text: 'Prediction Distribution'
                                        }
                                    }
                                }
                            });
                        } else {
                            document.getElementById('predictions-table').innerHTML = 'No predictions found.';
                            document.getElementById('predictions-chart').style.display = 'none'; // Hide the chart if no predictions found
                        }
                    }
                </script>
            </body>
        </html>
    """, request_entries=request_entries)

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
            download_name=f"file_{file_id}.pcap"  
        )
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True, port=8888)
