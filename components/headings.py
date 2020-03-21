import dash_html_components as html

def header(title):
    return html.Div(
        html.H1(title, className="h3 mb-0 text-gray-800"),
        className="d-sm-flex align-items-center justify-content-between mb-4",
    )


def subheader(title):
    return html.Div(
        html.H1(title, className="h6 mb-0 text-gray-800"),
        className="d-sm-flex align-items-center justify-content-between mb-4",
    )