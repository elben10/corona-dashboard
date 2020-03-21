import dash
from flask_caching import Cache

EXTERNAL_SCRIPTS = [
    "https://code.jquery.com/jquery-3.4.1.slim.min.js",
    "https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js",
    "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js",
]
EXTERNAL_STYLESHEETS = [
    "https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i",
    "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.12.1/css/all.min.css",
]

app = dash.Dash(
    __name__,
    external_scripts=EXTERNAL_SCRIPTS,
    external_stylesheets=EXTERNAL_STYLESHEETS,
)
server = app.server
app.config.suppress_callback_exceptions = True

cache = Cache(server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

TIMEOUT = 60 * 60 * 6

