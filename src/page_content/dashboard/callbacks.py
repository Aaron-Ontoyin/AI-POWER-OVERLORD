from typing import Callable

from flask import session
from dash import Dash, Output, Input, State, ctx, html
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from .waiter import get_coverage_areas
from .schemas import CoverageArea


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
        Input("ask-lyti", "n_clicks"),
        State("chat-canvas", "is_open"),
    )
    def toggle_offcanvas_scrollable(n1, is_open):
        if n1:
            return not is_open
        return is_open

    @app.callback(
        Output("coverage-areas-modal", "is_open"),
        Input("select-coverage-areas-btn", "n_clicks"),
        Input("coverage-areas-modal-close-btn", "n_clicks"),
    )
    def toggle_coverage_area_modal(open_btn, close_btn):
        return True if ctx.triggered_id == "select-coverage-areas-btn" else False

    def create_coverage_area_accordion_item(coverage_area: CoverageArea, level=0):
        return dmc.AccordionItem(
            [
                dbc.Container(
                    [
                        dbc.Checkbox(
                            id=f"coverage-area-check--{coverage_area.id}",
                            value=False,
                            style={
                                "fontSize": "1.2rem",
                                "width": "fit-content",
                            },
                        ),
                        dmc.AccordionControl(
                            [
                                dbc.Container(
                                    [
                                        dmc.Text(coverage_area.name, className="me-2"),
                                        dmc.Badge(
                                            coverage_area.type,
                                            color=coverage_area.badge_color,
                                            size="xs",
                                        ),
                                    ],
                                    className="d-flex align-items-center",
                                ),
                            ],
                            className="ps-0",
                        ),
                    ],
                    className="d-flex align-items-center",
                ),
                dmc.AccordionPanel(
                    [
                        (
                            dmc.Accordion(
                                [
                                    create_coverage_area_accordion_item(
                                        sub_area, level + 1
                                    )
                                    for sub_area in coverage_area.sub_areas
                                ],
                                id=f"sub-accordion-{coverage_area.id}",
                                className=f"nested-accordion-level-{level + 1}",
                                multiple=True,
                            )
                            if coverage_area.sub_areas
                            else html.Div("No sub-areas")
                        )
                    ],
                ),
            ],
            value=coverage_area.id,
        )

    @app.callback(
        Output("coverage-areas-modal-body", "children"),
        Input("auth-modal-close-btn", "n_clicks"),
    )
    def update_coverage_area_modal_body(auth_modal_close_btn):
        coverage_areas = get_coverage_areas()
        return (
            dmc.Accordion(
                [
                    create_coverage_area_accordion_item(coverage_area)
                    for coverage_area in coverage_areas
                ],
                id="main-coverage-accordion",
                className="main-coverage-accordion",
                multiple=True,
            )
            if coverage_areas
            else "No coverage areas"
        )

    @app.callback(
        Output("signal-stream-canvas", "is_open"),
        Input("signal-stream-btn", "n_clicks"),
        State("signal-stream-canvas", "is_open"),
    )
    def toggle_signal_stream_canvas(n1, is_open):
        if n1:
            return not is_open
        return is_open
