import dash
from dash import Dash
from dash import dash_table
import pandas as pd
import os
 
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
 
app = dash.Dash(__name__, requests_pathname_prefix = '/{}/{}/r/notebookSession/{}/'.format(os.environ.get("DOMINO_PROJECT_OWNER"),os.environ.get("DOMINO_PROJECT_NAME"),os.environ.get("DOMINO_RUN_ID")))
 
app.layout = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
 
if __name__ == '__main__':
    app.run_server(port='8888', host='0.0.0.0')
