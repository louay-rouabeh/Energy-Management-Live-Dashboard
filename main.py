import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd


first = pd.read_excel("consumption.xlsx", "FirstFloor")

app = dash.Dash()
colors = {'backgound': '#111111', 'text': '#7FDBFF'}


app.layout = html.Div([dcc.Graph(id='barplot',
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
                                 )
                       ])

app.run_server()