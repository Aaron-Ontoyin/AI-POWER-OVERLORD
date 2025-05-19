from dash import html
import dash_bootstrap_components as dbc


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
                        className="rounded-circle",
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

dashboard_ui = dbc.Container(
    [
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Container(
                                id="filters-container",
                                style={"min-height": 140},
                            ),
                            class_name="col-12 col-md-4 mt-1",
                        ),
                        dbc.Col(
                            dbc.Container(
                                class_name="metric-container",
                                style={"min-height": 140},
                            ),
                            class_name="col-12 col-md-3 mt-1",
                        ),
                        dbc.Col(
                            dbc.Container(
                                class_name="metric-container",
                                style={"min-height": 140},
                            ),
                            class_name="col-12 col-md-3 mt-1",
                        ),
                        dbc.Col(
                            dbc.Container(
                                [
                                    html.Img(
                                        src="assets/lyti.png",
                                        className="rounded-circle",
                                        style={"height": 60},
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                "Talk to", style={"color": "#555"}
                                            ),
                                            html.Span(
                                                "Lyti",
                                                className="glow-gradient mx-1",
                                            ),
                                            html.Div(className="pulse-circle"),
                                        ],
                                        n_clicks=0,
                                        id="lyti-container",
                                        className="mt-1 d-flex flex-row justify-content-center align-items-center",
                                    ),
                                    chat_canvas,
                                ],
                                class_name="d-flex flex-column justify-content-center align-items-center",
                                style={"min-height": 140},
                            ),
                            class_name="col-12 col-md-2 mt-1",
                        ),
                    ],
                    justify="between",
                    class_name="mt-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Container(
                                class_name="metric-container",
                                style={"min-height": 240},
                            ),
                            class_name="col-12 col-md-6 mt-4",
                        ),
                        dbc.Col(
                            dbc.Container(
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
                                class_name="metric-container",
                                style={"min-height": 240},
                            ),
                            class_name="col-12 col-md-6 mt-4",
                        ),
                        dbc.Col(
                            dbc.Container(
                                class_name="metric-container",
                                style={"min-height": 240},
                            ),
                            class_name="col-12 col-md-6 mt-4",
                        ),
                    ],
                    align="center",
                    justify="between",
                    class_name="mb-3",
                ),
            ],
            className="w-100 h-100",
            style={"overflow": "scroll"},
        ),
        html.Footer(
            [
                html.Span(
                    [
                        "Created by ",
                        html.A(
                            "Aaron Ontoyin",
                            href="https://aaronontoyin.tech/",
                            target="_blank",
                            className="mx-1",
                        ),
                        html.A("Arnold Bata", href="#", target="", className="mx-1"),
                        html.A(
                            "Ferguson Tetteh", href="#", target="", className="mx-1"
                        ),
                        html.A(
                            "Philip Blewushie", href="#", target="", className="mx-1"
                        ),
                    ],
                    className="me-3",
                ),
                dbc.Button(
                    "Logout",
                    id="logout-btn",
                    type="reset",
                    outline=True,
                    color="danger",
                    size="sm",
                ),
            ],
            className="w-100 text-end text-muted p-4",
            style={"fontSize": "0.6rem", "position": "absolute", "bottom": "0"},
        ),
    ],
    id="dashboard-container",
    fluid=True,
    className="p-0 w-100",
)
