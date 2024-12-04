from flask import Flask, request, render_template_string, jsonify
import pandas as pd
from io import StringIO
import uuid
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import IncrementalPCA
from sklearn.preprocessing import StandardScaler
import joblib

import numpy as np

app = Flask(__name__)

# Dictionary to store dataframes with unique IDs
dataframes = {}

@app.route('/upload', methods=['POST','GET'])
def upload():
    # # Get the CSV data from the request body
    # post_data = request.get_json()
    # ## Convert received dict into Dataframe
    # df = pd.DataFrame([post_data])
    
    # # Preprocess dataframe
    # # Reduce to exact columns that were used for fit
    # df= df[['dst_port', 'flow_duration', 'tot_fwd_pkts', 'tot_bwd_pkts',
    #    'totlen_fwd_pkts', 'totlen_bwd_pkts', 'fwd_pkt_len_max',
    #    'fwd_pkt_len_min', 'fwd_pkt_len_mean', 'fwd_pkt_len_std',
    #    'bwd_pkt_len_max', 'bwd_pkt_len_min', 'bwd_pkt_len_mean',
    #    'bwd_pkt_len_std', 'flow_byts_s', 'flow_pkts_s', 'flow_iat_mean',
    #    'flow_iat_std', 'flow_iat_max', 'flow_iat_min', 'fwd_iat_tot',
    #    'fwd_iat_mean', 'fwd_iat_std', 'fwd_iat_max', 'fwd_iat_min',
    #    'bwd_iat_tot', 'bwd_iat_mean', 'bwd_iat_std', 'bwd_iat_max',
    #    'bwd_iat_min', 'fwd_psh_flags', 'fwd_urg_flags', 'fwd_header_len',
    #    'bwd_header_len', 'fwd_pkts_s', 'bwd_pkts_s', 'pkt_len_min',
    #    'pkt_len_max', 'pkt_len_mean', 'pkt_len_std', 'pkt_len_var',
    #    'fin_flag_cnt', 'syn_flag_cnt', 'rst_flag_cnt', 'psh_flag_cnt',
    #    'ack_flag_cnt', 'urg_flag_cnt', 'cwr_flag_count', 'ece_flag_cnt',
    #    'down_up_ratio', 'pkt_size_avg', 'fwd_seg_size_avg',
    #    'bwd_seg_size_avg', 'fwd_header_len', 'subflow_fwd_pkts',
    #    'subflow_fwd_byts', 'subflow_bwd_pkts', 'subflow_bwd_byts',
    #    'init_fwd_win_byts', 'init_bwd_win_byts', 'fwd_act_data_pkts',
    #    'fwd_seg_size_min', 'active_mean', 'active_std', 'active_max',
    #    'active_min', 'idle_mean', 'idle_std', 'idle_max', 'idle_min']]
    # # Load pca and scaler
    # scaler = joblib.load('C:/Users/arin1/Google Drive/Fernuni/Praktikum/cicflowmeter/src/scaler.pkl')
    # ipca = joblib.load('C:/Users/arin1/Google Drive/Fernuni/Praktikum/cicflowmeter/src/ipca.pkl')
    # # scaler = StandardScaler()
    # scaled_features = scaler.transform(df)

    # size = len(df.columns) // 2
    # # ipca = IncrementalPCA(n_components = size)
    # # ipca.partial_fit(scaled_features)
    # #for batch in np.array_split(scaled_features, len(df) // 1):
    # #    ipca.partial_fit(batch)

    # #print(f'information retained: {sum(ipca.explained_variance_ratio_):.2%}')

    # transformed_features = ipca.transform(scaled_features)
    # new_data = pd.DataFrame(transformed_features, columns = [f'PC{i+1}' for i in range(size)])

    # #Loading the saved model with joblib
    # rf2 = joblib.load('C:/Users/arin1/Google Drive/Fernuni/Praktikum/cicflowmeter/src/rf2.pkl')

    # df["attack_type"] = rf2.predict(new_data)
    # Generate a unique ID for this DataFrame
    df = request.get_json()

    df_id = str(uuid.uuid4())

    # Store the DataFrame in the dictionary with its unique ID
    dataframes[df_id] = df

    return jsonify({"id": df_id})

@app.route('/')
def index():
    # Generate HTML content for all available dataframes
    links = [{'id': df_id, 'name': f"DataFrame {i+1}"} for i, df_id in enumerate(dataframes.keys())]

    return render_template_string("""
        <html>
            <head>
                <title>Real-Time DataFrames</title>
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
                    <h3>DataFrames</h3>
                    {% for link in links %}
                        <a href="javascript:void(0);" onclick="fetchData('{{ link.id }}')">{{ link.name }}</a>
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
        # Convert the DataFrame to a list of dictionaries for easier JSON rendering
        df = dataframes[df_id]
        df_json = df.to_dict(orient='records')
        return jsonify({"data": df_json})
    return jsonify({"error": "DataFrame not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
