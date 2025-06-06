from typing import Callable

from dash import Dash, Output, Input
from flask import session

from .dashboard import register_dashboard_callbacks
from .auth import register_auth_callbacks


def register_page_content_callbacks(app: Dash):
    pass
    # @app.callback(
    #     Output("page-content-sign-in", "class_name", allow_duplicate=True),
    #     Output("page-content-dashboard", "class_name", allow_duplicate=True),
    #     Output("data-name", "children"),
    #     Input("url", "pathname"),
    #     Input("url", "refresh"),
    # )
    # def on_app_reload(pathname, refresh):
    #     data_name = retrieve_data("data:name", False) or "No data name"

    #     if session.get("authenticated"):
    #         return (
    #             "page-content page-content-hidden",
    #             "page-content page-content-visible",
    #             data_name,
    #         )
    #     return (
    #         "page-content page-content-visible",
    #         "page-content page-content-hidden",
    #         data_name,
    #     )

    register_dashboard_callbacks(app)
    register_auth_callbacks(app)
