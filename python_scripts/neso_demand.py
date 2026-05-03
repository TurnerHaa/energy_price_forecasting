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
url_base = f"https://api.neso.energy/"
url_end = "api/3/action/datastore_search"


params = {
    'resource_id': '8a4a771c-3929-4e56-93ad-cdf13219dea5'
}

all_data = []
i = 1

print(f"Beginning data collection")


while url_end:
    try:
        full_url = f"{url_base}{url_end}"

        response = requests.get(url=full_url, params=params if i == 1 else None)
        response.raise_for_status()

        response = response.json()
        
        for entry in response['result'].get('records',[]):
            all_data.append(entry)
        
        i += 1
        print(f"Successfully pulled {i} pages of data. Total records: {len(all_data)}")
        
        url_end = response.get('result',{}).get('_links', {}).get('next',[])
        

    except Exception as e:
        print(f"Error ocurred: {e}")
        break


if all_data:
    df = pd.json_normalize(
        all_data
    )

    df.to_csv('temp_data/generation_test.csv', index=False)
    print(f"Success! Saved {len(df)} rows.")

# with open(f'{output_dir}/demand.json', 'w') as fp:
        #     json.dump(data, fp, indent=4)