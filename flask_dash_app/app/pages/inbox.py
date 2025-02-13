import dash
from dash import Dash, html, dcc, dash_table, Input, Output, callback, State
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from base64 import b64decode, b64encode
from io import BytesIO
import base64
import plotly.express as px

from ..elastic_connector import CustomElasticsearchConnector
import asyncio

from .grid_components import (create_world_map, make_pie_chart, make_detailed_grid,
                            make_grid, display_line, create_boxplot, make_prediction_pie_chart)


# Initialize  Dash App
dash.register_page(__name__, path='/inbox/')

# Number of flows to display
flow_nr = 5000

# Initialize Elasticsearch connector and get data
cec = CustomElasticsearchConnector()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
# Load maximum possible number of flows
try:
    df = asyncio.run(cec.get_all_flows(view="unseen", size=flow_nr, include_pcap=False))
    if df.empty:
        trigger = "empty"
    else:
        # Normal behaviour trigger
        trigger = "normal"
        
        flow_data = df["flow_data"].apply(pd.Series)
        min_flow_data = flow_data.select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1).min()
        max_flow_data = flow_data.select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1).max()
        mean_flow_data = flow_data.select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1).mean()
        q1_flow_data = flow_data.select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1).quantile([0.25])
        q3_flow_data = flow_data.select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1).quantile([0.75])

        min_flow_data = pd.DataFrame([min_flow_data], columns=mean_flow_data.index.to_list())
        max_flow_data = pd.DataFrame([max_flow_data], columns=mean_flow_data.index.to_list())
        mean_flow_data = pd.DataFrame([mean_flow_data], columns=mean_flow_data.index.to_list())
        # q1_flow_data = pd.DataFrame([q1_flow_data], columns=q1_flow_data.index.to_list())
        # q3_flow_data = pd.DataFrame([q3_flow_data], columns=q3_flow_data.index.to_list())
    
except Exception as e:
    trigger = "error"
    df = pd.DataFrame()

# Special Component Builders

# Get statistics of flow data

def create_welcome_alert():
    df = loop.run_until_complete(cec.get_all_flows(view="unseen", size=flow_nr, include_pcap=False))
    return dbc.Alert(        
        "Welcome! You have " + str(len(df[df["has_been_seen"] == False])) + " new flows.",
        id="welcome-alert",
        dismissable=True,
        is_open=True,
        duration=4000,
    )

def make_modal():
    return dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Detailed Flow View")),
                dbc.ModalBody("This is the content of the modal", id="modal-body"),
                dbc.ModalFooter([
                    dbc.Button(
                        "Submit Classification", 
                        id="submit-classification", 
                        color="primary",
                        className="mt-2",
                        n_clicks=None
                    ),
                    dbc.Button(
                        "Download PCAP", 
                        id="download-pcap", 
                        color="primary",
                        className="mt-2",
                        n_clicks=None
                    ),
                    dcc.Download(id="download-pcap-content"),
                    dbc.Button("Close", id="close", className="ms-auto", n_clicks=None)
                ]),
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
    def update_detail_grid(selected_rows):
        if not selected_rows:
            return []
        
        return pd.DataFrame(selected_rows).to_dict("records")


# Add callback for accordion
@callback(
    Output("boxplot-content", "children"),
    [Input("accordion", "active_item")],
    [State('selected-row-store', 'data')]
)
def update_boxplot(is_open, selected_row_data):
    if not is_open or not selected_row_data:
        return []
    detail_df = pd.DataFrame(selected_row_data)
    detail_flow_df = detail_df["flow_data"].apply(pd.Series).select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1)
    detail_flow_df = pd.concat([detail_flow_df, min_flow_data, mean_flow_data, max_flow_data, q1_flow_data, q3_flow_data],ignore_index=True)
    detail_flow_df = detail_flow_df.div(max_flow_data.iloc[0])

    return create_boxplot(detail_flow_df)


# First callback for modal visibility
@callback(
    Output("modal", "is_open"),
    Input('unseen_grid', 'selectedRows'),
    Input("close", "n_clicks"), 
    Input('submit-classification', 'n_clicks'),
    State("modal", "is_open"),
    prevent_initial_call=True
)
def toggle_modal(selected_rows, close_clicks, submit_clicks, is_open):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print("trigger modal")
    print(changed_id)
    print(submit_clicks)
    if "close" in changed_id or 'submit-classification' in changed_id:
        print("close or submit clicked")
        return False
    if selected_rows:
        print("close or submit NOT clicked")
        return True
    print("not in if")
    return dash.no_update

