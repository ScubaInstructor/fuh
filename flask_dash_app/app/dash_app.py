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
from .elastic_connector import CustomElasticsearchConnector
import asyncio

# # Loading of the .env file
# load_dotenv()
# # Elastic
# ES_HOST = os.getenv('ES_HOST')  # Change this to your Elasticsearch host
# ES_PORT = int(os.getenv('ES_PORT'))        # Change this to your Elasticsearch port
# ES_INDEX = os.getenv('ES_INDEX')  # Index name for storing flow data
# # Get these values from your Elasticsearch installation
# ES_API_KEY = os.getenv('ES_API_KEY')  # API key for access to elastic 
# SENSOR_NAME = os.getenv('SENSOR_NAME')  # Unique name to identify this sensor


def init_dash_app(flask_app):
    # Initialize  Dash App
    dash_app = Dash(__name__, server=flask_app, url_base_pathname='/dashboard/', external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Initialize Elasticsearch connector and get data
    cec = CustomElasticsearchConnector()
    df = asyncio.run(cec.get_all_flows(view="all", size=20))

    
    # Component Builders
    # Grid
    def make_grid(seen="*", grid_id="grid"):
        grid = dag.AgGrid(
            id=grid_id,
            rowData=df[df["has_been_seen"] == seen].to_dict("records"),
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
    def make_detailed_grid(grid_id):
        detail_grid = dag.AgGrid(
        id=grid_id,
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


    # Navigation Bar
    def make_navbar():
        return dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Page 1", href="#")),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("More pages", header=True),
                        dbc.DropdownMenuItem("Page 2", href="#"),
                        dbc.DropdownMenuItem("Page 3", href="#"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="More",
                ),
            ],
            brand="NavbarSimple",
            brand_href="#",
            color="primary",
            dark=True,
        )
    
    # Callbacks
    # Detailed Grid Callback
    def create_grid_callback(grid_id, detail_grid_id):
        @dash_app.callback(
            Output(detail_grid_id, 'rowData'),
            Input(grid_id, 'selectedRows')
        )
        def update_grid(selected_rows):
            if not selected_rows:
                return []
            
            return pd.DataFrame(selected_rows).to_dict("records")
    # Pie Chart Callback
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

    # Callback initialization
    create_grid_callback("unseen_grid", "detailed_grid_unseen")
    create_grid_callback("seen_grid", "detailed_grid_seen")
    
     
    # Layout Components
    dash_app.layout = html.Div([
        make_navbar(),
        # Main content row
        dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    dbc.Row([
                        # Left side - Grid
                        dbc.Col([
                            make_grid(seen=False, grid_id="unseen_grid")
                        ], width=8, style={"border": "1px solid #ddd", "padding": "10px"}),  # Add border and padding for debugging
                        
                        # Right side - Pie Chart
                        dbc.Col([
                            make_pie_chart()
                        ], width=4, style={"border": "1px solid #ddd", "padding": "10px"})  # Add border and padding for debugging
                    ], style={'margin': '20px 0', 'display': 'flex', 'flex-direction': 'row'}),
                    # Bottom row - Detailed Grid
                    dbc.Row([
                        dbc.Col([
                            make_detailed_grid("detailed_grid_unseen")
                        ], width=12)
                    ])
                ],
                title="Unclassified Flows",
            ),
            dbc.AccordionItem(
                [
                    make_grid(seen=True, grid_id="seen_grid"),
                    make_detailed_grid("detailed_grid_seen"),
                ],
                title="Classified Flows",
            ),
        ],
        ),
    ], style={'padding': '20px'})

    
    


    # Enforce authentication for the Dash app
    @flask_app.before_request
    def protect_dash_routes():
        if request.path.startswith('/dashboard/'):  # Check if the request is for the Dash app
            if not current_user.is_authenticated:  # Check if the user is logged in
                return redirect(url_for('auth.login'))  # Redirect to the login page
            

    return dash_app

