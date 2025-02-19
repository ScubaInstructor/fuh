import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash import dcc
import plotly.express as px
import plotly.graph_objects as go
import geoip2.database
import pandas as pd
from app.elastic_connector import CustomElasticsearchConnector
import asyncio

# World Map
def create_world_map(fig_id, df):
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
    
    df['source_lat'], df['source_lon'] = zip(*df['dst_ip'].apply(ip_to_lat_lon))
    
    fig = px.scatter_geo(
        df,
        lat='source_lat',
        lon='source_lon',
        hover_name='dst_ip',
        color='prediction',
        scope='world'
    )
    return dcc.Graph(id=fig_id, figure=fig, clickData=df.to_dict() ,style={'width': '100%', 'height': '600px'})

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

def make_prediction_pie_chart(fig_id, selected_rows, metric, title="Predictions"):
    """
    Creates a pie chart showing classification probabilities for selected rows.
    
    Args:
        fig_id (str): ID for the graph component
        selected_rows (list): List of dictionaries containing selected row data
        metric (str): The metric to display
        title (str): The title of the pie chart
    
    Returns:
        dash.dcc.Graph: A Dash graph component containing the pie chart
    """
    detail_df = pd.DataFrame(selected_rows)
    prediction_counts = detail_df[metric].value_counts()
    title = title
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

def create_boxplot(detail_flow_df, prediction):
    """
    Creates a boxplot showing the distribution of flow features.
    
    Args:
        detail_flow_df (pd.DataFrame): DataFrame containing flow feature data
        prediction (str): The prediction type
    
    Returns:
        dash.dcc.Graph: A Dash graph component containing the boxplot
    """
    PREDICTION_MAP = {
        'BENIGN': 1,
        'Bot': 2,
        'Brute Force': 3,
        'DOS': 4,
        'DDOS': 5,
        'Port Scan': 6,
        'Web Attack': 7
    }
    boxplot_index = PREDICTION_MAP.get(prediction, 0)

    fig = go.Figure()
    cec = CustomElasticsearchConnector()
    x = asyncio.run(cec.get_all_model_properties())

    model_df = pd.DataFrame(pd.DataFrame(x.iloc[0]["boxplotdata"][0]["metrics"])).drop(["metric_name"], axis=1)
    model_df = model_df.apply(lambda x: x.str[0])

    model_pred_df = pd.DataFrame(pd.DataFrame(x.iloc[0]["boxplotdata"][boxplot_index]["metrics"])).drop(["metric_name"], axis=1)
    model_pred_df = model_pred_df.apply(lambda x: x.str[0])

    norm_model_df = model_df.div(model_df.iloc[2], axis=1)
    norm_pred_df = model_pred_df.div(model_df.iloc[2], axis=1)
    norm_df = detail_flow_df.div(model_df.iloc[2], axis=1)

    traces = []
    
    for column in norm_model_df.columns:

        # Add scatter plot for individual data points
        scatter_trace = go.Scatter(
            x=norm_df[column],  # Data values on the x-axis
            y=[column] * len(norm_df[column]),  # Categories on the y-axis
            mode='markers',
            name=f'{column} Points',
            marker=dict(color='red', size=8, opacity=0.6, symbol="cross"),  # Customize scatter points
            showlegend=False,  # Hide scatter plot from legend
            hovertemplate="Flow Data: %{x:.3f}",
            offsetgroup=column  # Match offsetgroup
        )
        traces.append(scatter_trace)

        # Add scatter plot for individual data points
        mean_trace = go.Scatter(
            x=[norm_model_df[column].iloc[0]],  # Data values on the x-axis
            y=[column] * len(norm_df[column]),  # Categories on the y-axis
            mode='markers',
            name=f'{column} Points',
            marker=dict(
                symbol='line-ns-open',  # Vertical line marker; other option is "line-ns-open"
                color='black',
                size=20  # Adjust size as needed
            ),  # Customize scatter points
            showlegend=False,  # Hide scatter plot from legend
            hovertemplate="Global Mean Data: %{x:.3f}",
            offsetgroup=column  # Match offsetgroup
        )
        traces.append(mean_trace)

        max_trace = go.Scatter(
            x=[norm_model_df[column].iloc[2]],  # Data values on the x-axis
            y=[column] * len(norm_df[column]),  # Categories on the y-axis
            mode='markers',
            name=f'{column} Points',
            marker=dict(
                symbol='line-ns-open',  # Vertical line marker; other option is "line-ns-open"
                color='black',
                size=20  # Adjust size as needed
            ),  # Customize scatter points
            showlegend=False,  # Hide scatter plot from legend
            hovertemplate="Global Max Data: %{x:.3f}",
            offsetgroup=column  # Match offsetgroup
        )
        traces.append(max_trace)

        pred_trace = go.Scatter(
            x=[norm_pred_df[column].iloc[0]],  # Data values on the x-axis
            y=[column] * len(norm_df[column]),  # Categories on the y-axis
            mode='markers',
            name=f'{column} Points',
            marker=dict(
                symbol='line-ns-open',  # Vertical line marker; other option is "line-ns-open"
                color='blue',
                size=20  # Adjust size as needed
            ),  # Customize scatter points
            showlegend=False,  # Hide scatter plot from legend
            hovertemplate=f"{prediction} Mean Data: %{{x:.3f}}",
            offsetgroup=column  # Match offsetgroup
        )
        traces.append(pred_trace)
    
    # Create figure with custom layout
    fig = go.Figure(data=traces)
    
    fig.update_layout(
        title=dict(
            text=f'Flow Features Distribution - {prediction}',
            y=0.95,  # Reduce top space by moving title down
            x=0.5,
            xanchor='center',
            yanchor='top'
        ),
        xaxis=dict(
            title='Normalized Values',
            gridcolor='lightgray',
            showgrid=True
        ),
        yaxis=dict(
            title='Columns', 
            type='category',
            # Add these parameters to control spacing
            tickson="boundaries",
            ticklen=20,
            tickmode='linear',
            dtick=1,  # Controls spacing between ticks
        ),
        showlegend=False,
        boxmode='overlay',
        # Add height to give more vertical space
        height=len(norm_model_df.columns) * 40 + 200,  # Adjust this value to control overall height
        # Add margin to ensure labels aren't cut off
        margin=dict(l=200, r=50, t=50, b=10),
        bargap=1.0  # Controls space between bars (0-1)
    )

    # for idx, col in enumerate(detail_flow_df.columns):
    #     fig.add_trace(go.Box(
    #         x=detail_flow_df[col],
    #         name=col,
    #         orientation='h',
    #         boxpoints='all',
    #         jitter=0,
    #         pointpos=0,
    #         marker_color='blue',
    #         showlegend=False,
    #         showwhiskers=False,
    #     ))

    # fig.update_layout(
    #     title="Flow Features Distribution",
    #     xaxis_title="Value",
    #     yaxis_title="Features",
    #     showlegend=True,
    #     height=len(detail_flow_df.columns) * 40,
    #     margin=dict(l=300),
    # )
    
    return dcc.Graph(figure=fig)