from datetime import date, timedelta

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from ..footer_ui import get_footer


chat_history_modal = dbc.Modal(
    [
        dbc.ModalHeader(
            dbc.ModalTitle(
                [
                    "Chat History",
                    html.I(className="fa fa-history text-muted ms-2"),
                ],
                className="fs-6 d-flex align-items-center",
            ),
            close_button=False,
        ),
        dcc.Loading(
            dbc.ModalBody(
                id="chat-history-modal-body",
            ),
            type="dot",
        ),
    ],
    id="chat-history-modal",
)

chat_canvas = html.Div(
    [
        dbc.Offcanvas(
            [
                dbc.Container(
                    [
                        dbc.Container(
                            [
                                html.Span(
                                    "New Chat",
                                    id="current-chat-title",
                                    className="text-muted",
                                ),
                                html.Span(id="current-chat-id", className="d-none"),
                            ],
                            class_name="m-0",
                        ),
                        dbc.Container(
                            [],
                            class_name="flex-grow-1 m-0 p-0",
                            id="chat-content",
                            style={"maxHeight": "80vh", "overflow": "scroll"},
                        ),
                        dbc.Container(
                            [
                                dmc.Textarea(
                                    id="chat-input",
                                    autosize=True,
                                    minRows=1,
                                    maxRows=5,
                                    placeholder="Ask Lyti anything...",
                                    className="me-3 flex-grow-1",
                                ),
                                dbc.Button(
                                    [
                                        html.I(
                                            className="fa fa-stop text-muted d-none",
                                            **{"aria-hidden": "true"},
                                            title="Cancel",
                                            id="chat-cancel-icon",
                                        ),
                                        html.I(
                                            className="fa fa-arrow-up text-muted",
                                            **{"aria-hidden": "true"},
                                            title="Send",
                                            id="chat-send-icon",
                                        ),
                                    ],
                                    id="chat-send-btn",
                                ),
                            ],
                            class_name="m-0 p-0 mb-3 d-flex align-items-center",
                        ),
                    ],
                    class_name="d-flex flex-column h-100 m-0 p-0",
                    style={"height": "100vh"},
                )
            ],
            id="chat-canvas",
            placement="end",
            scrollable=True,
            title=html.Div(
                [
                    dbc.Container(
                        [
                            html.Img(
                                src="assets/lyti.png",
                                className="rounded-circle lyti-img",
                                style={"height": 40},
                            ),
                            html.Div(
                                [
                                    html.Span(
                                        "Lyti",
                                        className="glow-gradient mx-1",
                                    ),
                                    html.Div(className="pulse-circle"),
                                ],
                                className="d-flex justify-content-center align-items-center",
                            ),
                        ]
                    ),
                    html.I(
                        className="fa fa-history text-muted ms-4 align-self-end fs-6",
                        title="Chat history",
                        id="threads-btn",
                    ),
                    html.I(
                        className="fa fa-plus text-muted ms-4 align-self-end fs-6",
                        title="New chat",
                        id="new-chat-btn",
                    ),
                    chat_history_modal,
                ],
                className="d-flex justify-content-between align-items-center w-100 mb-0",
            ),
        ),
    ]
)

coverage_area_modal = dbc.Modal(
    [
        dbc.ModalHeader(
            [
                dbc.ModalTitle("Select Coverage Areas", className="fs-6"),
                html.I(
                    className="fa fa-street-view text-muted", **{"aria-hidden": "true"}
                ),
            ],
            class_name="d-flex justify-content-between pe-4",
            close_button=False,
        ),
        dcc.Loading(dbc.ModalBody(id="coverage-areas-modal-body"), type="dot"),
        dbc.ModalFooter(
            dbc.Button(
                "Done",
                id="coverage-areas-modal-close-btn",
                class_name="btn btn-info me-2",
                style={"width": "100px"},
            )
        ),
    ],
    id="coverage-areas-modal",
    keyboard=False,
    backdrop="static",
    centered=True,
    size="lg",
)

