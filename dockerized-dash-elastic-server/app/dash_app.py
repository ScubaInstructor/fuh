import dash
from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from flask_login import current_user
from flask import redirect, url_for, request, session, g
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import pandas as pd
import os
from dotenv import load_dotenv
import plotly.express as px
from .elastic_connector import CustomElasticsearchConnector
import asyncio
from functools import wraps


def init_dash_app(flask_app):
    # Initialize  Dash App
    dash_app = Dash(
        __package__,
        server=flask_app,
        # url_base_pathname='/dashboard/',
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        use_pages=True,
    )

    def is_admin():
        print(current_user)
        try:
            with flask_app.app_context():
                return current_user.is_authenticated and current_user.role == "admin"
        except:
            return False

    # Create base navigation items
    # nav_items = [
    #     dbc.NavItem(dbc.NavLink("Inbox", href="/inbox/")),
    #     dbc.NavItem(dbc.NavLink("Classified", href="/classified/")),
    #     dbc.NavItem(dbc.NavLink("Training", href="/training/"))
    # ]

    # Add admin check to layout
    @dash_app.callback(Output("navbar-items", "children"), Input("url", "pathname"))
    def update_nav(path):
        if is_admin():
            return dbc.NavItem(dbc.NavLink("Admin-Panel", href="/admin/"))
        return dash.no_update

    dash_app.layout = html.Div(
        [
            dcc.Location(id="url", refresh=False),
            dbc.NavbarSimple(
                children=[
                    dbc.NavItem(dbc.NavLink("Inbox", href="/inbox/")),
                    dbc.NavItem(dbc.NavLink("Classified", href="/classified/")),
                    html.Div([], id="navbar-items"),
                    dbc.NavItem(
                        dbc.NavLink("Logout", href="/logout", external_link=True)
                    ),
                    # dbc.DropdownMenu(
                    #     children=[
                    #         dbc.DropdownMenuItem("Settings", href="#"),
                    #         dbc.DropdownMenuItem("Logout", href="/logout", external_link=True),
                    #     ],
                    #     nav=True,
                    #     in_navbar=True,
                    #     label="My Account",
                    # ),
                ],
                brand="Network Anomaly Detection Demonstrator",
                brand_href="#",
                className="ms-0",
                color="primary",
                dark=True,
            ),
            dash.page_container,
        ],
        style={"padding": "20px"},
    )

    # TODO CHECK IF ANOTHER PATH COULD BE CRITICAL
    # Enforce authentication for the Dash app
    @flask_app.before_request
    def protect_dash_routes():
        if (
            request.path.startswith("/inbox/")
            or request.path.startswith("/classified/")
            or request.path.startswith("/training/")
        ):  # Check if the request is for the Dash app
            if not current_user.is_authenticated:  # Check if the user is logged in
                return redirect(url_for("auth.login"))  # Redirect to the login page
        if request.path.startswith(
            "/admin/"
        ):  # Check if the request is for the Dash app
            if current_user.role != "admin":  # Check if the user is logged in
                return redirect(url_for("/"))  # Redirect to the login page

    return dash_app
