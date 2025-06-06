from typing import Callable, List

from flask import session
from dash import Dash, Output, Input, State, ctx, no_update, html, ALL, Patch
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from .waiter import (
    get_coverage_areas,
    get_dashboard_data,
    get_signal_streams,
    get_chat_thread,
    get_chat_threads,
)
from .schemas import CoverageArea, Plots, ChatMessage
from .plots import get_plots, text_plot
from .utils import readable_when


def register_dashboard_callbacks(app: Dash):
    @app.callback(
        Output("dashboard-container", "className"),
        Input("url", "pathname"),
    )
    def show_hide_page(url_pathname):
        if session.get("authenticated") == True:
            return "main-page-visible"
        return "main-page-hidden"

    @app.callback(
        output=dict(
            is_open=Output("chat-canvas", "is_open"),
            current_chat_title=Output(
                "current-chat-title", "children", allow_duplicate=True
            ),
            current_chat_id=Output("current-chat-id", "children", allow_duplicate=True),
        ),
        inputs=dict(
            ask_lyti_btn=Input("ask-lyti", "n_clicks"),
            local_store=State("local-store", "data"),
        ),
    )
    def open_chat_offcanvas(ask_lyti_btn, local_store):
        return {
            "is_open": True,
            "current_chat_title": local_store["current_chat_title"],
            "current_chat_id": local_store["current_chat_id"],
        }

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
        output=dict(
            signal_streams=Output("signal-stream-canvas", "children"),
            num_signal_streams=Output("signal-stream-badge", "children"),
        ),
        inputs=dict(
            signal_stream_interval=Input("signal-stream-interval", "n_intervals")
        ),
        prevent_initial_call=False,
    )
    def update_signal_stream(signal_stream_interval):
        signal_streams = get_signal_streams()
        num_signal_streams = len(signal_streams)
        if num_signal_streams == 0:
            return {
                "signal_streams": "No signal streams.",
                "num_signal_streams": 0,
            }

        if num_signal_streams > 99:
            num_signal_streams = "99+"

        cards = [
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
        return {
            "signal_streams": cards,
            "num_signal_streams": num_signal_streams,
        }

    def create_chat_message(message: ChatMessage):
        align = "end" if message.sender == "user" else "start"
        card_color = (
            {"background-color": "#adb8c66b"} if message.sender == "user" else {}
        )
        return dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                html.Div(
                                    message.message,
                                    className=f"mb-2 text-dark p-0 m-0",
                                    style={
                                        "whiteSpace": "pre-line",
                                        "fontSize": "0.9rem",
                                        "textAlign": "justify",
                                    },
                                )
                            ],
                            className="p-0 m-0",
                        )
                    ],
                    className="mb-2 p-2 m-0 border-0",
                    style={
                        "maxWidth": "90%",
                        "marginLeft": "auto" if align == "end" else 0,
                        "marginRight": "auto" if align == "start" else 0,
                        "borderRadius": "8px",
                        **card_color,
                    },
                ),
                width={"size": 11, "offset": 1} if align == "end" else 11,
                className=f"d-flex justify-content-{align}",
            ),
            class_name="mb-2",
        )

    @app.callback(
        output=dict(
            chat_content=Output("chat-content", "children"),
            local_store=Output("local-store", "data", allow_duplicate=True),
            current_chat_title=Output("current-chat-title", "children"),
            current_chat_id=Output("current-chat-id", "children"),
        ),
        inputs=dict(
            n_clicks=Input("chat-send-icon", "n_clicks"),
            new_message=State("chat-input", "value"),
            datetime_start=State("datetime-picker-start", "value"),
            datetime_end=State("datetime-picker-end", "value"),
            local_store=State("local-store", "data"),
            thread_id=State("current-chat-id", "children"),
        ),
        running=[
            (
                Output("chat-send-icon", "className"),
                "d-none",
                "fa fa-arrow-up text-muted",
            ),
            (
                Output("chat-cancel-icon", "className"),
                "fa fa-stop text-muted",
                "d-none",
            ),
        ],
        cancel=Input("chat-cancel-icon", "n_clicks"),
        background=True,
        prevent_initial_call=True,
    )
    def send_message(
        n_clicks,
        new_message,
        datetime_start,
        datetime_end,
        local_store,
        thread_id,
    ):
        ca_ids = [ca_id for ca_id, _ in local_store.get("checked_ca_ids", [])]
        thread = get_chat_thread(
            thread_id=thread_id,
            new_message=new_message,
            datetime_start=datetime_start,
            datetime_end=datetime_end,
            coverage_areas_ids=ca_ids,
        )
        local_store["current_chat_id"] = thread.id
        local_store["current_chat_title"] = thread.title

        return {
            "chat_content": [create_chat_message(msg) for msg in thread.messages],
            "local_store": local_store,
            "current_chat_title": thread.title,
            "current_chat_id": thread.id,
        }

    @app.callback(
        Output("chat-history-modal", "is_open"),
        Input("threads-btn", "n_clicks"),
    )
    def toggle_chat_history_modal(n_clicks):
        return True

    @app.callback(
        Output("chat-history-modal-body", "children"),
        Input("chat-history-modal", "is_open"),
    )
    def update_chat_history_modal_body(is_open):
        if not is_open:
            raise PreventUpdate

        modal_body_items = []
        chat_histories = get_chat_threads()
        for date_, threads in chat_histories.get_sorted_threads().items():
            modal_body_items.append(
                dbc.Container(
                    [
                        html.Div(readable_when(date_), className="fs-6 mb-2"),
                        dbc.Container(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            thread.title,
                                            id={
                                                "type": "chat-thread-item",
                                                "thread_id": thread.id,
                                                "thread_title": thread.title,
                                            },
                                            className="chat-thread-title text-muted fs-6",
                                        ),
                                    ]
                                )
                                for thread in threads
                            ],
                        ),
                    ],
                    className="mb-3 pb-2",
                    style={"borderBottom": "1px solid #e0e0e0"},
                )
            )

        return modal_body_items

    @app.callback(
        output=dict(
            current_chat_title=Output(
                "current-chat-title", "children", allow_duplicate=True
            ),
            current_chat_id=Output("current-chat-id", "children", allow_duplicate=True),
            chat_history_modal_is_open=Output(
                "chat-history-modal", "is_open", allow_duplicate=True
            ),
            local_store=Output("local-store", "data", allow_duplicate=True),
        ),
        inputs=dict(
            new_chat_btn=Input("new-chat-btn", "n_clicks"),
            thread_item_n_clicks=Input(
                {"type": "chat-thread-item", "thread_id": ALL, "thread_title": ALL},
                "n_clicks",
            ),
        ),
    )
    def update_current_chat(new_chat_btn, thread_item_n_clicks):
        if ctx.triggered_id == "new-chat-btn":
            return {
                "current_chat_title": "New Chat",
                "current_chat_id": "new-chat",
                "chat_history_modal_is_open": False,
                "local_store": no_update,
            }
        if ctx.triggered_id["type"] == "chat-thread-item":
            if not any(thread_item_n_clicks):
                raise PreventUpdate
            local_store = Patch()
            local_store["current_chat_id"] = ctx.triggered_id["thread_id"]
            local_store["current_chat_title"] = ctx.triggered_id["thread_title"]

            return {
                "current_chat_title": ctx.triggered_id["thread_title"],
                "current_chat_id": ctx.triggered_id["thread_id"],
                "chat_history_modal_is_open": False,
                "local_store": local_store,
            }
