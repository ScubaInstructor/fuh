import asyncio
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State
from .utils import generate_env_file_for_sensors, get_secret_key
from ..models import User, db, Sensor
from ..elastic_connector import CustomElasticsearchConnector
import dash_ag_grid as dag
from flask import current_app
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .. import mc, restore_model_to_previous_version, cec
from ..model_visualisations import Model_Visualisator
from elasticsearch.exceptions import ConnectionError

dash.register_page(__name__, path="/admin/")
mv = Model_Visualisator()


def user_management_content():
    with current_app.app_context():
        users = User.query.all()
        users_list = [{"username": user.username, "role": user.role} for user in users]

    return html.Div([
        html.H3("User Management"),
        dag.AgGrid(
            id="users-grid",
            rowData=users_list,
            columnDefs=[
                {
                    "field": "select",
                    "headerName": "",
                    "checkboxSelection": True,
                    "headerCheckboxSelection": True,
                    "width": 50
                },
                {
                    "field": "username", 
                    "sortable": True, 
                    "filter": True,
                    "editable": False
                },
                {
                    "field": "role", 
                    "sortable": True, 
                    "filter": True,
                    "editable": False,
                    "cellEditor": "agSelectCellEditor",
                    "cellEditorParams": {
                        "values": ["user", "admin"]
                    }
                },
                {
                    "field": "password",
                    "editable": False,
                    "cellRenderer": "passwordRenderer",
                    "hide": True
                },
            ],
            defaultColDef={
                "resizable": True,
                "sortable": True,
                "filter": True
            },
            dashGridOptions={
                "pagination": True,
                "paginationAutoPageSize": True,
                "rowSelection": "single",
                "deltaRowDataMode": True
            },
            getRowId="params.data.username",
            style={"height": 400}
        ),
        dbc.Button("Delete Selected", id="delete-selected-btn", color="danger", className="mt-3"),
        dbc.Button("Add New User", id="add-user-btn", className="mt-3 ms-2"),  # Added margin-start
        dbc.Button("Modify User", id="modify-user-btn", className="mt-3 ms-2"),
        html.Div(id="user-update-status"),
        
        # Add Modal for new user
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle(id="user-modal-title")),
            dbc.ModalBody([
                dbc.Form([
                    dbc.Row([
                        dbc.Label("Username", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text",
                                id="new-user-name",
                                placeholder="Enter username"
                            ),
                            width=10,
                        ),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Label("Password", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="password",
                                id="new-user-password",
                                placeholder="Enter password (leave empty to keep current)"
                            ),
                            width=10,
                        ),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Label("Role", width=2),
                        dbc.Col(
                            dbc.Select(
                                id="new-user-role",
                                options=[
                                    {"label": "User", "value": "user"},
                                    {"label": "Admin", "value": "admin"}
                                ],
                                value="user"
                            ),
                            width=10,
                        ),
                    ], className="mb-3"),
                ])
            ]),
            dbc.ModalFooter([
                dbc.Button("Close", id="add-user-close", className="ms-auto", n_clicks=0),
                dbc.Button("Save", id="add-user-save", className="ms-2", color="primary", n_clicks=0),
            ]),
        ], id="add-user-modal", is_open=False),
        dcc.Store(id='edit-user-data'),
    ])

# Add new callback for modal
@callback(
    [Output("add-user-modal", "is_open"),
     Output("user-modal-title", "children"),
     Output("new-user-name", "value"),
     Output("new-user-role", "value"),
     Output("new-user-name", "disabled"),
     Output("edit-user-data", "data")],
    [Input("add-user-btn", "n_clicks"),
     Input("modify-user-btn", "n_clicks"),
     Input("add-user-close", "n_clicks"),
     Input("add-user-save", "n_clicks")],
    [State("add-user-modal", "is_open"),
     State("users-grid", "selectedRows")]
)
def toggle_modal(n1, n2, n3, n4, is_open, selected_rows):
    ctx = dash.callback_context
    if not ctx.triggered:
        return False, "", None, "user", False, None
        
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "add-user-btn":
        return True, "Add New User", "", "user", False, None
    elif button_id == "modify-user-btn" and selected_rows:
        user = selected_rows[0]
        return True, "Modify User", user['username'], user['role'], True, user
    elif button_id in ["add-user-close", "add-user-save"]:
        return False, "", None, "user", False, None
    
    return is_open, "", None, "user", False, None

