import requests
from credentials import *

from datetime import datetime, timedelta
import json
import os
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


def main(maximum_stock_quote_age=86400):
    # Read the last update timestamp from the "last_update.txt" file
    try:
        with open("data/last_update.txt", "r") as file:
            last_update_str = file.read().strip()
            if last_update_str:
                last_update = datetime.strptime(last_update_str, "%Y-%m-%d %H:%M:%S")
            else:
                raise ValueError("Last update timestamp is empty")
    except (FileNotFoundError, ValueError) as e:
        # Handle the case when the file does not exist or the timestamp is invalid
        print(f"Error reading last update timestamp: {e}")
        last_update = datetime.min

    # Calculate the time elapsed since the last update
    time_elapsed = (datetime.now() - last_update).total_seconds()
    print(f"last data request: {time_elapsed}s")

    # If the time elapsed is greater than the maximum allowed age
    if time_elapsed > maximum_stock_quote_age:
        print("A new request is being made.")
        for ticker in ['BOL.PA', 'ODET.PA', 'UMG.AMS', 'VIV.PA']:
            save_data_for(ticker=ticker)        

        # Update the last update timestamp to the current datetime
        new_last_update = datetime.now()
        
        # Write the updated timestamp to the "last_update.txt" file
        with open("data/last_update.txt", "w") as file:
            file.write(new_last_update.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        print("Data up to date")
        print("Next request in ",maximum_stock_quote_age - time_elapsed,"s")

    
def save_data_for(ticker="TSCO.LON", my_api_key=my_api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={my_api_key}'
    r = requests.get(url)
    json_data = r.json()

    current_directory = os.getcwd()
    file_name = f'{ticker.replace(".", "_")}.json'
    
    collection.update_one({'_id': file_name},
                          {'$set': {'data': json_data}},
                          upsert=True)        
      
    
    file_path = os.path.join(current_directory, "data", file_name )
    
    print(file_path)
    # file_path = os.path.join(file_path, 'downloads')
    # file_path = os.path.join(file_path, f'{ticker.replace(".", "_")}.json')
    
    with open(file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)


if __name__ == "__main__":
    if (False):
        main()
    else:
        save_data_for()
        print("test complete")