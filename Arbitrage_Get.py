import requests
import pandas as pd
import json
from datetime import datetime
import time

url = 'https://api.the-odds-api.com/v4/sports/basketball_nba/odds'

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
        print('Number of events:', len(odds_json))
        print(odds_json)

        # Check the usage quota
        print('Remaining requests', api_response.headers['x-requests-remaining'])
        print('Used requests', api_response.headers['x-requests-used'])
        
        # Save to csv
        time_now = datetime.now()
        current_time = time_now.strftime("%m_%d_%H_%M_%S")
        df = pd.DataFrame(odds_json)
        df["time"] = [current_time] * len(df)
        return df
    
def naive_scheduler(job_to_run, how_many_seconds_to_sleep = 5, max_iteration = 5):
    """
    runs the function provided job_to_run for max_iterations, and sleeps after how_many_seconds_to_sleep
    """
    
    list_of_dfs = []
    for i in range(max_iteration):
        job_time_now = time.time() 
        print("Running for run", i)
        df = job_to_run()
        list_of_dfs.append(df)

        time_used = time.time() - job_time_now

        to_sleep = how_many_seconds_to_sleep - time_used
        if(to_sleep > 0):
            print("Ready to sleep", to_sleep, "seconds")
            time.sleep(to_sleep) 
    
    odds_df = pd.concat(list_of_dfs)
    time_now = datetime.now()
    current_time = time_now.strftime("%m_%d_%H_%M")
    odds_df.to_excel(current_time + ".xlsx")
    
test_job = lambda: get_odds(API_KEY)
naive_scheduler(test_job, 3600, 5)


