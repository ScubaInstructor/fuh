import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State
from .utils import generate_env_file_for_sensors, get_secret_key
from ..models import User, db, Sensor
import dash_ag_grid as dag
from flask import current_app

dash.register_page(__name__, path='/admin/')

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
                    "editable": True
                },
                {
                    "field": "role", 
                    "sortable": True, 
                    "filter": True,
                    "editable": True,
                    "cellEditor": "agSelectCellEditor",
                    "cellEditorParams": {
                        "values": ["user", "admin"]
                    }
                },
                {
                    "field": "password",
                    "editable": True,
                    "cellRenderer": "passwordRenderer",
                    "hide": False
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
                "rowSelection": "multiple",
                "deltaRowDataMode": True
            },
            getRowId="params.data.username",
            style={"height": 400}
        ),
        dbc.Button("Delete Selected", id="delete-selected-btn", color="danger", className="mt-3"),
        dbc.Button("Add New User", id="add-user-btn", className="mt-3"),
        html.Div(id="user-update-status")
    ])


def model_management_content():
    return html.Div([
        html.H3("Model Management"),
        # Add model management components here
    ])

def sensor_management_content():
    with current_app.app_context():
        sensors = Sensor.query.all()
        sensors_list = [{"name": sensor.name, "created_at": sensor.created_at.strftime("%Y-%m-%d %H:%M:%S")} for sensor in sensors]

    return html.Div([
        html.H3("Sensor Management"),
        dbc.Row([
            dbc.Col([
                dbc.Input(id="sensor-name-input", placeholder="Enter sensor name", type="text"),
                dbc.Button("Create Sensor", id="submit-sensor", color="primary", className="mt-2"),
                html.Div(id="sensor-submit-output"),
                dcc.Download(id="download-sensor")
            ], width=4),
        ]),
        html.Hr(),
        dag.AgGrid(
            id="sensors-grid",
            rowData=sensors_list,
            columnDefs=[
                {"field": "name", "sortable": True, "filter": True},
                {"field": "created_at", "sortable": True, "filter": True}
            ],
            defaultColDef={"resizable": True},
            dashGridOptions={"pagination": True},
            style={"height": 400}
        )
    ])

@callback(
    [Output("sensor-name-input", "invalid"),
     Output("sensor-submit-output", "children"),
     Output("download-sensor", "data"),
     Output("sensors-grid", "rowData")],
    Input("submit-sensor", "n_clicks"),
    State("sensor-name-input", "value"),
    prevent_initial_call=True
)
def submit_sensor(n_clicks, sensor_name):
    if not sensor_name:
        return True, "Please enter a sensor name", None, dash.no_update
    if not sensor_name.replace('_', '').isalnum():
        return True, "Invalid sensor name format", None, dash.no_update
        
    try:
        with current_app.app_context():
            new_sensor = Sensor(name=sensor_name)
            db.session.add(new_sensor)
            db.session.commit()
            
            # Get updated sensor list
            sensors = Sensor.query.all()
            sensors_list = [{"name": s.name, "created_at": s.created_at.strftime("%Y-%m-%d %H:%M:%S")} for s in sensors]
            
        sensor_env = generate_env_file_for_sensors(sensor_name)
        dl_content = dict(
            content=sensor_env,
            filename=f"{sensor_name}.env",
            type=".env"
        )
        return False, f"Sensor {sensor_name} created successfully", dl_content, sensors_list
    except Exception as e:
        return True, f"Error creating sensor: {str(e)}", None, dash.no_update

# @callback(
#     [Output("users-grid", "rowData"),
#      Output("user-update-status", "children")],
#     [Input("delete-selected-btn", "n_clicks")],
#     #State("users-grid", "selectedRows"),
#     prevent_initial_call=True
# )
# def delete_selected_users(n_clicks):#, selected_rows):
#     print("sss")
#     return dash.no_update, dash.no_update
#     if not selected_rows:
#         return dash.no_update, dash.no_update
    
#     try:
#         with current_app.app_context():
#             for row in selected_rows:
#                 user = User.query.filter_by(username=row['username']).first()
#                 if user:
#                     db.session.delete(user)
#             db.session.commit()
            
