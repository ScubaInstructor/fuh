import dash
from dash import Dash, html, dcc, dash_table, Input, Output, callback, State
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from flask_login import current_user
import plotly.express as px
from ..models import User, db
from ..retrainer import retrain
from .. import mc
from .. import app
import geoip2.database


from ..elastic_connector import CustomElasticsearchConnector
import asyncio

from .grid_components import (create_world_map, make_pie_chart, make_detailed_grid,
                            make_grid, create_boxplot, make_prediction_pie_chart)


# Initialize  Dash App
dash.register_page(__name__, path='/classified/')

def is_admin():
    try:
        if current_user.is_authenticated:
            print(f"User authenticated: {current_user.username}")
            print(f"User role: {current_user.role}")
            return True
        return False
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False

# Number of flows to display
flow_nr = 10000

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
# Initialize Elasticsearch connector and get data
cec = CustomElasticsearchConnector()
# Load maximum possible number of flows
try:
    print("reloaded")
    df = asyncio.run(cec.get_all_flows(view="seen", size=flow_nr, include_pcap=False))
    print(df)
    if df.empty:
        trigger = "empty"
    else:
        # Normal behaviour trigger
        trigger = "normal"
        flow_data = df["flow_data"].apply(pd.Series)
        # min_flow_data = flow_data.select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1).min()
        # max_flow_data = flow_data.select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1).max()
        # mean_flow_data = flow_data.select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1).mean()
        # q1_flow_data = flow_data.select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1).quantile([0.25])
        # q3_flow_data = flow_data.select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1).quantile([0.75])

        # min_flow_data = pd.DataFrame([min_flow_data], columns=mean_flow_data.index.to_list())
        # max_flow_data = pd.DataFrame([max_flow_data], columns=mean_flow_data.index.to_list())
        # mean_flow_data = pd.DataFrame([mean_flow_data], columns=mean_flow_data.index.to_list())
        # q1_flow_data = pd.DataFrame([q1_flow_data], columns=q1_flow_data.index.to_list())
        # q3_flow_data = pd.DataFrame([q3_flow_data], columns=q3_flow_data.index.to_list())
        
except Exception as e:
    trigger = "error"
    df = pd.DataFrame()

# Special Component Builders

# Get statistics of flow data

def make_modal():
    return dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Detailed Flow View")),
                dbc.ModalBody("This is the content of the modal", id="classified-modal-body"),
                dbc.ModalFooter([
                    dbc.Button(
                        "Submit Classification", 
                        id="classified-submit-classification", 
                        color="primary",
                        className="mt-2",
                        n_clicks=None
                    ),
                    dbc.Button(
                        "Download PCAP", 
                        id="classified-download-pcap", 
                        color="primary",
                        className="mt-2",
                        n_clicks=None
                    ),
                    dcc.Download(id="classified-download-pcap-content"),
                    dbc.Button("Close", id="classified-close", className="ms-auto", n_clicks=None)
                ]),
            ],
            id="classified-modal",
            size="xl",
            is_open=False,
        )

# # Callbacks

# Add callback for accordion
@callback(
    Output("classified-boxplot-content", "children"),
    [Input("classified-accordion", "active_item")],
    [State('classified-selected-row-store', 'data')]
)
def update_boxplot(is_open, selected_row_data):
    if not is_open or not selected_row_data:
        return []
    detail_df = pd.DataFrame(selected_row_data)
    detail_flow_df = detail_df["flow_data"].apply(pd.Series).select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1)
    # detail_flow_df = pd.concat([detail_flow_df, min_flow_data, mean_flow_data, max_flow_data, q1_flow_data, q3_flow_data],ignore_index=True)
    # detail_flow_df = detail_flow_df.div(max_flow_data.iloc[0])

    return create_boxplot(detail_flow_df, detail_df.prediction.values[0])


