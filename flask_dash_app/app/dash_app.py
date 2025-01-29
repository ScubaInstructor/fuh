import dash
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


def init_dash_app(flask_app):
    # Initialize  Dash App
    dash_app = Dash(__package__, 
                    server=flask_app, 
                    #url_base_pathname='/dashboard/', 
                    external_stylesheets=[dbc.themes.BOOTSTRAP],
                    use_pages=True,)

    

    # # Navigation Bar
    # def make_navbar():
    #     return dbc.NavbarSimple(
    #         children=[
    #             dbc.NavItem(dbc.NavLink("Page 1", href="#")),
    #             dbc.DropdownMenu(
    #                 children=[
    #                     dbc.DropdownMenuItem("More pages", header=True),
    #                     dbc.DropdownMenuItem("Page 2", href="#"),
    #                     dbc.DropdownMenuItem("Page 3", href="#"),
    #                 ],
    #                 nav=True,
    #                 in_navbar=True,
    #                 label="More",
    #             ),
    #         ],
    #         brand="Network Anomaly Detection Demonstrator",
    #         brand_href="#",
    #         color="primary",
    #         dark=True,
    #     )
    
    # Get dash pages
    pages = dash.page_registry.values()
    # Layout Components
    dash_app.layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Inbox", href="/inbox/")),
                dbc.NavItem(dbc.NavLink("Classified", href="/classified/")),
                dbc.NavItem(dbc.NavLink("Training", href="/training/")),
                dbc.DropdownMenu(
                    children=[
                        #dbc.DropdownMenuItem("More pages", header=True),
                        dbc.DropdownMenuItem("Settings", href="#"),
                        dbc.DropdownMenuItem("Logout", href="/logout", external_link=True),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="My Account",
                ),
            ],
            brand="Network Anomaly Detection Demonstrator",
            brand_href="#",
            className="ms-0",
            color="primary",
            dark=True,
        ),
        dash.page_container
    ], style={'padding': '20px'})

    
    

    # TODO CHECK IF ANOTHER PATH COULD BE CRITICAL
    # Enforce authentication for the Dash app
    @flask_app.before_request
    def protect_dash_routes():
        if request.path.startswith('/inbox/'):  # Check if the request is for the Dash app
            if not current_user.is_authenticated:  # Check if the user is logged in
                return redirect(url_for('auth.login'))  # Redirect to the login page
            

    return dash_app

