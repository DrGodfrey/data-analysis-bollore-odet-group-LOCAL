import requests
from credentials import *

from datetime import datetime, timedelta
import json
import pymongo

try:
    client = pymongo.MongoClient("mongodb://localhost:27017")
    print("Connected at mongodb://localhost:27017")
except:
    print("Could not connect to MongoDB")


db = client["bollore_analysis_db"]
collection = db["timeseries_data_files"]     

# from credentials
my_api_key = alpha_vantage_api_key


def main(mongodb_collection=collection, maximum_stock_quote_age=86400):
    # If the time elapsed is greater than the maximum allowed age
    if check_time_point(mongodb_collection=mongodb_collection, maximum_stock_quote_age=maximum_stock_quote_age):
        # check_time_point handles timestamp validation (and updating) with mongoDB database
        print("A new request is being made.")
        for ticker in ['BOL.PA', 'ODET.PA', 'UMG.AMS', 'VIV.PA']:
            save_data_for(ticker=ticker)
            print(f"updated data for {ticker}")

    
def save_data_for(ticker="TSCO.LON", my_api_key=my_api_key, mongodb_collection=collection):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={my_api_key}'
    r = requests.get(url)
    json_data = r.json()

    file_name = f'{ticker.replace(".", "_")}.json'
    
    mongodb_collection.update_one({'_id': file_name},
                          {'$set': {'data': json_data}},
                          upsert=True)        


def check_time_point(mongodb_collection=collection, maximum_stock_quote_age=86400):
    # Read the last update timestamp from mongoDB
    try:
        last_update_str = mongodb_collection.find_one({'_id': 'last_update'})['last_update']        
        last_update = datetime.strptime(last_update_str, "%Y-%m-%d %H:%M:%S")

    except (FileNotFoundError, ValueError, TypeError) as e:
        # Handle the case when the value does not exist or the timestamp is invalid
        print(f"Error reading last update timestamp: {e}")
        print(f"Treat missing last update timestamp as 0AD (minimum)")
        last_update = datetime.min

    # Calculate the time elapsed since the last update
    time_elapsed = (datetime.now() - last_update).total_seconds()
    print(f"last data request: {time_elapsed}s")

    # If the time elapsed is greater than the maximum allowed age
    if time_elapsed > maximum_stock_quote_age:
        new_last_update = datetime.now()
        new_last_update_str = new_last_update.strftime("%Y-%m-%d %H:%M:%S")

        mongodb_collection.update_one({'_id': "last_update"},
                                {'$set': {'last_update': new_last_update_str}},
                                upsert=True)       
              
        return True
    else:
        print("Data up to date")
        print("Next request in ",maximum_stock_quote_age - time_elapsed,"s")
        return False   
    
    

if __name__ == "__main__":
    if (True):
        main()
    else:
        #For testing functions while (WIP)
        save_data_for()
        print("test complete")