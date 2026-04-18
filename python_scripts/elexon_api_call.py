# ===============================
# import packages
# ===============================
import pandas as pd
import numpy as np
import requests
from datetime import datetime as dt, timezone, timedelta
from pathlib import Path

# ===============================
# API request
# ===============================

# define url and parameters
start_date = "2025-04-13"
original_start_date = start_date
end_date = dt.now(timezone.utc).strftime('%Y-%m-%d')
i = 1
full_data = []

while start_date <= end_date:
    print(f"Obtaining data for {start_date}.")

    # make and check API request
    data_url = f"https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/{start_date}"
    
    response = requests.get(data_url)

    if response.status_code != 200:
        print("Failed to retrieve package info:", response.text)
        exit(1)
    else:
        print(f"API retrieved successfully x{i}.")

    # piece in here abour saving JSON file
    data = response.json()

    try:
        for entry in data.get('data', []):
            full_data.append(entry)
    except (IndexError, KeyError, TypeError):
        data = None
        print("Failed to pass data into dictionary. Dictionary or values missing")

    # increase start_date for API call by one day
    start_date = dt.strptime(start_date, "%Y-%m-%d")

    start_date = (start_date + timedelta(days = 1)).strftime("%Y-%m-%d")

    i += 1

print(f"Script ended. {i} entries added to data.")

print(f"Saving file as system_prices_{original_start_date}_to_{end_date}.csv")



# ===============================
# save data
# ===============================
try:
    script_dir = Path(__file__).resolve().parent

    target_dir = script_dir.parent / 'transform/seeds'

    target_dir.mkdir(parents=True, exist_ok=True)

    file_path = target_dir / f'system_prices.csv'

    full_data_pd = pd.DataFrame(full_data)

    full_data_pd.to_csv(file_path, index=False)

    print(f"File saved successfully to: {file_path}")
except Exception as e:
    print(f"Error trying to save csv: {e}")

