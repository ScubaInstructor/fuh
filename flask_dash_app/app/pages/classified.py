import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/classified/')

layout = html.Div([
    dbc.Accordion(
        [
            dbc.AccordionItem(
                "This is the content of the first section", title="Item 1"
            ),
            dbc.AccordionItem(
                "This is the content of the second section", title="Item 2"
            ),
            dbc.AccordionItem(
                "This is the content of the third section", title="Item 3"
            ),
        ],
        start_collapsed=True,
    ),
])