# Dash app modified to work on newer versions of dash packages.
# Also stores the external css file locally so that networking restrictions are not a problem.
# STEP 0: Fill in DOMINO_URL with your url below.
# STEP 1: Put this file into an "assets" folder to make the example work: 
#    https://codepen.io/chriddyp/pen/bWLwgP.css
# STEP 2 [if required]: Here are the relevant package versions:
#    dash==1.9.1
#    dash-core-components==1.8.1
#    dash-html-components==1.0.2
#    dash-renderer==1.2.4
#    dash-table==4.6.1
#  If the above are already in the compute environment, then app.sh will have only this line:
#    python app-dash.py
#  If the above are not already in the compute environment, add them to this file:
#    requirements_apps.txt
#  And then add the following to app.sh:
#    pip install -r requirements_apps.txt --user
#    python app-dash.py
# STEP 3 [for debugging]: When debugging in a workspace, two changes are needed (see code below):
#  Edit the definition of PATH_PREFIX
#  Change the port the app starts on

import os
import subprocess
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt  # replaces dash_table_experiments
import json
import pandas as pd
import numpy as np
import plotly


################################################################
# Configure app and path for dependencies. This is required for Domino.
# Learn more about Dash on Domino https://blog.dominodatalab.com/building-domino-web-app-dash/
#################################################################

DOMINO_URL = 'your Domino URL here'
# Use this definition of PATH_PREFIX when publishing in Domino
PATH_PREFIX = '/{}/{}/r/notebookSession/{}/'.format(
    os.environ.get("DOMINO_PROJECT_OWNER"),
    os.environ.get("DOMINO_PROJECT_NAME"),
    os.environ.get("DOMINO_RUN_ID")
)
# Use this definition of PATH_PREFIX when debugging in a Domino workspace
#PATH_PREFIX = '/{}/{}/notebookSession/{}/proxy/8887/'.format(
#    os.environ.get("DOMINO_PROJECT_OWNER"),
#    os.environ.get("DOMINO_PROJECT_NAME"),
#    os.environ.get("DOMINO_RUN_ID")
#)

# Set the external path to the assets folder
app = dash.Dash(assets_external_path = '{}{}assets/'.format(
    DOMINO_URL,
    PATH_PREFIX
),routes_pathname_prefix = '/',requests_pathname_prefix=PATH_PREFIX)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

# app.config.update({
# 'routes_pathname_prefix': '',
# 'requests_pathname_prefix': PATH_PREFIX
# })

################################################################
# Below callbacks are edited from the "vanilla quick-start"
#  in order to work with dash_table instead of dash_table_experiments
#################################################################

DF_WALMART = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/1962_2006_walmart_store_openings.csv')

DF_GAPMINDER = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv'
)
DF_GAPMINDER = DF_GAPMINDER[DF_GAPMINDER['year'] == 2007]
DF_GAPMINDER.loc[0:20]

DF_SIMPLE = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D', 'E', 'F'],
    'y': [4, 3, 1, 2, 3, 6],
    'z': ['a', 'b', 'c', 'a', 'b', 'c']
})

ROWS = [
    {'a': 'AA', 'b': 1},
    {'a': 'AB', 'b': 2},
    {'a': 'BB', 'b': 3},
    {'a': 'BC', 'b': 4},
    {'a': 'CC', 'b': 5},
    {'a': 'CD', 'b': 6}
]


app.layout = html.Div([
    html.H4('Gapminder DataTable'),
    dt.DataTable(
        data=DF_GAPMINDER.to_dict('records'),
        # optional - sets the order of columns
        columns=[{"name": i, "id": i} for i in sorted(DF_GAPMINDER.columns)],
        editable=False,
        row_selectable=True,
        filter_action='native',
        sort_action='native',
        selected_row_ids=[],
        id='datatable-gapminder'
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='graph-gapminder'
    ),
], className="container")

@app.callback(
    Output('datatable-gapminder', 'selected_row_ids'),
    [Input('graph-gapminder', 'clickData')],
    [State('datatable-gapminder', 'selected_row_ids')])
def update_selected_row_indices(clickData, selected_row_ids):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_ids:
                selected_row_ids.remove(point['pointNumber'])
            else:
                selected_row_ids.append(point['pointNumber'])
    return selected_row_ids


@app.callback(
    Output('graph-gapminder', 'figure'),
    [Input('datatable-gapminder', 'data'),
     Input('datatable-gapminder', 'selected_row_ids')])
def update_figure(data, selected_row_ids):
    dff = pd.DataFrame(data)
    fig = plotly.tools.make_subplots(
        rows=3, cols=1,
        subplot_titles=('Life Expectancy', 'GDP Per Capita', 'Population',),
        shared_xaxes=True)
    marker = {'color': ['#0074D9']*len(dff)}
    for i in (selected_row_ids or []):
        marker['color'][i] = '#FF851B'
    fig.append_trace({
        'x': dff['country'],
        'y': dff['lifeExp'],
        'type': 'bar',
        'marker': marker
    }, 1, 1)
    fig.append_trace({
        'x': dff['country'],
        'y': dff['gdpPercap'],
        'type': 'bar',
        'marker': marker
    }, 2, 1)
    fig.append_trace({
        'x': dff['country'],
        'y': dff['pop'],
        'type': 'bar',
        'marker': marker
    }, 3, 1)
    fig['layout']['showlegend'] = False
    fig['layout']['height'] = 800
    fig['layout']['margin'] = {
        'l': 40,
        'r': 10,
        't': 60,
        'b': 200
    }
    fig['layout']['yaxis3']['type'] = 'log'
    return fig



if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=8883) # Domino hosts all apps at 0.0.0.0:8888
#    app.run_server(host='0.0.0.0',port=8887) # Use a different port for debugging
