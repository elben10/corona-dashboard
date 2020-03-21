import dash_core_components as dcc
import dash_html_components as html


def base_layout(title, icon, sidebar_dict=None):
    return html.Div(
        html.Div(
            [
                sidebar(title, icon, sidebar_dict),
                html.Div(
                    html.Div(id="content"),
                    className="d-flex flex-column",
                    id="content-wrapper",
                ),
            ],
            id="wrapper",
        ),
        id="page-top",
    )


def sidebar(title, icon, sidebar_items):
    brand = dcc.Link(
        [
            html.Div(
                html.I(className=icon),
                className="sidebar-brand-icon",
            ),
            html.Div(title, className="sidebar-brand-text mx-3"),
        ],
        className="sidebar-brand d-flex align-items-center justify-content-center",
        href="/",
    )
    navbar_items = [
        create_navbar_item(
            sidebar_item["title"], sidebar_item["icon"], sidebar_item["href"]
        )
        for sidebar_item in sidebar_items
    ]
    return html.Ul(
        [brand, divider(), *navbar_items],
        className="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion",
        id="accordionSidebar",
    )


def create_navbar_item(title, icon, href):
    return html.Li(
        dcc.Link(
            [html.I(className=f"{icon}"), html.Span(title)],
            className="nav-link",
            href=href,
        ),
        className="nav-item",
    )


def divider():
    return html.Hr(className="sidebar-divider my-0")
