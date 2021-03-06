import base64
import io
from app import app
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from sqlalchemy import create_engine
import dash

engine = create_engine('sqlite:///data.db', echo=False)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

drop = html.Div([
    dcc.Upload(
        id='datatable-upload',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed',
            'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
        },
    ),
    dash_table.DataTable(id='datatable-upload-container', editable=True, export_format='xlsx',
                         export_headers='display',
                         merge_duplicate_headers=True),
    dcc.Graph(id='datatable-upload-graph'),
    html.Div(id="output-data-upload1"),
    dcc.Input(
        id='sql-query',
        value='SELECT * FROM "data1.db"',
        style={'width': '100%'},
        type='text'
    ),
    html.Button('Run Query', id='run-query'),

    html.Hr(),

    html.Div([
        html.Div(id='table-container', className="four columns"),

        html.Div([
            html.Div([
                html.Div([
                    html.Label('Select X'),
                    dcc.Dropdown(
                        id='dropdown-x',
                        clearable=False,
                    )
                ], className="six columns"),
                html.Div([
                    html.Label('Select Y'),
                    dcc.Dropdown(
                        id='dropdown-y',
                        clearable=False,
                    )
                ], className="six columns")
            ], className="row"),
            html.Div(dcc.Graph(id='graph'), className="ten columns")
        ], className="eight columns")
    ], className="row"),

    # hidden store element
    html.Div(id='table-stored', style={'display': 'none'})
])


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded))


@app.callback(Output('datatable-upload-container', 'data'),
              Output('datatable-upload-container', 'columns'),
              Input('datatable-upload', 'contents'),
              State('datatable-upload', 'filename'))
def update_output(contents, filename):
    if contents is None:
        return [{}], []
    df = parse_contents(contents, filename)
    df = df.set_index(df.columns[2])
    df.to_sql('data.db', con=engine, if_exists='replace')
    return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]


@app.callback(Output('datatable-upload-graph', 'figure'),
              Input('datatable-upload-container', 'data'))
def display_graph(rows):
    df = pd.DataFrame(rows)

    if df.empty or len(df.columns) < 1:
        return {
            'data': [{
                'x': [],
                'y': [],
                'type': 'bar'
            }]
        }
    return {
        'data': [{
            'x': df[df.columns[1]],
            'y': df[df.columns[0]],
            'type': 'bar'
        }]
    }


@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    [Input('Datatable-interactivity', 'selected_columns')]
)
def update_styles(selected_columns):
    for i in selected_columns:
        [{
            'if': {'column_id': i},
            'background_color': '#D2F3FF'
        }]

@app.callback(
    dash.dependencies.Output('table-stored', 'children'),
    [dash.dependencies.Input('run-query', 'n_clicks')],
    state=[dash.dependencies.State('sql-query', 'value')])
def sql(number_of_times_button_has_been_clicked, sql_query):
    dff = pd.read_sql_query(
        sql_query,
        engine
    )
    return dff.to_json()