# First callback for modal visibility
@callback(
    Output("classified-modal", "is_open"),
    Input('seen_grid', 'selectedRows'),
    Input("classified-close", "n_clicks"), 
    Input('classified-submit-classification', 'n_clicks'),
    State("classified-modal", "is_open"),
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

# # Second callback for modal content
@callback(
    Output("classified-modal-body", "children"),
    Input('seen_grid', 'selectedRows')
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
        dcc.Store(id='classified-selected-row-store', data=detail_df.to_dict("records")),
        make_detailed_grid("classified-detailed-modal-grid", selected_rows),
        make_pie_chart("classified-prob-pie-modal", selected_rows),
        dbc.Accordion(
        [
            dbc.AccordionItem(
                children=[html.Div(id="classified-boxplot-content")],  # Add container for content
                title="Flow Metrics",
                id="classified-accordion-item"
            ),
        ],
        start_collapsed=True, id="classified-accordion"
        ),
        dbc.Row([
            html.H5(children="Selected Attack Type Classification", className="mb-0 mb-1"),
            dcc.Dropdown(
                id='classified-attack-type-dropdown',
                options=list(df.probabilities.values[0].keys()),
                value=detail_df.attack_class.values[0],
                clearable=False,
                className='mb-3'
            ),
        ], className="mt-3 mb-3"),
        ]

@callback(
    Output("classified-download-pcap-content", "data"),
    Input("classified-download-pcap", "n_clicks"),
    State('classified-selected-row-store', 'data'),
    prevent_initial_call=True
)
def download_pcap(n_clicks, selected_row_data):
    if n_clicks is None:
        return None

    # Request pcap data for flow id
    item = asyncio.run(cec.get_all_flows(view="all", size=1, include_pcap=True, flow_id=selected_row_data[0]["flow_id"]))
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
    Output("seen_grid", "rowData"),
    Output("world-map-classified", "figure"),
    Input("classified-submit-classification", "n_clicks"),
    Input("classified-reset-grid", "n_clicks"),
    Input("world-map-classified", "clickData"),
    State('df_with_location_classified', 'data'),
    State('classified-attack-type-dropdown', 'value'),
    State('classified-selected-row-store', 'data')
)
def update_grid(n_clicks_submit, n_clicks_reset, clickData_map, df_with_location_classified_data, selected_type_value, selected_row_data):
    print( n_clicks_reset)
    trigger = dash.callback_context.triggered_id
    print(f"Triggered by: {trigger}")
    
    if trigger == "classified-reset-grid" and n_clicks_reset:
        df_update = asyncio.run(cec.get_all_flows(view="seen", size=flow_nr, include_pcap=False))
        seen_data = df_update[df_update["has_been_seen"] == True].to_dict("records")
        return seen_data, create_world_map("world-map-classified", pd.DataFrame(seen_data)).figure
    
    if trigger == "classified-submit-classification" and n_clicks_submit:
        print("Updating grid after classification...")   
        # Reclassification
        detail_df = pd.DataFrame(selected_row_data)
        flow_id = detail_df["flow_id"].values[0]

        try:
            asyncio.run(cec.set_attack_class(flow_id=flow_id, attack_class=selected_type_value))

        except:
            print(f'Flow {flow_id} could not be classified. Elastic Database Error.')
        
        df_update = asyncio.run(cec.get_all_flows(view="all", size=flow_nr, include_pcap=False))
        seen_data = df_update[df_update["has_been_seen"] == True].to_dict("records")
        return seen_data, create_world_map("world-map-classified", pd.DataFrame(seen_data)).figure
    
    # Updating based on selection on the map
    if trigger == "world-map-classified" and clickData_map:
        print("Updating grid based on world-map-classified click...")
        df = pd.DataFrame(df_with_location_classified_data)
        df_lat = df[df["source_lat"] == clickData_map["points"][0]["lat"]]
        df_lon = df_lat[df_lat["source_lon"] == clickData_map["points"][0]["lon"]]
        clickData_map = None
        seen_data = df_lon[df_lon["has_been_seen"] == True].to_dict("records")
        return seen_data, create_world_map("world-map-classified", pd.DataFrame(seen_data)).figure
    
    # Default return for initial load
    print("Default grid load...")
    return dash.no_update

@callback(
    Output("retrain-button", "children"),
    Input("url", "pathname")
)
def update_retrain_button(search):
    if is_admin():
        return dbc.Button("Retrain Model", id="retrain-model", color="primary", className="mt-2", n_clicks=None)

@callback(
    [Output("retrain-status", "children"),
     Output("retrain-model", "disabled")],
    Input("retrain-model", "n_clicks"),
    prevent_initial_call=True
)
def retrain_model(n_clicks):
    if not n_clicks:
        return dash.no_update, dash.no_update
    try:
        mc.set_hash(retrain())
        return html.Div("Model retrained successfully!", style={"color": "green"}), False
    except Exception as e:
        return html.Div(f"Error retraining model: {str(e)}", style={"color": "red"}), False

# # Add new callback for refresh
# @callback(
#     [Output("url-refresh", "pathname"),
#      Output("url-refresh", "refresh")],  # Add refresh output
#     Input("refresh-button", "n_clicks"),
#     prevent_initial_call=True
# )
# def refresh_page(n_clicks):
#     if n_clicks:
#         # Force reload data from Elasticsearch
       
#         try:
            
#             return "/classified/", True  # Force page refresh
#         except Exception as e:
#             print(f"Error refreshing data: {e}")
#             return dash.no_update, dash.no_update
#     return dash.no_update, dash.no_update


