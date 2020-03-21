import dash.dependencies as dep
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go

from app import app
from data_loader import (
   get_start_date,
   get_total_deaths,
   get_total_incidents,
   get_new_deaths,
   get_new_incidents,
   dataframe
)
from components.cards import card, card_fact, card_with_dropdown
from components.headings import header, subheader

from CONSTANTS import *

CORONA_MAP_VALUE = "incidentsPerMillion"
CORONA_MAP_OPTIONS = [
    {"value": "incidentsPerMillion", "label": "Corono incidents per million citizens"},
    {"value": "totalIncidents", "label": "Corona incidents"},
]


def layout():
    header_ = header("Dashboard")
    subheader_ = html.Div(
        [
            subheader(f"Data updated at: {get_start_date()}"),
            html.Div(
                [
                    html.A(
                        "Source",
                        href="https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide",
                    )
                ],
                className="d-sm-flex align-items-center justify-content-between mb-4",
            ),
        ],
        className="d-flex flex-row align-items-center justify-content-between",
    )
    fact_row = html.Div(
        [
            html.Div(
                card_fact(
                    "Number of deaths", f"{get_total_deaths():,.0f}", "fas fa-book-dead"
                ),
                className="col-xl-3 col-md-6 mb-4",
            ),
            html.Div(
                card_fact(
                    "Number of new deaths", f"{get_new_deaths():,.0f}", "fas fa-arrow-up"
                ),
                className="col-xl-3 col-md-6 mb-4",
            ),
            html.Div(
                card_fact(
                    "Number of cases",
                    f"{get_total_incidents():,.0f}",
                    "fas fa-hospital-alt",
                ),
                className="col-xl-3 col-md-6 mb-4",
            ),
            html.Div(
                card_fact(
                    "Number of new cases", f"{get_new_incidents():,.0f}", "fas fa-arrow-up"
                ),
                className="col-xl-3 col-md-6 mb-4",
            ),
        ],
        className="row",
    )
    first_row = html.Div(
        html.Div(
            dcc.Loading(
                card_with_dropdown(
                    "Map over corono incidents",
                    dcc.Loading(dcc.Graph(id="corona_map")),
                    None,
                    "corona_map_dropdown",
                    CORONA_MAP_VALUE,
                    CORONA_MAP_OPTIONS,
                )
            ),
            className="col-12",
        ),
        className="row",
    )
    return html.Div(
        [header_, subheader_, fact_row, first_row], className="container-fluid pt-5"
    )


@app.callback(
    dep.Output("corona_map", "figure"), [dep.Input("corona_map_dropdown", "value")]
)
def update_corona_map(value):
    _, df = dataframe()
    df_ = (
        df.groupby(["iso3", COUNTRY_TEXT])[[DEATHS, CASES]]
        .sum()
        .reset_index()
        .copy()
    )

    df_pop_ = (
        df.groupby(["iso3", COUNTRY_TEXT])[["population_2018"]]
        .first()
        .reset_index()
        .copy()
    )

    z = (
        df_[CASES] / df_pop_["population_2018"] * 1000000
        if value == "incidentsPerMillion"
        else df_[CASES]
    )

    fig = go.Figure(
        data=go.Choropleth(
            locations=df_["iso3"],
            z=z,
            zmin=z.quantile(0.01),
            zmax=z.quantile(0.99),
            # text = df['COUNTRY'],
            colorscale="blues",
            marker_line_color="black",
            marker_line_width=0.5,
            colorbar_title="Number of <br>corono incidents",
        )
    )

    fig.update_layout(
        geo=dict(
            landcolor="gray",
            showframe=False,
            showcoastlines=False,
            projection_type="equirectangular",
        ),
        margin=dict(t=0, b=0, l=0, r=0),
        height=600,
    )

    return fig

