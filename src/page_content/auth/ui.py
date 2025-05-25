from dash import html, dcc
import dash_bootstrap_components as dbc

from ..footer_ui import get_footer


login_form = dbc.Form(
    dbc.Col(
        [
            dbc.Row(
                dbc.Input(
                    type="password",
                    placeholder="Authentication key",
                    size="sm",
                    id="auth-key",
                ),
                className="",
            ),
            dbc.Row(
                dbc.Button(
                    "Authorize",
                    color="primary",
                    type="submit",
                    id="auth-btn",
                    class_name="btn-sm mt-4",
                ),
                style={"width": "fit-content"},
            ),
        ],
        className="d-flex flex-column align-items-center",
    ),
    style={"width": "fit-content"},
)


markdown_highlight_style = {
    "backgroundColor": "rgba(0, 0, 230, 0.07)",
    "color": "#000b3d",
    "borderRadius": "5px",
    "padding": "0 5px",
    "fontSize": "1rem",
}

lean_more_modal = dbc.Modal(
    [
        dbc.ModalHeader("Enerlytics"),
        dbc.ModalBody(
            [
                "Enerlytics is an AI-powered smart metering and analytics platform designed to optimize electricity distribution and management. Our system leverages real-time data from smart meters to detect anomalies, monitor energy usage patterns, and provide actionable insights for utility providers.",
                html.Br(),
                "By combining ",
                html.Span("Intelligent Algorithms ", style=markdown_highlight_style),
                "with modern visualization tools, Enerlytics enables faster decision-making, reduced energy loss, and improved efficiency across the power grid.",
                html.Br(),
                "Whether you're managing transformers, tracking consumption, or preventing fraud, Enerlytics gives you the tools to do it smarter.",
            ],
            className="fs-6",
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Close", id="learn-more-close-btn", className="btn btn-info btn-sm"
            )
        ),
    ],
    id="learn-more-modal",
    size="lg",
    centered=True,
    backdrop="static",
    keyboard=False,
)
auth_modal = dbc.Modal(
    [
        dbc.ModalHeader(
            [
                dbc.ModalTitle("Authorization", className="fs-6"),
                dcc.Loading(
                    display="show",
                    className="me-5",
                    id="auth-loading-icon",
                ),
            ],
            class_name="d-flex justify-content-between pe-4",
            close_button=False,
            id="auth-modal-header",
        ),
        dbc.ModalBody(id="auth-modal-body", class_name="fs-6"),
        dbc.ModalFooter(
            dbc.Button(
                "Close",
                id="auth-modal-close-btn",
                class_name="btn btn-info me-2",
                style={"width": "100px"},
            )
        ),
    ],
    id="auth-modal",
    keyboard=False,
    backdrop="static",
    centered=True,
    size="md",
)

auth_ui = dbc.Container(
    [
        dbc.Container(
            [
                dbc.Container(
                    [
                        dbc.Row(
                            login_form,
                            className="h-50 d-flex justify-content-center align-items-center pe-md-5",
                        ),
                        dbc.Row(className="h-50 d-none d-md-block"),
                    ],
                    className="h-100",
                ),
                dbc.Container(className="h-100 d-none d-md-block"),
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                html.Img(
                                    src="assets/trans.png",
                                    className="img-fluid w-75 d-none d-lg-block",
                                )
                            ],
                            className="h-50 d-none d-md-flex justify-content-end pe-lg-5",
                        ),
                        dbc.Row(
                            [
                                html.Div(
                                    [
                                        html.Span(
                                            "Enerlytics", style=markdown_highlight_style
                                        ),
                                        "empowers smarter energy distribution through real-time analytics and intelligent monitoring — ",
                                        html.A(
                                            "Learn more", id="learn-more-link", href="#"
                                        ),
                                    ],
                                    className="text-center pe-md-5 pt-5 pt-md-0 text-muted fs-6",
                                ),
                            ],
                            className="h-50 d-flex justify-content-center align-items-center pe-md-5 pt-5 pt-md-0",
                        ),
                    ],
                    className="h-100",
                ),
                auth_modal,
                lean_more_modal,
            ],
            fluid=True,
            class_name="d-flex justify-content-center flex-column flex-md-row align-items-center h-100 w-100",
        ),
        get_footer(add_logout_btn=False),
    ],
    id="sign-in-container",
    fluid=True,
    style={
        "backgroundImage": "url('assets/bgs.jpg')",
        "backgroundSize": "cover",
        "backgroundPosition": "center",
        "backgroundRepeat": "no-repeat",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "zIndex": 2,
    },
)
