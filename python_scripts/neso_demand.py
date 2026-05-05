# ===============================
# import packages
# ===============================
import pandas as pd
import requests
from datetime import datetime as dt
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

all_data = []
offset = 0

print(f"Beginning data collection...")
 

while True:
    try:
        full_url = f"https://api.neso.energy/api/3/action/datastore_search"
        params = {
            'resource_id': '8a4a771c-3929-4e56-93ad-cdf13219dea5',
            'offset': offset
        }

        response = requests.get(url=full_url, params=params)
        response.raise_for_status()
        data = response.json()

        records = data.get('result', {}).get('records', [])
        total_records = data.get('result', {}).get('total', 0)

        if not records:
            print("No more records found. Exiting.")
            break
        
        all_data.extend(records)

        print(f"Collected {len(all_data)} of {total_records}...")
                
        offset += 100

    except Exception as e:
        print(f"Error ocurred: {e}")
        break


if all_data:
    df = pd.json_normalize(
        all_data
    )

    df.to_csv('temp_data/generation_test.csv', index=False)
    print(f"Success! Saved {len(df)} rows.")

with open(f'{output_dir}/demand.json', 'w') as fp:
            json.dump(data, fp, indent=4)