# Modify the existing manage_users callback
@callback(
    [Output("users-grid", "rowData"),
     Output("user-update-status", "children")],
    [Input("delete-selected-btn", "n_clicks"),
     Input("add-user-save", "n_clicks")],
    [State("users-grid", "selectedRows"),
     State("new-user-name", "value"),
     State("new-user-password", "value"),
     State("new-user-role", "value"),
     State("edit-user-data", "data")]
)
def manage_users(delete_clicks, save_clicks, selected_rows, username, password, role, edit_data):
    trigger = dash.callback_context.triggered_id
    if not trigger:
        return dash.no_update, dash.no_update
    
    try:
        with current_app.app_context():
            if trigger == "delete-selected-btn" and selected_rows:
                for row in selected_rows:
                    user = User.query.filter_by(username=row['username']).first()
                    if user:
                        db.session.delete(user)
                db.session.commit()
                
            elif trigger == "add-user-save":
                if edit_data:  # Modify existing user
                    user = User.query.filter_by(username=username).first()
                    if user:
                        if password:  # Only update password if provided
                            user.set_password(password)
                        user.role = role
                        db.session.commit()
                else:  # Add new user
                    if not username or not password:
                        return dash.no_update, "Username and password are required"
                    user = User(username=username, role=role)
                    user.set_password(password)
                    db.session.add(user)
                    db.session.commit()
            
            # Refresh user list
            users = User.query.all()
            users_list = [{"username": user.username, "role": user.role} for user in users]
            return users_list, "Operation completed successfully"
            
    except Exception as e:
        return dash.no_update, f"Error: {str(e)}"


def model_management_content():
    # return html.Div([
    #     html.H3("Model Management"),
    #     # Add model management components here
    # ])
    try:
        import asyncio
        from ..elastic_connector import CustomElasticsearchConnector

        cec = CustomElasticsearchConnector()
        model_properties = asyncio.run(cec.get_all_model_properties(size=1000))
        if len(model_properties) == 0:
            return html.Div("No models found in Elasticsearch.", style={"color": "red"})
        box_plot_df = model_properties.sort_values(by="timestamp")
        box_plot_df = box_plot_df.head(10)
        model_list = model_properties.to_dict("records")

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(
                x=model_properties["timestamp"],
                y=model_properties["score"],
                mode="lines+markers",
                name="Accuracy",
            ),
            secondary_y=False,  # left y-achsis
        )

        # adds the line "own_flow_count"
        fig.add_trace(
            go.Scatter(
                x=model_properties["timestamp"],
                y=model_properties["own_flow_count"],
                mode="lines+markers",
                name="Own Flow Count",
            ),
            secondary_y=True,  # Rechte y-Achse
        )

        # title and labels
        fig.update_layout(
            xaxis_rangeslider_visible=True,
            title="Score and Own Flow Count Over Time",
            xaxis_title="Timestamp",
            yaxis_title="Accuracy",  # left achsis title
            yaxis2_title="Own Flow Count",  # right achsis title
        )

        return html.Div(
            [
                html.H3("Model Management"),
                dag.AgGrid(
                    id="models-grid",
                    rowData=model_list,
                    columnDefs=[
                        {
                            "field": "model_hash",
                            "headerName": "Model Hash",
                            "sortable": True,
                            "filter": True,
                        },
                        {
                            "field": "score",
                            "headerName": "Score",
                            "sortable": True,
                            "filter": True,
                        },
                        {
                            "field": "timestamp",
                            "headerName": "Timestamp",
                            "sortable": True,
                            "filter": True,
                        },
                        {
                            "field": "own_flow_count",
                            "headerName": "Own Flow Count",
                            "sortable": True,
                            "filter": True,
                        },
                    ],
                    defaultColDef={"resizable": True, "sortable": True, "filter": True},
                    dashGridOptions={
                        "pagination": True,
                        "paginationAutoPageSize": True,
                        "rowSelection": "single",
                        "onRowClicked": {
                            "function": "onRowClicked"
                        },  # Function to open dialog
                    },
                    style={"height": 400},
                ),
                dcc.Graph(figure=fig),
                dcc.Graph(figure=mv.create_boxplot_for_all_models(box_plot_df)),
                html.Div(id="model-management-status"),
                dcc.Store(id="selected-model-data"),  # Saves the selected model data
                dbc.Modal(  # Add the Modal-Dialog
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Restore Model?")),
                        dcc.Graph(id="confusion-matrix-figure"),
                        dcc.Graph(id="model-metrics"),
                        dbc.ModalBody("Do you want to restore this model?"),
                        dbc.ModalFooter(
                            [
                                dbc.Button(
                                    "Delete",
                                    id="delete-model-button",
                                    color="danger",
                                    className="me-auto",
                                ),  # Delete Button left
                                dbc.Button(
                                    "No",
                                    id="modal-close-button",
                                    color="secondary",
                                    className="ms-2",
                                ),
                                dbc.Button(
                                    "Yes",
                                    id="restore-model-button",
                                    color="success",
                                    className="ms-2",
                                ),
                            ]
                        ),
                    ],
                    id="restore-model-modal",
                    is_open=False,
                ),
            ]
        )
    except ConnectionError as ce:
        return html.Div(
            f"Could not connect to Elasticsearch. Please check your connection and try again.",
            style={"color": "red"},
        )
    except Exception as e:
        return html.Div(f"Error fetching model data: {str(e)}", style={"color": "red"})


