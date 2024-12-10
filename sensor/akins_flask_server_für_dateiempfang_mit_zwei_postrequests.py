from flask import Flask, request, render_template_string, jsonify, send_file
import pandas as pd
import uuid
from io import BytesIO
import json

app = Flask(__name__)

# Dictionary to store dataframes and files with unique IDs
dataframes = {}
filestore = {}



@app.route('/upload', methods=['POST','GET'])
def upload():
    if 'file' not in request.files:  
        # Process JSON data
        df = pd.DataFrame([request.get_json()])
        df_id = str(uuid.uuid4())
        dataframes[df_id] = df
        return jsonify({"id": df_id})
    else: 
        # Process file upload
        file = request.files['file']
        files_id = str(uuid.uuid4())
        filestore[files_id] = file.read()  # Store file content
        return jsonify({"id": files_id})

# @app.route('/upload', methods=['POST'])
# def upload():
#     # Überprüfen, ob sowohl die Datei als auch die JSON-Daten in der Anfrage vorhanden sind
#     if 'file' in request.files and 'json' in request.files:
#         # Datei und JSON-Daten verarbeiten
#         file = request.files['file']
#         json_data = json.loads(request.files['json'].read().decode('utf-8'))

#         # Generiere eindeutige IDs
#         file_id = str(uuid.uuid4())
#         df_id = str(uuid.uuid4())

#         # Speichere den Inhalt der Datei
#         filestore[file_id] = file.read()

#         # Verarbeite die JSON-Daten
#         df = pd.DataFrame([json_data])
#         dataframes[df_id] = df

#         return jsonify({"file_id": file_id, "dataframe_id": df_id})
#     else:
#         return jsonify({"error": "Fehlende Datei oder JSON-Daten"}), 400



@app.route('/')
def index():
    # Generate HTML content for all available dataframes and files
    links = [{'id': df_id, 'name': f"DataFrame {i+1}", 'type': 'dataframe'} for i, df_id in enumerate(dataframes.keys())] 
    links += [{'id': file_id, 'name': f"File {i+1}", 'type': 'file'} for i, file_id in enumerate(filestore.keys())] 

    return render_template_string("""
        <html>
            <head>
                <title>Real-Time DataFrames and Files</title>
                <style>
                    body {
                        display: flex;
                        justify-content: space-between;
                    }
                    .sidebar {
                        width: 10%;
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
                    <h3>DataFrames and Files</h3>
                    {% for link in links %}
                        {% if link.type == 'dataframe' %}
                            <a href="javascript:void(0);" onclick="fetchData('{{ link.id }}')">{{ link.name }}</a>
                        {% else %}
                            <a href="/download/{{ link.id }}">{{ link.name }} (Download)</a>
                        {% endif %}
                    {% endfor %}
                </div>
                <div class="content">
                    <h3>DataFrame Details</h3>
                    <div id="dataframe-table">Select a DataFrame to view it here.</div>
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
                </script>
            </body>
        </html>
    """, links=links)

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