signal_stream_canvas = html.Div(
    [
        dbc.Offcanvas(
            id="signal-stream-canvas",
            scrollable=True,
            title=html.Div(
                [
                    html.I(
                        className="fa fa-bell text-muted me-3",
                        **{"aria-hidden": "true"},
                    ),
                    html.Div("Alerts!", className="text-muted fs-5"),
                ],
                className="d-flex justify-content-center align-items-center",
            ),
            is_open=False,
        )
    ]
)

fullscreen_graph_modal = dbc.Modal(
    [dbc.ModalHeader(), dbc.ModalBody(dcc.Graph(id="fullscreen-graph"))],
    id="graph-fullscreen-modal",
    fullscreen=True,
)

dashboard_ui = dbc.Container(
    [
        dbc.Container(
            [
                dbc.Alert(
                    duration=5000,
                    dismissable=True,
                    fade=True,
                    is_open=False,
                    color="warning",
                    id="general-alert",
                    class_name="mt-3",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    html.Div(
                                                        "Date Range",
                                                        className="card-label mb-2",
                                                    ),
                                                    dbc.Row(
                                                        [
                                                            dbc.Col(
                                                                dmc.DateTimePicker(
                                                                    id="datetime-picker-start",
                                                                    valueFormat="MMM D, YYYY HH:mm",
                                                                    value=date.today()
                                                                    - timedelta(days=7),
                                                                    clearable=False,
                                                                    className="setting-dtp",
                                                                ),
                                                                width=6,
                                                            ),
                                                            dbc.Col(
                                                                dmc.DateTimePicker(
                                                                    id="datetime-picker-end",
                                                                    valueFormat="MMM D, YYYY HH:mm",
                                                                    value=date.today(),
                                                                    clearable=False,
                                                                    className="setting-dtp",
                                                                ),
                                                                width=6,
                                                            ),
                                                        ],
                                                        class_name="gx-2 mb-3",
                                                    ),
                                                    dbc.Button(
                                                        "Select Coverage Area",
                                                        id="select-coverage-areas-btn",
                                                        color="light",
                                                    ),
                                                ],
                                                className="d-flex flex-column justify-content-center align-items-center",
                                            ),
                                        ],
                                        className="p-0",
                                    ),
                                    coverage_area_modal,
                                ],
                                class_name="shadow-sm border-0 h-100",
                            ),
                            class_name="col-12 col-md-6 col-lg-4 mt-1",
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.Span(
                                                                    "Transformers",
                                                                    className="card-label",
                                                                ),
                                                                dcc.Loading(
                                                                    html.Span(
                                                                        "40",
                                                                        id="total-transformers",
                                                                        className="metric-value",
                                                                    ),
                                                                    type="dot",
                                                                    className="ms-4 metrics-spinner",
                                                                ),
                                                            ],
                                                            className="metric-item",
                                                        ),
                                                        html.Div(
                                                            [
                                                                html.Span(
                                                                    "Meters",
                                                                    className="card-label",
                                                                ),
                                                                dcc.Loading(
                                                                    html.Span(
                                                                        "300",
                                                                        id="total-meters",
                                                                        className="metric-value",
                                                                    ),
                                                                    type="dot",
                                                                    className="ms-4 metrics-spinner",
                                                                ),
                                                            ],
                                                            className="metric-item",
                                                        ),
                                                    ],
                                                    class_name="col-12 col-md-4 d-flex d-md-block justify-content-between align-items-center px-3",
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Div(
                                                            [
                                                                html.Span(
                                                                    "Areas Covered",
                                                                    className="card-label",
                                                                ),
                                                                html.Div(
                                                                    id="areas-covered",
                                                                    className="areas-covered-wrap mt-2",
                                                                ),
                                                            ],
                                                            className="metric-item",
                                                        ),
                                                    ],
                                                    class_name="col-12 col-md-8",
                                                ),
                                            ],
                                            className="d-flex flex-row justify-content-between align-items-center",
                                        ),
                                    ],
                                    className="p-0",
                                ),
                                class_name="shadow-sm border-0 h-100",
                            ),
                            class_name="col-12 col-md-6 col-lg-5 mt-1",
                        ),
                        dbc.Col(
                            dbc.Container(
                                [
                                    dbc.Button(
                                        [
                                            "Signal Stream",
                                            dbc.Badge(
                                                color="danger",
                                                pill=True,
                                                text_color="white",
                                                className="position-absolute top-0 start-100 translate-middle",
                                                id="signal-stream-badge",
                                            ),
                                        ],
                                        outline=True,
                                        className="position-relative",
                                        id="signal-stream-btn",
                                    ),
                                    signal_stream_canvas,
                                ],
                                class_name="d-flex flex-column justify-content-center align-items-center py-5 py-md-0",
                            ),
                            class_name="col-12 col-md-6 col-lg-2 mt-1 d-flex justify-content-center align-items-center",
                        ),
                        dbc.Col(
                            dbc.Container(
                                [
                                    html.Img(
                                        src="assets/lyti.png",
                                        className="rounded-circle lyti-img",
                                        style={"height": 60},
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                "Ask",
                                                style={"color": "#555"},
                                                className="text-muted",
                                            ),
                                            html.Span(
                                                "Lyti",
                                                className="glow-gradient mx-1",
                                            ),
                                            html.Div(className="pulse-circle"),
                                        ],
                                        n_clicks=0,
                                        id="ask-lyti",
                                        className="d-flex flex-row justify-content-center align-items-center px-1",
                                    ),
                                    chat_canvas,
                                ],
                                class_name="d-flex flex-column justify-content-center align-items-center",
                                style={"min-height": 140},
                            ),
                            class_name="col-12 col-md-6 col-lg-1 mt-1",
                        ),
                    ],
                    justify="between",
                    class_name="mt-4 pe-lg-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Container(
                                [
                                    dcc.Graph(
                                        id="consumption-patterns-chart", className="m-0"
                                    ),
                                    html.Button(
                                        "Fullscreen",
                                        id={
                                            "id": "graph-fullscreen-btn",
                                            "graph_id": "consumption-patterns-chart",
                                        },
                                        className="fullscreen-btn m-0",
                                    ),
                                ],
                                class_name="metric-container",
                            ),
                            class_name="col-12 col-md-6 mt-4",
                        ),
                        dbc.Col(
                            dbc.Container(
                                [
                                    dcc.Graph(id="trend-analysis-chart"),
                                    html.Button(
                                        "Fullscreen",
                                        id={
                                            "id": "graph-fullscreen-btn",
                                            "graph_id": "trend-analysis-chart",
                                        },
                                        className="fullscreen-btn m-0",
                                    ),
                                ],
                                class_name="metric-container",
                            ),
                            class_name="col-12 col-md-6 mt-4",
                        ),
                    ],
                    align="center",
                    justify="between",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Container(
                                [
                                    dcc.Graph(id="anomaly-chart"),
                                    html.Button(
                                        "Fullscreen",
                                        id={
                                            "id": "graph-fullscreen-btn",
                                            "graph_id": "anomaly-chart",
                                        },
                                        className="fullscreen-btn m-0",
                                    ),
                                ],
                                class_name="metric-container",
                            ),
                            class_name="col-12 col-md-6 mt-4",
                        ),
                        dbc.Col(
                            dbc.Container(
                                [
                                    dcc.Graph(id="freq-analysis-chart"),
                                    html.Button(
                                        "Fullscreen",
                                        id={
                                            "id": "graph-fullscreen-btn",
                                            "graph_id": "freq-analysis-chart",
                                        },
                                        className="fullscreen-btn m-0",
                                    ),
                                ],
                                class_name="metric-container",
                            ),
                            class_name="col-12 col-md-6 mt-4",
                        ),
                    ],
                    align="center",
                    justify="between",
                    class_name="mb-5",
                ),
                fullscreen_graph_modal,
            ],
            className="w-100 h-100 pb-5",
            style={"overflow": "scroll", "scroll-behavior": "smooth"},
        ),
        get_footer(add_logout_btn=True),
    ],
    id="dashboard-container",
    fluid=True,
    className="p-0 w-100",
)
