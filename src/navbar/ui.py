from dash import html
import dash_bootstrap_components as dbc


navbar_ui = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                html.Img(
                                    src="assets/logo.png",
                                    alt="Enerlytics",
                                    height="50px",
                                )
                            )
                        ],
                        width="auto",
                        class_name="p-0",
                    ),
                    dbc.Col(
                        [
                            html.I(id="user-name-check", **{"aria-hidden": "true"}),  # type: ignore
                            html.Span(
                                style={
                                    "fontWeight": "bold",
                                    "color": "#454c5a",
                                    "fontSize": "0.8rem",
                                },
                                id="user-name-value",
                            ),
                        ],
                        id="data-id",
                        width="auto",
                    ),
                ],
                className="w-100 d-flex justify-content-between align-items-center m-0 p-2",
            )
        ],
        fluid=True,
        className="m-0 p-0",
        style={"background": "aliceblue"},
    ),
    class_name="p-0 m-0",
    style={
        "boxShadow": "0px 4px 8px rgba(0, 0, 255, 0.03)",
        "width": "100vw",
        "zIndex": 2,
    },
)
