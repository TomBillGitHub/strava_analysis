import pandas as pd
import argparse
import logging
import requests
import json
import subprocess
from cleansing import cleansing_steps
# from analysis.analysis import StravaAnalysis
from classes.refresh_token import Authentication

client_id = '139812'
client_secret = 'c3400b5ee2e89949f5799f4d67ae29e409844444'


########################################

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

########################################
########################################
########################################

def run(data):
    """
    Function to run all steps in analysis
    """

    # Cleanse the data
    tom_strava = cleansing_steps(data)
    tom_s = tom_strava.cleanse()

    if args.all == True or args.correlation == True:
        correlations = strava_analysis(tom_s)
        corr_heatmap = correlations.correlations()

########################################
########################################
########################################


if __name__=="__main__":

    # result = subprocess.run(['./request.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # data = json.loads(result.stdout)
    # df = pd.DataFrame(data)

    token = Authentication.authorise(client_id, client_secret)

    page = 1

    endpoint = f"https://www.strava.com/api/v3/athlete/activities?" \
                f"access_token={token['access_token']}&" \
                f"page={page}&" \
                f"per_page=10"
    
    response = requests.get(endpoint).json()
    r_data = pd.DataFrame(response)
    breakpoint()

    tom_strava_data = pd.read_csv('/workspaces/Portfolio/Strava/tom_strava_activities.csv')

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--all',
        action='store_true',
        help='Run all analysis'
    )

    parser.add_argument(
        '--correlation',
        action='store_true',
        help='Run only correlation analysis'
    )

    args = parser.parse_args()

    logger.info(f"Args called: {args}")


    ########################################
    ########################################
    ########################################

    run(tom_strava_data)