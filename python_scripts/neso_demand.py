# ===============================
# import packages
# ===============================
import pandas as pd
import requests
from datetime import datetime as dt
import json
from pathlib import Path
from bs4 import BeautifulSoup
import re

# ===============================
# system paths
# ===============================
script_dir = Path(__file__).resolve().parents[1]
output_dir = script_dir / "data"

json_dir = output_dir / "json"
csv_dir = output_dir / "csv"

json_dir.mkdir(parents=True, exist_ok=True)
csv_dir.mkdir(parents=True, exist_ok=True)

# ===============================
# obtain data links
# ===============================
i = 2016
resource_ids = []

while i <= dt.today().year:
     data_url = f'https://www.neso.energy/data-portal/historic-demand-data/historic_demand_data_{i}'
     
     response = requests.get(data_url).text
     
     soup = BeautifulSoup(response, 'html.parser')

     for link in soup.find_all('a', href=re.compile(r'resource/.*\.csv$')):
          url = link.get('href')
          parts = url.split('/')

          if 'resource' in parts:
            res_id = parts[parts.index('resource') + 1]
            resource_ids.append(res_id)

     i += 1

# ===============================
# API request
# ===============================

all_data = []
offset = 0

print(f"Beginning data collection...")

for resource_id in [resource_ids[-1]]:
    offset = 0

    while True:
        try:
            full_url = f"https://api.neso.energy/api/3/action/datastore_search"
            params = {
                'resource_id': resource_id,
                'offset': offset,
                'limit': 1000
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

            print(f"Collected {total_records} entries...")
                    
            offset += 1000

        except Exception as e:
            print(f"Error ocurred: {e}")
            break


if all_data:
    df = pd.json_normalize(
        all_data
    )

    df.to_csv(csv_dir / 'demand.csv', index=False)
    print(f"Success! Saved {len(df)} rows.")

    output_file = json_dir / 'demand.json'

    with open(output_file, 'w') as fp:
                json.dump(all_data, fp, indent=4)