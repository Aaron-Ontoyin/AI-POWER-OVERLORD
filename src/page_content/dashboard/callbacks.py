from typing import Callable

from flask import session
from dash import Dash, Output, Input, State


def register_dashboard_callbacks(app: Dash, store_data: Callable, retrieve_data):
    @app.callback(
        Output("dashboard-container", "className"),
        inputs=dict(
            url_pathname=Input("url", "pathname"),
            refresh=Input("url", "refresh"),
        ),
    )
    def show_hide_page(url_pathname, refresh):
        if session.get("authenticated") == True:
            return "main-page-visible"
        return "main-page-hidden"

    @app.callback(
        Output("chat-canvas", "is_open"),
        Input("lyti-container", "n_clicks"),
        State("chat-canvas", "is_open"),
    )
    def toggle_offcanvas_scrollable(n1, is_open):
        if n1:
            return not is_open
        return is_open
