from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from flask_login import current_user
from flask import redirect, url_for, request
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import pandas as pd
import os
from dotenv import load_dotenv
import plotly.express as px

# Loading of the .env file
load_dotenv()
# Elastic
ES_HOST = os.getenv('ES_HOST')  # Change this to your Elasticsearch host
ES_PORT = int(os.getenv('ES_PORT'))        # Change this to your Elasticsearch port
ES_INDEX = os.getenv('ES_INDEX')  # Index name for storing flow data
# Get these values from your Elasticsearch installation
ES_API_KEY = os.getenv('ES_API_KEY')  # API key for access to elastic 
SENSOR_NAME = os.getenv('SENSOR_NAME')  # Unique name to identify this sensor


def init_dash_app(flask_app):
    dash_app = Dash(__name__, server=flask_app, url_base_pathname='/dashboard/', external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Initialize Elasticsearch client
    es = Elasticsearch(
            f"{ES_HOST}:{ES_PORT}",
            api_key=ES_API_KEY,  # Authentication via API-key
            verify_certs=False,
            ssl_show_warn=False,
            request_timeout=30,
            retry_on_timeout=True
        )
    
    # Modify search to match your document structure
    s = Search(using=es, index=ES_INDEX) \
        .extra(size=10) \
        .source(['flow_id', 'flow_data', 'timestamp', "prediction", "attack_class", "has_been_seen" ])  # Specify fields to return

    # Debug: Print total documents in index
    response = s.execute()

    # Print results with more detail
    df_list = []
    for hit in response:
        df_list.append(pd.DataFrame([hit.to_dict()]))
    

    df = pd.concat(df_list)
    # DataTable columns
    cols = [
    {'name': 'flow_id', 'id': 'flow_id'},
    {'name': 'prediction', 'id': 'prediction'},
    {'name': 'attack_class', 'id': 'attack_class'},
    {'name': 'has_been_seen', 'id': 'has_been_seen'}]

    def make_grid():
        grid = dag.AgGrid(
            id="grid",
            rowData=df.to_dict("records"),
            columnDefs=[
            {"field": "timestamp", "checkboxSelection": True },
            {"field": "flow_id", "floatingFilter": False},
            {"field": "prediction" },
            {"field": "attack_class" },
            {"field": "has_been_seen" }],
            defaultColDef={"filter": True, "floatingFilter": True,  "wrapHeaderText": True, "autoHeaderHeight": True},
            dashGridOptions={"rowSelection": "multiple", "suppressRowClickSelection": True, "animateRows": False},
            #filterModel={'Report Year': {'filterType': 'number', 'type': 'equals', 'filter': 2023}},
            rowClassRules = {"bg-secondary text-dark bg-opacity-25": "params.node.rowPinned === 'top' | params.node.rowPinned === 'bottom'"},
            style={"height": 600, "width": "100%"},
            #selectedRows=df.head(1).to_dict("records")
        )
        return grid
    
    @dash_app.callback(
    Output('detail_grid', 'rowData'),
    Input('grid', 'selectedRows')
    )
    def update_detailed_grid(selected_rows):
        if not selected_rows:
            return []
    
        # Convert selected rows to dict format
        return pd.DataFrame(selected_rows).to_dict("records")
    
    def make_detailed_grid():
        detail_grid = dag.AgGrid(
        id="detail_grid",
        rowData=[],  # Empty initially
        columnDefs=[
            {"field": "timestamp"},
            {"field": "flow_id"},
            {"field": "prediction"},
            {"field": "attack_class"}
        ],
        style={"height": 400}
        )
        return detail_grid

    def make_pie_chart():
        return dcc.Graph(
            id='prediction-pie',
            figure=px.pie(
                df, 
                names="attack_class", 
                title="Attack Class Distribution"
            ).update_layout(
                legend=dict(
                    orientation="h",  # Horizontal legend
                    yanchor="bottom", # Anchor legend to the bottom
                    y=-0.3,           # Position legend below the chart (negative y moves it down)
                    xanchor="center", # Center the legend horizontally
                    x=0.5             # Center the legend
                )
            ),
            style={'height': '700px', 'width': '100%'}  # Adjust height to accommodate the legend
        )

    dash_app.layout = html.Div([
        html.H1("Welcome to the Dashboard"),
        # Main content row
        dbc.Row([
            # Left side - Grid
            dbc.Col([
                make_grid()
            ], width=8, style={"border": "1px solid #ddd", "padding": "10px"}),  # Add border and padding for debugging
            
            # Right side - Pie Chart
            dbc.Col([
                make_pie_chart()
            ], width=4, style={"border": "1px solid #ddd", "padding": "10px"})  # Add border and padding for debugging
        ], style={'margin': '20px 0', 'display': 'flex', 'flex-direction': 'row'}),
        # Bottom row - Detailed Grid
        dbc.Row([
            dbc.Col([
                make_detailed_grid()
            ], width=12)
        ])
    ], style={'padding': '20px'})

    @dash_app.callback(
    Output('prediction-pie', 'figure'),
    Input('grid', 'selectedRows')
    )
    def update_pie_chart(selected_rows):
        if not selected_rows:
            # Show overall distribution if nothing selected
            pie_data = df['flow_id'].value_counts()
            return px.pie(
                values=pie_data.values,
                names=pie_data.index,
                title='Prediction Distribution'
            ).update_layout(
                legend=dict(
                    orientation="h",  # Horizontal legend
                    yanchor="bottom", # Anchor legend to the bottom
                    y=-0.3,           # Position legend below the chart (negative y moves it down)
                    xanchor="center", # Center the legend horizontally
                    x=0.5             # Center the legend
                )
            )
        
        # Show prediction for selected row
        selected_data = selected_rows[0]
        pred = selected_data['flow_id']
        return px.pie(
            values=[1],
            names=[pred],
            title=f'Selected Flow Prediction: {pred}'
        ).update_layout(
                legend=dict(
                    orientation="h",  # Horizontal legend
                    yanchor="bottom", # Anchor legend to the bottom
                    y=-0.3,           # Position legend below the chart (negative y moves it down)
                    xanchor="center", # Center the legend horizontally
                    x=0.5             # Center the legend
                )
            )

    # Enforce authentication for the Dash app
    @flask_app.before_request
    def protect_dash_routes():
        if request.path.startswith('/dashboard/'):  # Check if the request is for the Dash app
            if not current_user.is_authenticated:  # Check if the user is logged in
                return redirect(url_for('auth.login'))  # Redirect to the login page
            

    return dash_app