def sensor_management_content():
    with current_app.app_context():
        sensors = Sensor.query.all()
        sensors_list = [
            {
                "name": sensor.name,
                "created_at": sensor.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for sensor in sensors
        ]

    return html.Div(
        [
            html.H3("Sensor Management"),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Input(
                                id="sensor-name-input",
                                placeholder="Enter sensor name",
                                type="text",
                            ),
                            dbc.Button(
                                "Create Sensor",
                                id="submit-sensor",
                                color="primary",
                                className="mt-2",
                            ),
                            html.Div(id="sensor-submit-output"),
                            dcc.Download(id="download-sensor"),
                        ],
                        width=4,
                    ),
                ]
            ),
            html.Hr(),
            dag.AgGrid(
                id="sensors-grid",
                rowData=sensors_list,
                columnDefs=[
                    {
                        "field": "select",
                        "headerName": "",
                        "checkboxSelection": True,
                        "headerCheckboxSelection": True,
                        "width": 50,
                    },
                    {"field": "id", "hide": True},
                    {"field": "name", "sortable": True, "filter": True},
                    {"field": "created_at", "sortable": True, "filter": True},
                ],
                defaultColDef={"resizable": True, "sortable": True, "filter": True},
                dashGridOptions={
                    "pagination": True,
                    "paginationAutoPageSize": True,
                    "rowSelection": "multiple",
                    "deltaRowDataMode": True,
                },
                getRowId="params.data.id",
                style={"height": 400},
            ),
            dbc.Button(
                "Delete Selected",
                id="delete-selected-sensor-btn",
                color="danger",
                className="mt-3",
            ),
            html.Div(id="sensor-update-status"),
        ]
    )


@callback(
    [
        Output("sensor-name-input", "invalid"),
        Output("sensor-submit-output", "children"),
        Output("download-sensor", "data"),
        Output("sensors-grid", "rowData"),
        Output("sensor-update-status", "children"),
    ],
    [
        Input("submit-sensor", "n_clicks"),
        Input("delete-selected-sensor-btn", "n_clicks"),
    ],
    [
        State("sensor-name-input", "value"),
        State("sensors-grid", "selectedRows"),
        State("sensors-grid", "rowData"),
    ],
    prevent_initial_call=True,
)
def manage_sensors(
    submit_clicks, delete_clicks, sensor_name, selected_rows, current_rows
):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False, dash.no_update, None, dash.no_update, dash.no_update

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Handle Sensor Creation
    if trigger_id == "submit-sensor":
        if not sensor_name:
            return (
                True,
                "Please enter a sensor name",
                None,
                dash.no_update,
                dash.no_update,
            )
        if not sensor_name.replace("_", "").isalnum():
            return (
                True,
                "Invalid sensor name format",
                None,
                dash.no_update,
                dash.no_update,
            )

        try:
            with current_app.app_context():
                new_sensor = Sensor(name=sensor_name)
                db.session.add(new_sensor)
                db.session.commit()

                # Get updated sensor list
                sensors = Sensor.query.all()
                sensors_list = [
                    {
                        "id": s.id,
                        "name": s.name,
                        "created_at": s.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    for s in sensors
                ]

            sensor_env = generate_env_file_for_sensors(sensor_name)
            dl_content = dict(
                content=sensor_env, filename=f"{sensor_name}.env", type=".env"
            )
            return (
                False,
                f"Sensor {sensor_name} created successfully",
                dl_content,
                sensors_list,
                dash.no_update,
            )

        except Exception as e:
            return (
                True,
                f"Error creating sensor: {str(e)}",
                None,
                dash.no_update,
                f"Error: {str(e)}",
            )

    # Handle Sensor Deletion
    elif trigger_id == "delete-selected-sensor-btn" and selected_rows:
        try:
            with current_app.app_context():
                for row in selected_rows:
                    sensor_id = row["id"]
                    sensor = Sensor.query.get(sensor_id)
                    if sensor:
                        db.session.delete(sensor)
                db.session.commit()

                sensors = Sensor.query.all()
                sensors_list = [
                    {
                        "id": s.id,
                        "name": s.name,
                        "created_at": s.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    for s in sensors
                ]
            return (
                False,
                dash.no_update,
                None,
                sensors_list,
                "Sensors deleted successfully",
            )

        except Exception as e:
            return False, dash.no_update, None, dash.no_update, f"Error: {str(e)}"

    # No action
    return False, dash.no_update, None, dash.no_update, dash.no_update



@callback(Output("admin-content", "children"), Input("url", "search"))
def update_admin_content(search):
    if search == "?section=users":
        return user_management_content()
    elif search == "?section=models":
        return model_management_content()
    elif search == "?section=sensors":
        return sensor_management_content()
    return html.P("Please select a section from the menu.")


layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Nav(
                            [
                                dbc.NavLink(
                                    "User Management",
                                    href="/admin?section=users",
                                    active="exact",
                                    style={
                                        "width": "100%",
                                        "textAlign": "left",
                                        "padding": "10px 15px",
                                        "marginBottom": "2px",
                                    },
                                    className="text-dark bg-light",
                                ),
                                dbc.NavLink(
                                    "Sensor Management",
                                    href="/admin?section=sensors",
                                    active="exact",
                                    style={
                                        "width": "100%",
                                        "textAlign": "left",
                                        "padding": "10px 15px",
                                        "marginBottom": "2px",
                                    },
                                    className="text-dark bg-light",
                                ),
                                dbc.NavLink(
                                    "Model Management",
                                    href="/admin?section=models",
                                    active="exact",
                                    style={
                                        "width": "100%",
                                        "textAlign": "left",
                                        "padding": "10px 15px",
                                        "marginBottom": "2px",
                                    },
                                    className="text-dark bg-light",
                                ),
                            ],
                            vertical=True,
                            pills=True,
                            style={
                                "backgroundColor": "#f8f9fa",
                                "padding": "10px",
                                "borderRadius": "5px",
                                "width": "100%",
                            },
                            className="nav-pills-custom",
                        ),
                    ],
                    width=3,
                ),
                dbc.Col([html.Div(id="admin-content")], width=9),
            ]
        ),
    ]
)


