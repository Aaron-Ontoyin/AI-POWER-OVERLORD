from dash import Dash, Output, Input
from flask import session


def register_nav_callbacks(app: Dash):
    @app.callback(
        output=dict(
            user_check=Output("user-name-check", "className"),
            username=Output("user-name-value", "children"),
        ),
        inputs=dict(
            url_pathname=Input("url", "pathname"),
            url_refresh=Input("url", "refresh"),
        ),
    )
    def update_username(url_pathname, url_refresh):
        user = {"username": "Unauthenticated"}
        if authenticated := session.get("authenticated") == True:
            user = session.get("user") or {}

        user_check = (
            "fa fa-check-circle me-2 text-success"
            if authenticated
            else "fa fa-lock me-2 text-warning"
        )
        return {"user_check": user_check, "username": user.get("username")}