#             users = User.query.all()
#             users_list = [{"username": user.username, "role": user.role} for user in users]
#             return users_list, html.Div("Users deleted successfully", style={"color": "green"})
            
#     except Exception as e:
#         return dash.no_update, html.Div(f"Error deleting users: {str(e)}", style={"color": "red"})


@callback(
    [Output("users-grid", "rowData"),
     Output("user-update-status", "children")],
    [Input("delete-selected-btn", "n_clicks"),
     Input("add-user-btn", "n_clicks"),
     Input("users-grid", "cellValueChanged")],
    [State("users-grid", "selectedRows"),
     State("users-grid", "rowData")]
)
def manage_users(delete_clicks, n_clicks, cell_changed, selected_rows, current_rows):
    print(selected_rows)
    trigger = dash.callback_context.triggered_id
    if not trigger:
        return dash.no_update, dash.no_update
    
    # Handle delete
    if trigger == "delete-selected-btn" and selected_rows:
        try:
            with current_app.app_context():
                for row in selected_rows:
                    user = User.query.filter_by(username=row['username']).first()
                    if user:
                        db.session.delete(user)
                db.session.commit()
                users = User.query.all()
                users_list = [{"username": user.username, "role": user.role} for user in users]
                return users_list, "Users deleted successfully"
        except Exception as e:
            return dash.no_update, f"Error: {str(e)}"
        
    print(trigger,cell_changed)
    if trigger == "add-user-btn" and n_clicks:
        current_rows.append({"username": "", "role": "user", "password": ""})
        return current_rows, ""
        
    if trigger == "users-grid" and cell_changed:
        try:
            with current_app.app_context():
                username = cell_changed[0]['data']['username']
                role = cell_changed[0]['data']['role']
                try:
                    password = cell_changed[0]['data']['password']
                except KeyError:
                    password = None
                # Change role
                if cell_changed[0]['colId'] == "role":
                    user = User.query.filter_by(username=username).first()
                    if user:
                        user.role = role
                        db.session.commit()
                        return dash.no_update, f"Updated role for {username} to {role}"
                    print("role")
                
                # User creation
                if not username or not password:
                    return dash.no_update, "Username and password required"
                
                user = User(username=username, role=role)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                
                return dash.no_update, f"User {username} created successfully"
            
        except Exception as e:
            return dash.no_update, f"Error: {str(e)}"
    
    return dash.no_update, dash.no_update

@callback(
    Output("admin-content", "children"),
    Input("url", "search")
)
def update_admin_content(search):
    if (search == "?section=users"):
        return user_management_content()
    elif (search == "?section=models"):
        return model_management_content()
    elif (search == "?section=sensors"):
        return sensor_management_content()
    return html.P("Please select a section from the menu.")

layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col([
            dbc.Nav([
                    dbc.NavLink(
                        "User Management",
                        href="/admin?section=users",
                        active="exact",
                        style={
                            "width": "100%",
                            "textAlign": "left",
                            "padding": "10px 15px",
                            "marginBottom": "2px"
                        },
                        className="text-dark bg-light"
                    ),
                    dbc.NavLink(
                        "Sensor Management",
                        href="/admin?section=sensors",
                        active="exact",
                        style={
                            "width": "100%",
                            "textAlign": "left",
                            "padding": "10px 15px",
                            "marginBottom": "2px"
                        },
                        className="text-dark bg-light"
                    ),
                    dbc.NavLink(
                        "Model Management",
                        href="/admin?section=models",
                        active="exact",
                        style={
                            "width": "100%",
                            "textAlign": "left",
                            "padding": "10px 15px",
                            "marginBottom": "2px"
                        },
                        className="text-dark bg-light"
                    ),
                ],
                vertical=True,
                pills=True,
                style={
                    "backgroundColor": "#f8f9fa",
                    "padding": "10px",
                    "borderRadius": "5px",
                    "width": "100%"
                },
                className="nav-pills-custom"
            ),
        ], width=3),
        dbc.Col([
            html.Div(id="admin-content")
        ], width=9),
    ]),
])