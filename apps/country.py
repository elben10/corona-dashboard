import dash.dependencies as dep
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots


from app import app
from components.cards import card
from components.headings import header, subheader
from data_loader import get_country_options, dataframe

from CONSTANTS import *


def layout():
    header_ = header("Countries")
    dropdown_row = html.Div(
        html.Div(
            dcc.Dropdown(
                id="country_dropdown", value=None, options=get_country_options()
            ),
            className="col-lg-6",
        ),
        className="row",
    )
    graph_row = html.Div(
        [
            html.Div(
                card(
                    "Number of incidents",
                    dcc.Loading(dcc.Graph(id="country_incident_graph")),
                ),
                className="col-lg-6",
            ),
            html.Div(
                card(
                    "Number of deaths",
                    dcc.Loading(dcc.Graph(id="country_deaths_graph")),
                ),
                className="col-lg-6",
            ),
        ],
        className="row",
    )
    return html.Div(
        [header_, dropdown_row, html.Hr(), graph_row], className="container-fluid pt-5"
    )


@app.callback(
    [
        dep.Output("country_incident_graph", "figure"),
        dep.Output("country_deaths_graph", "figure"),
    ],
    [dep.Input("country_dropdown", "value")],
)
def update_country_graphs(iso3):
    _, df = dataframe()
    if iso3:
        df = df[df["iso3"] == iso3]
    else:
        df = df.groupby(DATE)[[CASES, DEATHS]].sum().reset_index()
    return generate_incidents_graph(df), generate_deaths_graph(df)


def generate_incidents_graph(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            name="New incidents",
            x=df[DATE],
            y=df[CASES],
            opacity=0.5,
            marker_color="#4e73df",
        ),
        secondary_y=True,
    )
    fig.add_trace(
        go.Scatter(name="Total number of incidents", x=df[DATE], y=df[CASES].cumsum())
    )

    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        height=600,
        plot_bgcolor="white",
        yaxis=dict(title="Total number of incidents"),
        yaxis2=dict(title="Number of new incidents"),
        legend=dict(x=-0.1, y=1.2),
    )
    return fig


def generate_deaths_graph(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            name="New deaths",
            x=df[DATE],
            y=df[DEATHS],
            opacity=0.5,
            marker_color="#4e73df",
        ),
        secondary_y=True,
    )
    fig.add_trace(
        go.Scatter(name="Total number of deaths", x=df[DATE], y=df[DEATHS].cumsum())
    )

    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        height=600,
        plot_bgcolor="white",
        yaxis=dict(title="Total number of deaths"),
        yaxis2=dict(title="Number of new deaths"),
        legend=dict(x=-0.1, y=1.2),
    )
    return fig
