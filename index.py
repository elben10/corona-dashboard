from urllib.parse import urlparse

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from apps import country, error, home

from base import base_layout

TITLE = "Corona"
ICON = "fas fa-biohazard"
SIDEBAR = [
    {"title": "Dashboard", "icon": "fas fa-fw fa-tachometer-alt", "href": "/"},
    {"title": "Countries", "icon": "fas fa-flag", "href": "/countries"},
]


app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), base_layout(TITLE, ICON, SIDEBAR),]
)


@app.callback(Output("content", "children"), [Input("url", "href")])
def display_page(href):
    parsed_url = urlparse(href)
    if parsed_url.path == "/":
        return home.layout()
    elif parsed_url.path == "/countries":
        return country.layout()
    else:
        return error.layout()


if __name__ == "__main__":
    app.run_server(debug=True)
