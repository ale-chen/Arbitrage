import time
import requests
import pandas as pd
import json
from datetime import datetime
import time

# Show that the process is starting
print("Starting the job at", time.ctime(time.time()))


# Execute the api call
url = 'https://api.the-odds-api.com/v4/sports/basketball_nba/odds'
# PASS IN YOUR API KEY HERE
API_KEY = 'da66357d0212ad8c30a55e21a99e9954'
REGIONS = 'us'
ODDS_FORMAT = 'decimal'
MARKETS = 'h2h,spreads'
DATE_FORMAT = 'iso'

STAKE: float = 500.0

def get_odds(curr_api_key):
    """
    get odds data from the odds api using the curr_api_key.
    """
    my_params={
    'apiKey': curr_api_key,
    'regions': REGIONS,
    'oddsFormat': ODDS_FORMAT,
    'dateFormat': DATE_FORMAT
    }

    api_response = requests.get(url, params = my_params)

    if api_response.status_code != 200:
        print(f'Failed to get odds: status_code {api_response.status_code}, response body {api_response.text}')

    else:
        odds_json = api_response.json()

        # Check the usage quota
        print('Remaining requests', api_response.headers['x-requests-remaining'])
        print('Used requests', api_response.headers['x-requests-used'])

        # Save to csv
        time_now = datetime.now()
        current_time = time_now.strftime("%m/%d/%H/%M/%S")
        df = pd.DataFrame(odds_json)
        print("getting", len(df), "rows of data...")
        df["time"] = [current_time] * len(df)
        time_now = datetime.now()
        current_time = time_now.strftime("%m_%d_%H_%M")
        df.to_excel(current_time + ".xlsx")

get_odds(API_KEY)

# FINSIHED and going to sleep for a time marked by
# while :; do python3 get_data_show.py; sleep 5; done
print("End of the job at", time.ctime(time.time()))
