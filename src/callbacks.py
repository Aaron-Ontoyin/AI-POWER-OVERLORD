from dash import Dash

from .page_content import register_page_content_callbacks
from .navbar import register_nav_callbacks


def register_callbacks(app: Dash):
    register_nav_callbacks(app)
    register_page_content_callbacks(app)
