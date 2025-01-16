import dash
from dash import Dash, html, dcc, dash_table, Input, Output, callback, State
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import pandas as pd
from dotenv import load_dotenv
import plotly.express as px
from datetime import datetime, timedelta
from flask import session

from ..elastic_connector import CustomElasticsearchConnector
import asyncio

# Initialize  Dash App
dash.register_page(__name__, path='/inbox/')

# Initialize Elasticsearch connector and get data
cec = CustomElasticsearchConnector()
df = asyncio.run(cec.get_all_flows(view="all", size=20))

# Component Builders


# Grid
def make_grid(seen=False, grid_id="grid"):
    grid = dag.AgGrid(
        id=grid_id,
        rowData=df[df["has_been_seen"] == seen].to_dict("records"),
        columnDefs=[
        {"field": "timestamp", "checkboxSelection": False },
        {"field": "sensor_name"},
        {"field": "flow_id", "floatingFilter": False},
        {"field": "prediction" },
        {"field": "attack_class" },
        {"field": "has_been_seen" }],
        defaultColDef={"filter": True, "floatingFilter": True,  "wrapHeaderText": True, "autoHeaderHeight": True},
        dashGridOptions={"rowSelection": "single", "suppressRowClickSelection": False, "animateRows": False},
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

def make_modal():
    return dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Detailed Flow View")),
                dbc.ModalBody("This is the content of the modal"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            size="xl",
            is_open=False,
        )

# Callbacks
# Detailed Grid Callback
def create_grid_callback(grid_id, detail_grid_id):
    @callback(
        Output(detail_grid_id, 'rowData'),
        Input(grid_id, 'selectedRows')
    )
    def update_grid(selected_rows):
        if not selected_rows:
            return []
        
        return pd.DataFrame(selected_rows).to_dict("records")

# Pie Chart Callback
@callback(
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

@callback(
    Output("graph", "figure"), 
    Input("dropdown", "value"))
def update_bar_chart(filter_date):
    # Create 30-min bins
    df['time_bin'] = df['timestamp'].dt.floor('0.1min')
    grouped_df = df[df["timestamp"]> filter_date]
    grouped_df = grouped_df.groupby(['time_bin', 'prediction']).size().reset_index(name='count')
    
    fig = px.bar(grouped_df, x="time_bin", y="count", 
                color="prediction", 
                title='Network Flow Activity',
                labels={
                    'time_bin': 'Time',
                    'count': 'Number of Flows',
                    'prediction': 'Prediction Type'
                },
                barmode="stack")
    return fig

# First callback for modal visibility
@callback(
    Output("modal", "is_open"),
    [Input('unseen_grid', 'selectedRows'),
     Input("close", "n_clicks")],
    [State("modal", "is_open")]
)
def toggle_modal(selected_rows, close_clicks, is_open):
    if close_clicks:
        return False
    if selected_rows:
        return True
    return is_open

# Second callback for modal content
@callback(
    Output("modal", "children"),
    Input('unseen_grid', 'selectedRows')
)
def update_modal_content(selected_rows):
    detail_df = pd.DataFrame(selected_rows)
    #prob_data = eval(detail_df["probabilities"].iloc[0])
    #prob_df = pd.DataFrame(list(prob_data.items()), columns=['class', 'probability'])
    
    if not selected_rows:
        return []
    
    return [
        dbc.ModalHeader(dbc.ModalTitle("Detailed Flow View")),
        dbc.ModalBody([
            dag.AgGrid(
                id="detailed_modal_grid",
                rowData= detail_df.to_dict("records"),  
                columnDefs=[
                    {"field": "timestamp"},
                    {"field": "flow_id"},
                    {"field": "prediction"},
                    {"field": "attack_class"}
                ],
                #style={"height": 400}
                ),
            dcc.Graph(
                id='prob_pie_modal',
                figure=px.pie(
                    detail_df,
                    values=detail_df.probabilities.values[0].values(),
                    names=detail_df.probabilities.values[0].keys(),
                    title="Classification Probabilities"
                ).update_layout(
                    legend=dict(
                        orientation="h",  # Horizontal legend
                        yanchor="bottom", # Anchor legend to the bottom
                        y=-0.3,           # Position legend below the chart (negative y moves it down)
                        xanchor="center", # Center the legend horizontally
                        x=0.5             # Center the legend
                    )
                ),
                ),
            dcc.Dropdown(
                id='attack-type-dropdown',
                options=list(df.probabilities.values[0].keys()),
                value=detail_df.prediction.values[0],
                clearable=False,
                className='mb-3'
            ),
            dbc.Button(
                "Submit Classification", 
                id="submit-classification", 
                color="primary",
                className="mt-2"
            ),
        ]),
        dbc.ModalFooter(
            dbc.Button("Close", id="close", className="ms-auto", n_clicks=0)
        )
    ]

@callback(
    Output('classification-output', 'children'),
    [Input('submit-classification', 'n_clicks')],
    [State('attack-type-dropdown', 'value')]
)
def handle_classification(n_clicks, selected_type):
    if n_clicks is None:
        return ""
    # Call your generic function here with selected_type
    print(f"Classified as: {selected_type}")
    return f"Classified as: {selected_type}"

# # Add callback to update welcome message
# @callback(
#     Output("welcome-alert", "children"),
#     Input("welcome-alert", "id")  # Dummy input to trigger callback
# )
# def update_welcome_message(_):
#     return f"Welcome {session.get('username', 'Guest')}!"

# Callback initialization
create_grid_callback("unseen_grid", "detailed_grid_unseen")
create_grid_callback("seen_grid", "detailed_grid_seen")


    
# Layout Components
layout = html.Div([
    make_modal(),
    dbc.Row([
        dbc.Alert(
                "Welcome! You have " + str(len(df[df["has_been_seen"] == False])) + " new flows.",
                id="welcome-alert",
                dismissable=True,
                is_open=True,
            ),
        html.Hr(),
    ], className="mt-3 mb-3"),
    dbc.Row([
        dcc.Dropdown(
        id="dropdown",
        options=[
            {'label': 'Today', 'value': datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()},
            {'label': 'Last 7 days', 'value': datetime.now() - timedelta(days=7)},
            {'label': 'Last Month', 'value': datetime.now() - timedelta(days=30)},
            {'label': 'Last Year', 'value': datetime.now() - timedelta(days=365)},
            {'label': 'All Time', 'value': "2000-01-11"}],
        value="2000-01-11",
        clearable=False),
        dcc.Graph(id="graph")
    ]),
    # Main content row
    dbc.Accordion(
    [
        dbc.AccordionItem(
            [
                dbc.Row([
                    make_grid(seen=False, grid_id="unseen_grid")
                    # # Left side - Grid
                    # dbc.Col([
                    #     make_grid(seen=False, grid_id="unseen_grid")
                    # ], width=8, style={"border": "1px solid #ddd", "padding": "10px"}),  # Add border and padding for debugging
                    
                    # # Right side - Pie Chart
                    # dbc.Col([
                    #     make_pie_chart()
                    # ], width=4, style={"border": "1px solid #ddd", "padding": "10px"})  # Add border and padding for debugging
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
])