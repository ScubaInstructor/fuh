import dash
from dash import Dash, html, dcc, dash_table, Input, Output, callback, State
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

import plotly.express as px

from ..elastic_connector import CustomElasticsearchConnector
import asyncio

from .grid_components import (create_world_map, make_pie_chart, make_detailed_grid,
                            make_grid, display_line, create_boxplot)


# Initialize  Dash App
dash.register_page(__name__, path='/classified/')

# Number of flows to display
flow_nr = 10000

# Initialize Elasticsearch connector and get data
cec = CustomElasticsearchConnector()
# Load maximum possible number of flows
try:
    df = asyncio.run(cec.get_all_flows(view="seen", size=flow_nr, include_pcap=False))
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
    df = pd.DataFrame()

# Special Component Builders

# Get statistics of flow data

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

# # Callbacks

# # Add callback for accordion
# @callback(
#     Output("boxplot-content", "children"),
#     [Input("accordion", "active_item")],
#     [State('selected-row-store', 'data')]
# )
# def update_boxplot(is_open, selected_row_data):
#     if not is_open or not selected_row_data:
#         return []
#     detail_df = pd.DataFrame(selected_row_data)
#     detail_flow_df = detail_df["flow_data"].apply(pd.Series).select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1)
#     detail_flow_df = pd.concat([detail_flow_df, min_flow_data, mean_flow_data, max_flow_data, q1_flow_data, q3_flow_data],ignore_index=True)
#     detail_flow_df = detail_flow_df.div(max_flow_data.iloc[0])

#     return create_boxplot(detail_flow_df)


#First callback for modal visibility
# @callback(
#     Output("modal", "is_open"),
#     Input('seen_grid', 'selectedRows'),
#     Input("close", "n_clicks"), 
#     Input('submit-classification', 'n_clicks'),
#     State("modal", "is_open"),
#     prevent_initial_call=True
# )
# def toggle_modal(selected_rows, close_clicks, submit_clicks, is_open):

#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     print("trigger modal")
#     print(changed_id)
#     print(submit_clicks)
#     if "close" in changed_id or 'submit-classification' in changed_id:
#         print("close or submit clicked")
#         return False
#     if selected_rows:
#         print("close or submit NOT clicked")
#         return True
#     print("not in if")
#     return dash.no_update

# # Second callback for modal content
# @callback(
#     Output("modal-body", "children"),
#     Input('seen_grid', 'selectedRows')
# )
# def update_modal_content(selected_rows):
#     detail_df = pd.DataFrame(selected_rows)
#     # detail_flow_df = detail_df["flow_data"].apply(pd.Series).select_dtypes(include='number').drop(["src_port", "dst_port", "protocol"], axis=1)
#     # detail_flow_df = pd.concat([detail_flow_df, min_flow_data, mean_flow_data, max_flow_data, q1_flow_data, q3_flow_data],ignore_index=True)
#     # detail_flow_df = detail_flow_df.div(max_flow_data.iloc[0])
#     #prob_data = eval(detail_df["probabilities"].iloc[0])
#     #prob_df = pd.DataFrame(list(prob_data.items()), columns=['class', 'probability'])
    
#     if not selected_rows:
#         return dash.no_update
    
#     return [
#         dcc.Store(id='selected-row-store', data=detail_df.to_dict("records")),
#         make_detailed_grid("detailed_modal_grid", selected_rows),
#         make_pie_chart("prob_pie_modal", selected_rows),
#         dbc.Accordion(
#         [
#             dbc.AccordionItem(
#                 children=[html.Div(id="boxplot-content")],  # Add container for content
#                 title="Flow Metrics",
#                 id="accordion-item"
#             ),
#         ],
#         start_collapsed=True, id="accordion"
#         ),
#         dbc.Row([
#             html.H5(children="Selected Type Classification:", className="mb-0 mb-1"),
#             dcc.Dropdown(
#                 id='attack-type-dropdown',
#                 options=[{'label': detail_df.attack_class.values[0], 
#                         'value': detail_df.attack_class.values[0]}],
#                 value=detail_df.attack_class.values[0],
#                 clearable=False,
#                 disabled=True,
#                 className='mb-3'
#             ),
#         ], className="mt-3 mb-3"),
#         ]


# @callback(
#     Output("download-pcap-content", "data"),
#     Input("download-pcap", "n_clicks"),
#     State('selected-row-store', 'data'),
#     prevent_initial_call=True
# )
# def download_pcap(n_clicks, selected_row_data):
#     if n_clicks is None:
#         return None

#     # Request pcap data for flow id
#     item = asyncio.run(cec.get_all_flows(view="all", size=1, include_pcap=True, flow_id=selected_row_data[0]["flow_id"]))
#     detail_df = pd.DataFrame(item)
#     pcap_data = detail_df["pcap_data"].values[0]
#     flow_id = detail_df["flow_id"].values[0]

#     return dict(
#         content=pcap_data,
#         filename=f"flow_{flow_id}.pcap",
#         type="application/vnd.tcpdump.pcap"
#     )

# # Callback initialization
# #create_grid_callback("seen_grid", "detailed_grid_unseen")
# #create_grid_callback("seen_grid", "detailed_grid_seen")

# @callback(
#     Output("seen_grid", "rowData"),
#     Input("time-scatter", "clickData"),
#     Input("reset-grid", "n_clicks")
# )
# def update_grid(clickData, n_clicks_reset):
#     print(clickData, n_clicks_reset)
#     trigger = dash.callback_context.triggered_id
#     print(f"Triggered by: {trigger}")
    
#     if trigger == "reset-grid" and n_clicks_reset:
#         df_update = asyncio.run(cec.get_all_flows(view="all", size=flow_nr, include_pcap=False))
#         return df_update[df_update["has_been_seen"] == False].to_dict("records")
    
#     if trigger == "time-scatter" and clickData:
#         print("Updating grid based on time-scatter click...")
#         return df[df["time_bin"]==clickData["points"][0]['x']].to_dict("records")
    
#     # Default return for initial load
#     print("Default grid load...")
#     return dash.no_update


# Check for failed elastic connection
if df.empty:
    layout = html.Div([
        dbc.Alert(
            "Could not connect to Elasticsearch. Please check your connection and try again.",
            color="danger",
            dismissable=False,
            is_open=True,
        ),
        dbc.NavLink("Refresh", href="/classified/", style={"margin-top": "20px", "text-decoration": "underline"})
    ])
else:
    print("normal layout")    
    # Layout Components
    layout = html.Div([
        dbc.Row([
            html.Hr(),
        ], className="mt-3 mb-3"),
        dbc.Row([], className="mt-3 mb-3"),
        # Main content row
        dbc.Row([
            #make_grid(seen=False, grid_id="seen_grid")
            # Left side - Grid
            dbc.Col([
                make_grid(df, seen=True, grid_id="seen_grid", columns=[{"field": "timestamp"},{"field": "sensor_name"},{"field": "partner_ip"},{"field": "prediction"},{"field": "attack_class"},{"field": "flow_id"}]),
                dbc.Button("Reset", id="reset-grid", className="ms-auto", n_clicks=None, style={"margin-top": "2px"})
            ], width=6, style={"border": "1px solid #ddd", "padding": "10px"}),  # Add border and padding for debugging
            # Right side - Pie Chart
            dbc.Col([
                create_world_map(df)
            ], width=6, style={"border": "1px solid #ddd", "padding": "10px"})  # Add border and padding for debugging
        ], style={'margin': '20px 0', 'display': 'flex', 'flex-direction': 'row'}),
        make_modal(),
    ])
