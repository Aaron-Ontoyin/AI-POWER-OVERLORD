from typing import Callable, List

from flask import session
from dash import Dash, Output, Input, State, ctx, no_update, html, ALL
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from .waiter import (
    get_coverage_areas,
    get_dashboard_data,
    get_signal_streams,
    get_chat_messages,
)
from .schemas import CoverageArea, Plots, ChatMessage
from .plots import get_plots, text_plot


def register_dashboard_callbacks(
    app: Dash,
    store_data: Callable,
    retrieve_data: Callable,
):
    @app.callback(
        Output("dashboard-container", "className"),
        Input("url", "pathname"),
    )
    def show_hide_page(url_pathname):
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
                            id={
                                "type": "coverage-area-check",
                                "area_id": coverage_area.id,
                                "area_name": coverage_area.name,
                            },
                            value=coverage_area.checked,
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

    def recursive_check_uncheck_area(area: CoverageArea, checked_ids: List[str]):
        area.checked = area.id in checked_ids
        for sub_area in area.sub_areas:
            recursive_check_uncheck_area(sub_area, checked_ids)

    @app.callback(
        Output("coverage-areas-modal-body", "children"),
        inputs=dict(
            auth_modal_close=Input("auth-modal-close-btn", "n_clicks"),
            url_pathname=Input("url", "pathname"),
            local_store=State("local-store", "data"),
        ),
    )
    def update_coverage_area_modal_body(auth_modal_close, url_pathname, local_store):
        if not session.get("authenticated") == True:
            raise PreventUpdate

        coverage_areas = get_coverage_areas()
        checked_ids = [ca[0] for ca in local_store.get("checked_ca_ids", [])]
        for area in coverage_areas:
            recursive_check_uncheck_area(area, checked_ids)

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

    @app.callback(
        output=dict(
            alert_value=Output("general-alert", "children"),
            alert_is_open=Output("general-alert", "is_open"),
            areas_covered=Output("areas-covered", "children"),
            local_store=Output("local-store", "data"),
        ),
        inputs=dict(
            datetime_start=Input("datetime-picker-start", "value"),
            datetime_end=Input("datetime-picker-end", "value"),
            ca_selection=Input("coverage-areas-modal-close-btn", "n_clicks"),
            url_pathname=Input("url", "pathname"),
            ca_ids=State(
                {"type": "coverage-area-check", "area_id": ALL, "area_name": ALL},
                "id",
            ),
            ca_values=State(
                {"type": "coverage-area-check", "area_id": ALL, "area_name": ALL},
                "value",
            ),
            local_store=State("local-store", "data"),
        ),
    )
    def update_metrics_card(
        datetime_start,
        datetime_end,
        ca_selection,
        url_pathname,
        ca_ids,
        ca_values,
        local_store,
    ):
        if datetime_end <= datetime_start:
            return {
                "alert_value": "Please select an end date and time after the start.",
                "alert_is_open": True,
                "areas_covered": no_update,
                "local_store": no_update,
            }

        if ctx.triggered_id == "url":
            checked_cas = local_store.get("checked_ca_ids", [])
        else:
            checked_cas = [
                (ca_id["area_id"], ca_id["area_name"])
                for ca_id, ca_value in zip(ca_ids, ca_values)
                if ca_value
            ]

        if not checked_cas:
            local_store["checked_ca_ids"] = []
            return {
                "alert_value": no_update,
                "alert_is_open": no_update,
                "areas_covered": html.Span(
                    "Please select some areas to view data.",
                    className="text-muted",
                ),
                "local_store": local_store,
            }

        local_store["checked_ca_ids"] = checked_cas

        areas_covered = [
            html.Span(
                area_name, className="area-covered", id=f"area-covered--{area_id}"
            )
            for area_id, area_name in checked_cas
        ]
        return {
            "alert_value": no_update,
            "alert_is_open": no_update,
            "areas_covered": areas_covered,
            "local_store": local_store,
        }

    @app.callback(
        output=dict(
            total_transformers=Output("total-transformers", "children"),
            total_meters=Output("total-meters", "children"),
            consumption_patterns_fig=Output("consumption-patterns-chart", "figure"),
            trend_analysis_fig=Output("trend-analysis-chart", "figure"),
            freq_analysis_fig=Output("freq-analysis-chart", "figure"),
            anomaly_fig=Output("anomaly-chart", "figure"),
            local_store=Output("local-store", "data", allow_duplicate=True),
        ),
        inputs=dict(
            areas_covered=Input("areas-covered", "children"),
            datetime_start=State("datetime-picker-start", "value"),
            datetime_end=State("datetime-picker-end", "value"),
            local_store=State("local-store", "data"),
        ),
    )
    def update_total_values_and_graphs(
        datetime_start,
        datetime_end,
        areas_covered,
        local_store,
    ):
        ca_ids = [ca_id for ca_id, _ in local_store["checked_ca_ids"]]
        if not ca_ids:
            text_fig = text_plot("No areas selected")
            return {
                "total_transformers": "--",
                "total_meters": "--",
                "consumption_patterns_fig": text_fig,
                "trend_analysis_fig": text_fig,
                "freq_analysis_fig": text_fig,
                "anomaly_fig": text_fig,
                "local_store": no_update,
            }

        plots_key = f"dashboard-plots-{datetime_start}-{datetime_end}-{ca_ids}"

        if plots_dict := local_store.get(plots_key):
            plots = Plots(**plots_dict)
        else:
            data = get_dashboard_data(
                datetime_start=datetime_start,
                datetime_end=datetime_end,
                coverage_areas_ids=ca_ids,
            )
            plots = get_plots(data)

            keys_to_delete = [
                k for k in local_store.keys() if k.startswith("dashboard-plots-")
            ]
            for k in keys_to_delete:
                del local_store[k]

            local_store[plots_key] = plots.model_dump()

        return {
            "total_transformers": plots.num_transformers,
            "total_meters": plots.num_meters,
            "consumption_patterns_fig": plots.consump_ptrns_fig,
            "trend_analysis_fig": plots.trend_analysis_fig,
            "freq_analysis_fig": plots.freq_analysis_fig,
            "anomaly_fig": plots.anomaly_fig,
            "local_store": local_store,
        }

    @app.callback(
        output=dict(
            graph_fullscreen_modal_is_open=Output("graph-fullscreen-modal", "is_open"),
            fullscreen_graph_figure=Output("fullscreen-graph", "figure"),
        ),
        inputs=dict(
            n_clicks=Input({"id": "graph-fullscreen-btn", "graph_id": ALL}, "n_clicks"),
            figures={
                "consumption-patterns-chart": State(
                    "consumption-patterns-chart", "figure"
                ),
                "trend-analysis-chart": State("trend-analysis-chart", "figure"),
                "freq-analysis-chart": State("freq-analysis-chart", "figure"),
                "anomaly-chart": State("anomaly-chart", "figure"),
            },
        ),
    )
    def open_graph_fullscreen_modal(n_clicks, figures):
        return {
            "graph_fullscreen_modal_is_open": True,
            "fullscreen_graph_figure": figures[ctx.triggered_id["graph_id"]],
        }

    @app.callback(
        Output("signal-stream-canvas", "children"),
        Input("signal-stream-interval", "n_intervals"),
        prevent_initial_call=True,
    )
    def update_signal_stream(interval):
        signal_streams = get_signal_streams()
        if not signal_streams:
            return "No signal streams."

        return [
            dmc.Card(
                [
                    dmc.CardSection(
                        [
                            stream.title,
                            html.I(
                                className=f"fa fa-circle fa-tiny me-3 text-{stream.status}",
                            ),
                        ],
                        className="text-muted fs-5 d-flex justify-content-between align-items-center",
                    ),
                    dmc.CardSection(
                        stream.message,
                        className="text-muted fs-6",
                    ),
                    dmc.CardSection(
                        stream.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        className="text-muted signal-stream-timestamp",
                    ),
                ],
                className="bg-light p-4 text-dark mb-3",
            )
            for stream in signal_streams
        ]

    def create_chat_message(message: ChatMessage):
        align = "start" if message.sender == "user" else "end"
        card_color = "primary" if message.sender == "user" else "light"
        text_color = "white" if message.sender == "user" else "dark"
        return dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.Div(
                                    message.message,
                                    className=f"mb-2 text-{text_color} p-0 m-0",
                                    style={
                                        "whiteSpace": "pre-line",
                                        "fontSize": "0.9rem",
                                        "textAlign": "justify",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Small(
                                            message.timestamp.strftime(
                                                "%B %d, %I:%M %p"
                                            ),
                                            className="text-muted m-0 p-0",
                                            style={"fontSize": "0.8rem"},
                                        ),
                                    ],
                                    className="d-flex align-items-end justify-content-end p-0 m-0",
                                ),
                            ],
                            className="p-0 m-0",
                        )
                    ],
                    color=card_color,
                    className="mb-2 p-2 m-0",
                    style={
                        "maxWidth": "90%",
                        "marginLeft": "auto" if align == "end" else 0,
                        "marginRight": "auto" if align == "start" else 0,
                        "borderRadius": "8px",
                    },
                ),
                width={"size": 11, "offset": 1} if align == "end" else 11,
                className=f"d-flex justify-content-{align}",
            )
        )

    @app.callback(
        Output("chat-content", "children"),
        Input("chat-send-btn", "n_clicks"),
        State("chat-input", "value"),
    )
    def send_message(n_clicks, message):
        messages = get_chat_messages(thread_id="1")
        if not messages:
            return dbc.Container(
                "Want to explore the data? Just ask Lyti!",
                id="lyti-greeting",
                className="m-0 p-0",
            )
        return [create_chat_message(message) for message in messages]
