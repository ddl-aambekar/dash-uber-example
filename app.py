from dash import Dash, dash_table
import pandas as pd
import os 

app = Dash(__name__)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

# Configure Dash to recognize the URL of the container
user = os.environ.get("DOMINO_PROJECT_OWNER")
project = os.environ.get("DOMINO_PROJECT_NAME")
runid = os.environ.get("DOMINO_RUN_ID")
runurl = '/' + user + '/' + project + '/r/notebookSession/'+ runid + '/'

app.config.update({
'routes_pathname_prefix': runurl,
'requests_pathname_prefix': runurl
})


app.layout = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])

if __name__ == '__main__':
    app.run_server(port=8888, host='0.0.0.0', debug=True)