# Second callback for modal content
@callback(
    Output("modal-body", "children"),
    Input('unseen_grid', 'selectedRows')
)
def update_modal_content(selected_rows):
    detail_df = pd.DataFrame(selected_rows)
    # detail_flow_df = detail_df["flow_data"].apply(pd.Series).select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1)
    # detail_flow_df = pd.concat([detail_flow_df, min_flow_data, mean_flow_data, max_flow_data, q1_flow_data, q3_flow_data],ignore_index=True)
    # detail_flow_df = detail_flow_df.div(max_flow_data.iloc[0])
    #prob_data = eval(detail_df["probabilities"].iloc[0])
    #prob_df = pd.DataFrame(list(prob_data.items()), columns=['class', 'probability'])
    
    if not selected_rows:
        return dash.no_update
    
    return [
        dcc.Store(id='selected-row-store', data=detail_df.to_dict("records")),
        make_detailed_grid("detailed_modal_grid", selected_rows),
        make_pie_chart("prob_pie_modal", selected_rows),
        dbc.Accordion(
        [
            dbc.AccordionItem(
                children=[html.Div(id="boxplot-content")],  # Add container for content
                title="Flow Metrics",
                id="accordion-item"
            ),
        ],
        start_collapsed=True, id="accordion"
        ),
        dbc.Row([
            html.H5(children="Attack Type Classification", className="mb-0 mb-1"),
            dcc.Dropdown(
                id='attack-type-dropdown',
                options=list(df.probabilities.values[0].keys()),
                value=detail_df.prediction.values[0],
                clearable=False,
                className='mb-3'
            ),
        ], className="mt-3 mb-3"),
        ]


@callback(
    [Output('alert-store', 'data'),
     Output('alert-container', 'children')],
    [Input('submit-classification', 'n_clicks')],
    [State('attack-type-dropdown', 'value'),
     State('selected-row-store', 'data'),
     State('alert-store', 'data')]
)
def handle_classification(n_clicks, selected_type, selected_row_data, current_alerts):
    if n_clicks is None:
        return current_alerts, []
    
    # Change flow classification in elastic
    detail_df = pd.DataFrame(selected_row_data)
    flow_id = detail_df["flow_id"].values[0]
    status = "success"

    try:
        loop.run_until_complete(cec.set_attack_class(flow_id=flow_id, attack_class=selected_type))
        loop.run_until_complete(cec.set_flow_as_seen(flow_id=flow_id))
        # Create new alert
        new_alert = {
            'id': f'alert-{len(current_alerts)}',
            'message': f'Flow {flow_id} classified as {selected_type}'
        }
        status = "success"
    except:
        new_alert = {
        'id': f'alert-{len(current_alerts)}',
        'message': f'Flow {flow_id} could not be classified. Elastic Database Error.',
        }
        status = "danger"
        

    
    # Add new alert to list
    updated_alerts = current_alerts + [new_alert]
    
    # Create alert components
    alert_components = [
        dbc.Alert(
            f"{alert['message']}", 
            id=alert['id'],
            dismissable=True,
            is_open=True,
            color=status,
            duration=4000,
            className="mt-2"
        ) for alert in updated_alerts
    ]
    
    return updated_alerts, alert_components

@callback(
    Output("download-pcap-content", "data"),
    Input("download-pcap", "n_clicks"),
    State('selected-row-store', 'data'),
    prevent_initial_call=True
)
def download_pcap(n_clicks, selected_row_data):
    if n_clicks is None:
        return None

    # Request pcap data for flow id
    item = loop.run_until_complete(cec.get_all_flows(view="all", size=1, include_pcap=True, flow_id=selected_row_data[0]["flow_id"]))
    detail_df = pd.DataFrame(item)
    pcap_data = (detail_df["pcap_data"].values[0])
    flow_id = detail_df["flow_id"].values[0]
    
    # Return as downloadable file
    return dict(
        content=pcap_data,
        base64=True,
        filename=f"flow_{flow_id}.pcap",
        type="application/vnd.tcpdump.pcap"
    )


