from datetime import date

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from ..footer_ui import get_footer
from .plots import create_consumption_patterns_fig


chat_canvas = html.Div(
    [
        dbc.Offcanvas(
            [
                html.P(
                    "Explore the distribution data? Just ask Lyti!", id="lyti-greeting"
                )
            ],
            id="chat-canvas",
            placement="end",
            scrollable=True,
            title=html.Div(
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
                ],
                className="d-flex justify-content-center align-items-center",
            ),
            is_open=False,
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
            [
                dmc.Card(
                    [
                        dmc.CardSection(
                            [
                                "Header",
                                html.I(
                                    className="fa fa-circle fa-tiny me-3 text-success"
                                ),
                            ],
                            className="text-muted fs-5 d-flex justify-content-between align-items-center",
                        ),
                        dmc.CardSection(
                            "Some quick example text to build on the card title and make up the bulk of the card's content.",
                            className="text-muted fs-6",
                        ),
                    ],
                    className="bg-light p-4 text-dark mb-3",
                ),
                dmc.Card(
                    [
                        dmc.CardSection(
                            [
                                "Header",
                                html.I(
                                    className="fa fa-circle fa-tiny me-3 text-warning"
                                ),
                            ],
                            className="text-muted fs-5 d-flex justify-content-between align-items-center",
                        ),
                        dmc.CardSection(
                            "Some quick example text to build on the card title and make up the bulk of the card's content.",
                            className="text-muted fs-6",
                        ),
                    ],
                    className="bg-light p-4 text-dark mb-3",
                ),
                dmc.Card(
                    [
                        dmc.CardSection(
                            [
                                "Header",
                                html.I(
                                    className="fa fa-circle fa-tiny me-3 text-danger"
                                ),
                            ],
                            className="text-muted fs-5 d-flex justify-content-between align-items-center",
                        ),
                        dmc.CardSection(
                            "Some quick example text to build on the card title and make up the bulk of the card's content.",
                            className="text-muted fs-6",
                        ),
                    ],
                    className="bg-light p-4 text-dark mb-3",
                ),
                dmc.Card(
                    [
                        dmc.CardSection(
                            [
                                "Header",
                                html.I(
                                    className="fa fa-circle fa-tiny me-3 text-muted"
                                ),
                            ],
                            className="text-muted fs-5 d-flex justify-content-between align-items-center",
                        ),
                        dmc.CardSection(
                            "Some quick example text to build on the card title and make up the bulk of the card's content.",
                            className="text-muted fs-6",
                        ),
                    ],
                    className="bg-light p-4 text-dark mb-3",
                ),
            ],
            id="signal-stream-canvas",
            scrollable=True,
            title=html.Div(
                [
                    html.I(
                        className="fa fa-bell text-muted me-3",
                        **{"aria-hidden": "true"}
                    ),
                    html.Div("Alerts!", className="text-muted fs-5"),
                ],
                className="d-flex justify-content-center align-items-center",
            ),
            is_open=False,
        ),
    ]
)

dashboard_ui = dbc.Container(
    [
        dbc.Container(
            [
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
                                                                    value=date.today(),
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
                                class_name="shadow-sm border-0",
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
                                                                html.Span(
                                                                    "40",
                                                                    id="total-transformers",
                                                                    className="metric-value",
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
                                                                html.Span(
                                                                    "300",
                                                                    id="total-meters",
                                                                    className="metric-value",
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
                                                                    [
                                                                        html.Span(
                                                                            "Tongo District",
                                                                            className="area-covered",
                                                                        ),
                                                                        html.Span(
                                                                            "Kabwe Metropolitan Province",
                                                                            className="area-covered",
                                                                        ),
                                                                        html.Span(
                                                                            "Upper West",
                                                                            className="area-covered",
                                                                        ),
                                                                        html.Span(
                                                                            "North-Western",
                                                                            className="area-covered",
                                                                        ),
                                                                        html.Span(
                                                                            "Southern",
                                                                            className="area-covered",
                                                                        ),
                                                                        html.Span(
                                                                            "Copperbelt",
                                                                            className="area-covered",
                                                                        ),
                                                                        html.Span(
                                                                            "Eastern",
                                                                            className="area-covered",
                                                                        ),
                                                                    ],
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
                                class_name="shadow-sm border-0",
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
                                                "99+",
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
                                        id="consumption-patterns-chart",
                                        figure=create_consumption_patterns_fig(),
                                        style={"border-radius": "50px"},
                                    )
                                ],
                                class_name="metric-container",
                                style={"min-height": 240},
                            ),
                            class_name="col-12 col-md-6 mt-4",
                        ),
                        dbc.Col(
                            dbc.Container(
                                [
                                    dcc.Graph(
                                        id="trend-analysis-chart",
                                        figure=create_consumption_patterns_fig(),
                                    )
                                ],
                                class_name="metric-container",
                                style={"min-height": 240},
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
                                    dcc.Graph(
                                        id="anomaly-chart",
                                        figure=create_consumption_patterns_fig(),
                                    )
                                ],
                                class_name="metric-container",
                                style={"min-height": 240},
                            ),
                            class_name="col-12 col-md-6 mt-4",
                        ),
                        dbc.Col(
                            dbc.Container(
                                [
                                    dcc.Graph(
                                        id="freq-analysis-chart",
                                        figure=create_consumption_patterns_fig(),
                                    )
                                ],
                                class_name="metric-container",
                                style={"min-height": 240},
                            ),
                            class_name="col-12 col-md-6 mt-4",
                        ),
                    ],
                    align="center",
                    justify="between",
                    class_name="mb-5",
                ),
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
