import json
import request_data_av_with_mongodb
import pandas as pd

print("-- general functions loaded --")

from pymongo import MongoClient
# change this setting to use backup data-files in data folder
use_mongodb=True

if use_mongodb:
    client = MongoClient('mongodb://localhost:27017')
    db = client["bollore_analysis_db"]
    collection = db["timeseries_data_files"]
else:
    import os
    for dirname, _, filenames in os.walk('data'):
        for filename in filenames:
            print(os.path.join(dirname, filename))

def load_timeseries_df(ticker="BOL_PA", start_date='2021-09-21', use_mongodb=True):
    if use_mongodb:
        # Check data & update if necessary
        request_data_av_with_mongodb.main()
        # Read data from database
        data = collection.find_one({'_id': f'{ticker}.json'})["data"]
    else:
        with open(f'data/{ticker}.json') as json_file:
            data = json.load(json_file)
    
    timeseries_data = data["Time Series (Daily)"]

    df = pd.DataFrame(timeseries_data)
    df = df.transpose()
    
    # Backfill to start date with zeros
    date_range = pd.date_range(start=start_date, end=df.index.min(), freq='D')
    zero_df = pd.DataFrame(index=date_range, columns=df.columns).fillna(0).infer_objects()[::-1]
    df = pd.concat([df, zero_df])  
    
    # filter dates to relevant timeperiod
    df.index = pd.to_datetime(df.index)
    start_date = pd.to_datetime(start_date)
    df = df[df.index >= start_date]
            
    return df