@callback(
    Output("unseen_grid", "rowData"),
    Output("world-map-inbox", "figure"),
    Input("time-scatter", "clickData"),
    Input("submit-classification", "n_clicks"),
    Input("reset-grid", "n_clicks"),
    Input("world-map-inbox", "clickData"),
    Input('url', 'pathname')
)
def update_grid(clickData, n_clicks_submit, n_clicks_reset, clickData_map, pathname):
    global df
    print(clickData, n_clicks_submit, n_clicks_reset, clickData_map, pathname)
    trigger = dash.callback_context.triggered_id
    
    if trigger == "reset-grid" and n_clicks_reset:
        df_update = loop.run_until_complete(cec.get_all_flows(view="all", size=flow_nr, include_pcap=False))
        unseen_data = df_update[df_update["has_been_seen"] == False].to_dict("records")
        return unseen_data, create_world_map("world-map-inbox", pd.DataFrame(unseen_data)).figure
    
    if trigger == "submit-classification" and n_clicks_submit:
        print("Updating grid after classification...")
        df_update = loop.run_until_complete(cec.get_all_flows(view="all", size=flow_nr, include_pcap=False))
        df = df_update[df_update["has_been_seen"] == False]
        unseen_data =  df.to_dict("records")
        return unseen_data, create_world_map("world-map-inbox", pd.DataFrame(unseen_data)).figure
        
    if trigger == "time-scatter" and clickData:
        print("Updating grid based on time-scatter click...")
        unseen_data = df[df["time_bin"]==clickData["points"][0]['x']].to_dict("records")
        return unseen_data, create_world_map("world-map-inbox", pd.DataFrame(unseen_data)).figure
    
    if trigger == "world-map-inbox" and clickData_map:
        print("Updating grid based on world-map-inbox click...")
        df_lat = df[df["source_lat"]==clickData_map["points"][0]["lat"]]
        unseen_data = df_lat[df_lat["source_lon"]==clickData_map["points"][0]["lon"]].to_dict("records")
        return unseen_data, create_world_map("world-map-inbox", pd.DataFrame(unseen_data)).figure
    
    if trigger == None and pathname == "/inbox/":
        print("Updating grid based on reload...")
        df_update = loop.run_until_complete(cec.get_all_flows(view="all", size=flow_nr, include_pcap=False))
        df = df_update[df_update["has_been_seen"] == False]
        unseen_data = df.to_dict("records")
        return unseen_data, create_world_map("world-map-inbox", pd.DataFrame(unseen_data)).figure

    # Default return for initial load
    print("Default grid load...")
    return dash.no_update, dash.no_update

# Check for failed elastic connection
print("trigger is " + trigger)
if trigger == "error":
    layout = html.Div([
        dbc.Alert(
            "Could not connect to Elasticsearch. Please check your connection and try again.",
            color="danger",
            dismissable=False,
            is_open=True,
        ),
        dbc.NavLink("Refresh", href="/inbox/", style={"margin-top": "20px", "text-decoration": "underline"}, external_link=True)
    ])
elif trigger == "empty":
    layout = html.Div([
        dbc.Alert(
            "No data available yet. Wait for incoming flows.",
            color="warning",
            dismissable=False,
            is_open=True,
        ),
        dbc.NavLink("Refresh", href="/inbox/", style={"margin-top": "20px", "text-decoration": "underline"}, external_link=True)
    ])
else:    
    # Layout Components
    layout = html.Div([
        dcc.Location(id='url', refresh=True),
        dbc.Row([
            html.Div(create_welcome_alert()),
            dcc.Store(id='alert-store', data=[]),
            html.Div(id='alert-container'),
            html.Hr(),
        ], className="mt-3 mb-3"),
        dbc.Row([
            dbc.Col([display_line('time-scatter', df, "0.1min"),], width=9),
            dbc.Col([make_prediction_pie_chart("prediction_pie", df, "prediction")], width=3)
            ], className="mt-3 mb-3"),
        # Main content row
        dbc.Row([
            #make_grid(seen=False, grid_id="unseen_grid")
            # Left side - Grid
            dbc.Col([
                make_grid(df, seen=False, grid_id="unseen_grid", columns=[{"field": "timestamp"},{"field": "sensor_name"},{"field": "partner_ip"},{"field": "prediction"},{"field": "flow_id"}]),
                dbc.Button("Reset", id="reset-grid", className="ms-auto", n_clicks=None, style={"margin-top": "2px"})
            ], width=6, style={"border": "1px solid #ddd", "padding": "10px"}),  # Add border and padding for debugging
            # Right side - Pie Chart
            dbc.Col([
                create_world_map("world-map-inbox", df)
            ], width=6, style={"border": "1px solid #ddd", "padding": "10px"})  # Add border and padding for debugging
        ], style={'margin': '20px 0', 'display': 'flex', 'flex-direction': 'row'}),
        make_modal(),
    ])
