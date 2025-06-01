from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from flask import Flask, session
from flask_session import Session
import dash_mantine_components as dmc

from src.callbacks import register_callbacks
from src.navbar import navbar_ui
from src.page_content import page_content_ui
from settings import settings


external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "assets/styles.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
]

server = Flask(__name__)
server.secret_key = settings.SECRET_KEY
server.config["SESSION_TYPE"] = settings.SESSION_TYPE
server.config["SESSION_PERMANENT"] = settings.SESSION_PERMANENT
Session(server)


app = Dash(
    __name__,
    title="AI Power Overloard",
    server=server,
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets,
    prevent_initial_callbacks=True,
)

layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="local-store", storage_type="session", data={}),
        html.Div(id="dummy-output", className="d-none"),
        dcc.Interval(id="signal-stream-interval", interval=60 * 1000, n_intervals=1),
        navbar_ui,
        page_content_ui,
    ],
    fluid=True,
    class_name="d-flex flex-column p-0 m-0",
    style={
        "height": "100vh",
        "width": "100vw",
        "overflow": "hidden",
    },
)
app.layout = dmc.MantineProvider(children=layout)

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
