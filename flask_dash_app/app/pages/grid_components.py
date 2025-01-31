import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash import dcc
import plotly.express as px
import plotly.graph_objects as go
import geoip2.database
import pandas as pd

# World Map
def create_world_map(df):
    """
    Creates a geographical scatter plot of IP addresses on a world map.
    
    Args:
        df (pd.DataFrame): DataFrame containing IP addresses and prediction data
    
    Returns:
        dash.dcc.Graph: A Dash graph component containing the world map
    """
    # Get Map
    reader = geoip2.database.Reader('flask_dash_app/app/GeoLite2-City.mmdb')


    def ip_to_lat_lon(ip):
        try:
            response = reader.city(ip)
            return response.location.latitude, response.location.longitude
        except:
            return None, None
    
    df['source_lat'], df['source_lon'] = zip(*df['partner_ip'].apply(ip_to_lat_lon))
    
    fig = px.scatter_geo(
        df,
        lat='source_lat',
        lon='source_lon',
        hover_name='partner_ip',
        color='prediction',
        scope='world'
    )
    return dcc.Graph(figure=fig, style={'width': '100%', 'height': '600px'})

def make_pie_chart(fig_id, selected_rows):
    """
    Creates a pie chart showing classification probabilities for selected rows.
    
    Args:
        fig_id (str): ID for the graph component
        selected_rows (list): List of dictionaries containing selected row data
    
    Returns:
        dash.dcc.Graph: A Dash graph component containing the pie chart
    """
    detail_df = pd.DataFrame(selected_rows)
    return dcc.Graph(
        id=fig_id,
        figure=px.pie(
                detail_df,
                values=detail_df.probabilities.values[0].values(),
                names=detail_df.probabilities.values[0].keys(),
                title="Classification Probabilities"
            ).update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5
                )
            )
    )

def make_prediction_pie_chart(fig_id, selected_rows, metric):
    """
    Creates a pie chart showing classification probabilities for selected rows.
    
    Args:
        fig_id (str): ID for the graph component
        selected_rows (list): List of dictionaries containing selected row data
        metric (str): The metric to display
    
    Returns:
        dash.dcc.Graph: A Dash graph component containing the pie chart
    """
    detail_df = pd.DataFrame(selected_rows)
    prediction_counts = detail_df[metric].value_counts()
    title = metric.capitalize() + " Probabilities"
    return dcc.Graph(
        id=fig_id,
        figure=px.pie(
                detail_df,
                values=prediction_counts.values,
                names=prediction_counts.index,
                title=title
            ).update_layout(
                title=dict(
                    text=title,
                    x=0.5,
                    xanchor='center',
                    yanchor='top'
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5
                )
            )
    )

def make_detailed_grid(grid_id, selected_rows):
    """
    Creates a detailed grid view for selected rows.
    
    Args:
        grid_id (str): ID for the grid component
        selected_rows (list): List of dictionaries containing selected row data
    
    Returns:
        dash_ag_grid.AgGrid: An AG Grid component showing detailed data
    """
    detail_df = pd.DataFrame(selected_rows)
    detail_grid = dag.AgGrid(
                    id=grid_id,
                    rowData= detail_df.to_dict("records"),  
                    columnDefs=[{"field": col} for col in detail_df.columns if (col != "flow_data" and col!= "probabilities")],
                    style={"height": 200}
                    )
    return detail_grid

def make_grid(df, seen=False, grid_id="grid", columns=[]):
    """
    Creates a main grid view for flow data.
    
    Args:
        df (pd.DataFrame): DataFrame containing flow data
        seen (bool): Filter for seen/unseen flows
        grid_id (str): ID for the grid component
        columns (list): List of column definitions
    
    Returns:
        dash_ag_grid.AgGrid: An AG Grid component showing flow data
    """
    return dag.AgGrid(
        id=grid_id,
        rowData=df[df["has_been_seen"] == seen].to_dict("records"),
        columnDefs=columns,
        defaultColDef={"filter": True, "floatingFilter": True, "wrapHeaderText": True, "autoHeaderHeight": True, "resizable": True, "flex": 1},
        dashGridOptions={"pagination": True, "paginationPageSize": 10, "rowSelection": "single", "suppressRowClickfilter": False, "animateRows": False},
        rowClassRules={"bg-secondary text-dark bg-opacity-25": "params.node.rowPinned === 'top' | params.node.rowPinned === 'bottom'"},
        style={"height": 600, "width": "100%"},
    )

def display_line(fig_id, df, cluster_time):
    """
    Creates a scatter plot showing flow activity over time.
    
    Args:
        fig_id (str): ID for the graph component
        df (pd.DataFrame): DataFrame containing flow data
        cluster_time (str): Time interval for binning data
    
    Returns:
        dash.dcc.Graph: A Dash graph component containing the scatter plot
    """
    df["time_bin"] = df["timestamp"].dt.floor(cluster_time)
    grouped_df = df.groupby(['time_bin', 'prediction']).size().reset_index(name='count')
    
    fig = px.scatter(
        grouped_df,
        x="time_bin",
        y="count",
        color="prediction",
        title="Flow Activity Over Time",
        labels={
            'time_bin': 'Time',
            'count': 'Number of Flows',
            'prediction': 'Prediction Type'
        },
        size_max=15,
    )

    # Add vertical lines
    for idx, row in grouped_df.iterrows():
        fig.add_shape(
            type='line',
            x0=row['time_bin'],
            y0=0,
            x1=row['time_bin'],
            y1=row['count'],
            line=dict(
                color='rgba(128, 128, 128, 0.5)',
                width=1,
                dash='dash'
            )
        )

    fig.update_traces(marker=dict(size=10), marker_symbol="square")

    fig.update_layout(
        xaxis_rangeslider_visible=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.3,
            xanchor="center",
            x=0.5
        )
    )
    
    return dcc.Graph(id=fig_id, figure=fig)

def create_boxplot(detail_flow_df):
    """
    Creates a boxplot showing the distribution of flow features.
    
    Args:
        detail_flow_df (pd.DataFrame): DataFrame containing flow feature data
    
    Returns:
        dash.dcc.Graph: A Dash graph component containing the boxplot
    """
    fig = go.Figure()
    
    for idx, col in enumerate(detail_flow_df.columns):
        fig.add_trace(go.Box(
            x=detail_flow_df[col],
            name=col,
            orientation='h',
            boxpoints='all',
            jitter=0,
            pointpos=0,
            marker_color='blue',
            showlegend=False,
            showwhiskers=False,
        ))

    fig.update_layout(
        title="Flow Features Distribution",
        xaxis_title="Value",
        yaxis_title="Features",
        showlegend=True,
        height=len(detail_flow_df.columns) * 40,
        margin=dict(l=300),
    )
    
    return dcc.Graph(figure=fig)