from dash import html
import dash_bootstrap_components as dbc


def get_footer(add_logout_btn: bool = False):
    return html.Footer(
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
                    html.A("Ferguson Tetteh", href="#", target="", className="mx-1"),
                    html.A("Philip Blewushie", href="#", target="", className="mx-1"),
                ],
                className="me-3",
            ),
            (
                dbc.Button(
                    "Logout",
                    id="logout-btn",
                    type="reset",
                    outline=True,
                    color="danger",
                    size="sm",
                )
                if add_logout_btn
                else None
            ),
        ],
        className="w-100 text-end text-muted p-4",
        style={"fontSize": "0.6rem", "position": "absolute", "bottom": "0"},
    )
