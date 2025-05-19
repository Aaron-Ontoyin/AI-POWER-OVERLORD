import dash_bootstrap_components as dbc

from .dashboard import dashboard_ui
from .auth import auth_ui


page_content_ui = dbc.Container(
    [auth_ui, dashboard_ui],
    fluid=True,
    className="w-100 h-100 position-relative",
    style={"overflow": "hidden"},
)
