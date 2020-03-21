import dash_core_components as dcc
import dash_html_components as html


def card(title=None, element=None, element_id=None):
    header_ = html.Div(
        html.H6(title, className="m-0 font-weight-bold text-primary"),
        className="card-header py-3 d-flex flex-row align-items-center justify-content-between",
    )
    body_ = html.Div(element, className="card-body", id=element_id)

    return html.Div([header_, body_], className="card shadow mb-4")


def card_with_dropdown(
    title, element, element_id, dropdown_id, dropdown_value, dropdown_options
):
    header_ = html.Div(
        [
            html.H6(title, className="m-0 font-weight-bold text-primary"),
            dcc.Dropdown(
                id=dropdown_id,
                value=dropdown_value,
                options=dropdown_options,
                style={"width": "450px"},
                clearable=False,
            ),
        ],
        className="card-header py-3 d-flex flex-row align-items-center justify-content-between",
    )
    body_ = html.Div(element, className="card-body", id=element_id)

    return html.Div([header_, body_], className="card shadow mb-4")


def card_fact(title, fact, icon, color="text-primary"):
    return html.Div(
        html.Div(
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                title,
                                className="text-xs font-weight-bold {color} text-uppercase mb-1",
                            ),
                            html.Div(
                                fact, className="h5 mb-0 font-weight-bold text-gray-800"
                            ),
                        ],
                        className="col mr-2",
                    ),
                    html.Div(
                        html.I(className=f"{icon} fa-2x text-gray-300"),
                        className="col-auto",
                    ),
                ],
                className="row no-gutters align-items-center",
            ),
            className="card-body",
        ),
        className="card border-left-primary shadow h-100 py-2",
    )
