from dash import Dash, dash_table
import pandas as pd
import os 

# # Configure Dash to recognize the URL of the container
# user = os.environ.get("DOMINO_PROJECT_OWNER")
# project = os.environ.get("DOMINO_PROJECT_NAME")
# runid = os.environ.get("DOMINO_RUN_ID")
# runurl = '/' + user + '/' + project + '/r/notebookSession/'+ runid + '/' 




# app = Dash(__name__,
#            routes_pathname_prefix='/',
#            requests_pathname_prefix=runurl,
#            # external_stylesheets=[dbc.themes.BOOTSTRAP],
#            # static_folder='static',
#            # url_base_pathname=runurl
#            # serve_locally = False
#           )

DOMINO_URL = 'https://fldfive8383.cs.domino.tech/'
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
app = Dash(assets_external_path = '{}{}assets/'.format(DOMINO_URL,PATH_PREFIX),routes_pathname_prefix= '/',requests_pathname_prefix= PATH_PREFIX)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

app.layout = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])

if __name__ == '__main__':
    app.run_server(port=8885, host='0.0.0.0')
    
    
    
