import time

from dash import Dash, Input, Output, State, ctx, no_update, html
import dash_bootstrap_components as dbc
from flask import session
from settings import settings


def mark_a_status(msg: str, success: bool) -> dbc.Container:
    if success:
        icon_class = "fa fa-check-circle me-2 text-success"
    else:
        icon_class = "fa fa-times-circle me-2 text-danger"

    return dbc.Container([html.I(className=icon_class), html.Span(msg)])


def register_auth_callbacks(app: Dash):
    @app.callback(
        Output("sign-in-container", "className"),
        inputs=dict(
            url_pathname=Input("url", "pathname"),
            refresh=Input("url", "refresh"),
        ),
    )
    def show_hide_page(url_pathname, refresh):
        if session.get("authenticated") == True:
            return "main-page-hidden"
        return "main-page-visible"

    @app.callback(
        Output("learn-more-modal", "is_open"),
        Input("learn-more-link", "n_clicks"),
        Input("learn-more-close-btn", "n_clicks"),
    )
    def open_learn_more_modal(link, close):
        if ctx.triggered_id == "learn-more-link":
            return True
        return False

    @app.callback(
        Output("auth-modal", "is_open"),
        Output("auth-modal-body", "children"),
        Input("auth-btn", "n_clicks"),
    )
    def open_auth_modal(btn):
        return True, "Verifying authorization key..."

    @app.callback(
        output=dict(
            modal_openned=Output("auth-modal", "is_open", allow_duplicate=True),
            auth_info=Output("auth-modal-body", "children", allow_duplicate=True),
            url_refresh=Output("url", "refresh", allow_duplicate=True),
        ),
        inputs=dict(
            close_auth_modal=Input("auth-modal-close-btn", "n_clicks"),
            opened_modal=Input("auth-modal", "is_open"),
            auth_key=State("auth-key", "value"),
        ),
        running=[(Output("auth-loading-icon", "display"), "show", "hide")],
        cancel=[Input("auth-modal-close-btn", "n_clicks")],
    )
    def manage_auth__modal(close_auth_modal, opened_modal, auth_key):
        closing = ctx.triggered_id == "auth-modal-close-btn"

        if not closing:
            if auth_key == settings.ADMIN_KEY:
                session["authenticated"] = True
                session["user"] = {
                    "username": "vadmin",
                    "fullname": "Aaron Ontoyin Yin",
                }
                auth_info = mark_a_status("Authorised successfully!", True)
            else:
                time.sleep(1)
                auth_info = mark_a_status("Invalid Auth key!", False)
        else:
            auth_info = no_update

        return {
            "modal_openned": not closing,
            "url_refresh": closing,
            "auth_info": auth_info,
        }

    @app.callback(
        Output("url", "refresh"),
        Output("auth-key", "value"),
        Input("logout-btn", "n_clicks"),
    )
    def logout_user(n_clicks):
        session["authenticated"] = False
        session["user"] = None
        return True, ""