@dash.callback(
    Output("restore-model-modal", "is_open"),
    [
        Input("models-grid", "cellClicked"),
        Input("modal-close-button", "n_clicks"),
        Input("restore-model-button", "n_clicks"),
        Input("delete-model-button", "n_clicks"),
    ],
    [State("restore-model-modal", "is_open")],
)
def toggle_restore_model_modal(
    cell_clicked, close_clicks, restore_clicks, delete_clicks, is_open
):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "models-grid" and cell_clicked:
        return True
    elif (
        button_id == "modal-close-button"
        or button_id == "restore-model-button"
        or button_id == "delete-model-button"
    ):
        return False
    else:
        return is_open


@dash.callback(
    Output("model-management-status", "children"),
    [
        Input("restore-model-button", "n_clicks"),
        Input("delete-model-button", "n_clicks"),
    ],
    [State("selected-model-data", "data"), State("models-grid", "selectedRows")],
)
def manage_model(restore_clicks, delete_clicks, selected_model_data, selectedRows_data):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "restore-model-button":
        if restore_clicks is None:
            return dash.no_update

        if selected_model_data:
            model_hash = selected_model_data["model_hash"]
            elastic_id = asyncio.run(cec.get_model_uuid(hash=model_hash))
            restore_model_to_previous_version(elastic_id=elastic_id, mc=mc)
            return f"Restored model with hash: {model_hash}"
        else:
            return "No model selected."

    elif trigger_id == "delete-model-button":
        if delete_clicks is None:
            return dash.no_update

        if selectedRows_data:
            model_hash = selectedRows_data[0]["model_hash"]
            if asyncio.run(cec.delete_model_by_hash(model_hash)):
                return f"Deleted model with hash: {model_hash}"
            else:
                return f"Error deleting model with hash: {model_hash}"
        else:
            return "No model selected."


@dash.callback(
    Output("selected-model-data", "data"),
    Output("confusion-matrix-figure", "figure"),
    Output("model-metrics", "figure"),
    Input("models-grid", "cellClicked"),
    State("models-grid", "rowData"),
    State("models-grid", "selectedRows"),
)
def store_selected_data(cell_clicked, row_data, selectedRows_data):
    if cell_clicked:
        row_index = cell_clicked["rowIndex"]
        selected_row = row_data[row_index]
        confusion_matrix_data = selected_row["confusion_matrix"]
        confusion_matrix_figure = mv.create_confusion_matrix_figure_from_elastic_data(
            confusion_matrix_data
        )
        model_classes = mv.extract_class_names(confusion_matrix_data)
        class_metric_figure = mv.create_metrics_overview_from_elastic_data(
            selected_row["class_metric_data"], model_classes
        )
        return selected_row, confusion_matrix_figure, class_metric_figure

    return None, dash.no_update, dash.no_update
