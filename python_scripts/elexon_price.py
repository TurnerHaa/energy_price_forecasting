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
output_dir = script_dir / "data"
output_dir.mkdir(parents=True, exist_ok=True)


# ===============================
# API request
# ===============================
url = "https://data.elexon.co.uk/bmrs/api/v1/generation/outturn/summary"
start_date = dt(2016, 4, 1, tzinfo=timezone.utc)
end_date = dt.now(timezone.utc)
chunk_size = timedelta(days=7)

all_data = []
current_start = start_date

print(f"Pulling data from {start_date} to present.")

while current_start < end_date:
    current_end = min(current_start + chunk_size, end_date)

    params = {
    'from': current_start,
    'to': current_end,
    'includeNegativeGeneration': 'true',
    'format': 'json'
    }

    try:
        response = requests.get(url=url, params=params)
        response.raise_for_status()

        chunk_data = response.json()

        if chunk_data:
                all_data.extend(chunk_data)
                print(f"Fetched: {current_start.date()} to {current_end.date()} ({len(chunk_data)} rows)")
        else:
            print(f"No data for: {current_start.date()}")

    except Exception as e:
            print(f"Error at {current_start}: {e}")

    current_start = current_end
    time.sleep(0.5)

if all_data:
    output_file = output_dir / "generation.json"
    with open(output_file, 'w') as fp:
         json.dump(all_data, fp, indent=4)



    df = pd.json_normalize(
        all_data, 
        record_path=['data'], 
        meta=['startTime', 'settlementPeriod']
    )
    
    cols = ['startTime', 'settlementPeriod', 'fuelType', 'generation']
    df = df[cols]
    
    df.to_csv(output_dir / 'csv/generation_mix_2016_2026.csv', index=False)
    print(f"Success! Saved {len(df)} rows.")