import dash
import base64
import datetime
import io

import flask
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame

from GroundFloor import content0
from dash.dependencies import Input, Output


first = pd.read_excel("consumption.xlsx", "FirstFloor")

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True, prevent_initial_callbacks=True)


# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Medtech", className="display-4"),
        html.Hr(),
        html.P(
            "Electricity consumption and cost", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Floor 1", href="/floor-1", active="exact"),
                dbc.NavLink("Floor 2", href="/floor-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return [
            html.Div([html.Button("Download", id="btn"), Download(id="download"),
                      content0]),
        ]
    elif pathname == "/floor-1":
        return [
            content1
        ]
    elif pathname == "/floor-2":
        return [
            html.H1('consumption and cost of electricity in second floor',
                    style={'textAlign': 'center'}),

        ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

##################### download Button ##################


@app.callback(Output("download", "data"), [Input("btn", "n_clicks")])
def func(n_clicks):
    return send_data_frame(first.to_csv, "mydf.csv", index=False)

################################## First Floor ##################################


content1 = html.Div([dcc.Graph(id='barplot',
                               figure={'data': [
                                   go.Bar(x=first["Month"],
                                          y=first["consumption(670)"],

                                          marker={

                                       'color': 'rgb(200,204,53)',

                                   }
                                   )],
                                   'layout': go.Layout(title='consumption of counter 670 per month',
                                                       xaxis={
                                                           'title': '2019'}
                                                       )}
                               ),
                     dcc.Graph(id='barplot2',
                               figure={'data': [
                                   go.Bar(x=first["Month"],
                                          y=first["consumption(669)"],

                                          marker={

                                       'color': 'rgb(51,204,153)',

                                   }
                                   )],
                                   'layout': go.Layout(title='consumption of counter 669 per month',
                                                       xaxis={
                                                           'title': 'year 2019'}
                                                       )}
                               ),
                     dcc.Graph(id='barplot3',
                               figure={'data': [
                                   go.Bar(x=first["Month"],
                                          y=first["consumption(659)"],

                                          marker={

                                       'color': '#40E0D0',

                                   }
                                   )],
                                   'layout': go.Layout(title='consumption of counter 659 per month',
                                                       xaxis={
                                                           'title': '2019'}
                                                       )}
                               ),
                     dcc.Graph(id='barplot4',
                               figure={'data': [
                                   go.Bar(x=first["Month"],
                                          y=first["consumption(658)"],

                                          marker={

                                       'color': '#FFEBCD',

                                   }
                                   )],
                                   'layout': go.Layout(title='consumption of counter 658 per month',
                                                       xaxis={
                                                           'title': '2019'}
                                                       )}
                               )

                     ])


if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
