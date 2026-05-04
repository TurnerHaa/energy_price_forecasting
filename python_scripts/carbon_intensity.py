# ===============================
# import packages
# ===============================
import pandas as pd
import requests
from datetime import datetime as dt, timezone, timedelta
import time
import json
from pathlib import Path

# ===============================
# system paths
# ===============================
script_dir = Path(__file__).resolve().parents[1]
output_dir = script_dir / "temp_data"
output_dir.mkdir(parents=True, exist_ok=True)

# ===============================
# API request
# ===============================
# start_date = dt(2017, 9, 26, tzinfo=timezone.utc)
start_date = dt(2017, 9, 26, tzinfo=timezone.utc)
current_date = start_date + timedelta(days=30)
end_date = dt.now(timezone.utc)

url = f'https://api.carbonintensity.org.uk/intensity/{start_date.strftime('%Y-%m-%dT%H:%MZ')}/{current_date.strftime('%Y-%m-%dT%H:%MZ')}'

headers = {
    'Accept': 'application/json'
}

all_data = [] 
while current_date < end_date:
    try: 
        current_date = start_date + timedelta(days=30)

        response = requests.get(url=url, params={}, headers = headers)
        response.raise_for_status()

        current_data = response.json()

        if current_data:
            all_data.extend(current_data['data'])
            print(f"Fetched data from {start_date.strftime('%Y-%m-%dT%H:%MZ')} to {current_date.strftime('%Y-%m-%dT%H:%MZ')}. Total data: {len(all_data)} rows.")
        
        else:
            print(f"No data for {start_date}.")
            break

        start_date = current_date
        time.sleep(0.5)

    except Exception as e:
        print(f"Error accessing data: {e}")

print(f"Data obtained successfully: {len(all_data)} rows.")

if all_data:
    df = pd.json_normalize(
        all_data
    )

with open(f'{output_dir}/emissions.json', 'w') as fp:
    json.dump(all_data, fp, indent=4)    