# @callback(
#     [Output("url-refresh", "pathname"),
#      Output("url-refresh", "refresh")],
#     Input("refresh-button", "n_clicks"),
#     prevent_initial_call=True,
#     clientside=True  # Add this parameter
# )
# def refresh_page(n_clicks):
#     return """
#     function(n_clicks) {
#         if (n_clicks) {
#             window.location.reload(true);
#             return ['/classified/', true];
#         }
#         return [window.dash_clientside.no_update, window.dash_clientside.no_update];
#     }
#     """

# Replace the existing layout code with this basic layout
layout = html.Div([
    dcc.Location(id="url", refresh=False),
    # dcc.Interval(id="interval-classified", interval=100, max_intervals=1),
    html.Div(id="classified-page-content-container"),
    dcc.Store(id='df_with_location_classified')
])

# Add new callback to serve the main content
@callback(
    Output("classified-page-content-container", "children"),
    Output("df_with_location_classified", "data"),
    [#Input("interval-classified", "n_intervals"),
    #  Input("refresh-button", "n_clicks"),
     Input("url", "pathname")],  # Changed to use regular url instead of url-refresh
    prevent_initial_call=False
)
def serve_layout(pathname):

    print(f"pathname: {pathname}")
    
    
    if pathname == "/classified/":
        # Always reload data for any trigger
        try:
            print("Reloading data from Elasticsearch")
            df = asyncio.run(cec.get_all_flows(view="seen", size=flow_nr, include_pcap=False))
            if df.empty:
                trigger = "empty"
            else:
                trigger = "normal"

                # Get Map
                reader = geoip2.database.Reader('flask_dash_app/app/GeoLite2-City.mmdb')
                # add lat and long
                def ip_to_lat_lon(ip):
                    try:
                        response = reader.city(ip)
                        return response.location.latitude, response.location.longitude
                    except:
                        return None, None
                df['source_lat'], df['source_lon'] = zip(*df['dst_ip'].apply(ip_to_lat_lon))
                # Recalculate flow statistics
                flow_data = df["flow_data"].apply(pd.Series)
                # min_flow_data = flow_data.select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1).min()
                # max_flow_data = flow_data.select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1).max()
                # mean_flow_data = flow_data.select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1).mean()
        except Exception as e:
            print(f"Error loading data: {e}")
            trigger = "error"
            df = pd.DataFrame()

        if trigger == "error":
            return dbc.Container([
                dbc.Alert(
                    "Could not connect to Elasticsearch. Please check your connection and try again.",
                    color="danger",
                    dismissable=False,
                    is_open=True,
                ),
                dbc.Button(
                    "Refresh Data",
                    id="refresh-button",
                    color="primary",
                    className="mt-3", 
                    href="/classified/",
                    external_link=True
                )
            ], fluid=True, className="px-0 mx-0"), df.to_dict("records")
        
        elif trigger == "empty":
            return dbc.Container([
                dbc.Alert(
                    "No classified flows available yet.",
                    color="warning",
                    dismissable=False,
                    is_open=True,
                ),
                dbc.Button(
                    "Refresh Data",
                    id="refresh-button",
                    color="primary",
                    className="mt-3", 
                    href="/classified/",
                    external_link=True
                )
            ], fluid=True, className="px-0 mx-0"), df.to_dict("records")
        
        else:
            return dbc.Container([
                dbc.Row([
                    html.Hr(),
                ], className="mt-3 mb-3"),
                dbc.Row([make_prediction_pie_chart("prediction_pie", df, "attack_class")], 
                    className="mt-3 mb-3"),
                dbc.Row([
                    dbc.Col([
                        make_grid(df, seen=True, grid_id="seen_grid", 
                                columns=[{"field": "timestamp"},
                                    {"field": "sensor_name"},
                                    {"field": "src_ip"},
                                    {"field": "dst_ip"},
                                    {"field": "attack_class"},
                                    {"field": "flow_id"}]),
                        dbc.Button("Reset", id="classified-reset-grid", 
                                className="ms-auto", n_clicks=None, 
                                style={"margin-top": "2px"}),
                        html.Div(id="retrain-button"),
                        html.Div(id="retrain-status")
                    ], width=6, style={"border": "1px solid #ddd", "padding": "10px"}),
                    dbc.Col([
                        create_world_map("world-map-classified", df)
                    ], width=6, style={"border": "1px solid #ddd", "padding": "10px"})
                ], style={'margin': '20px 0', 'display': 'flex', 'flex-direction': 'row'}),
                make_modal(),
            ], fluid=True, className="px-0 mx-0"), df.to_dict("records")
    else:
        dash.no_update, dash.no_update