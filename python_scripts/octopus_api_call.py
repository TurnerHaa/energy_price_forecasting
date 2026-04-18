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
params = {
    'period_from':'2025-01-01T00:00Z', 
    'period_to': dt.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')}

full_data = []

data_url = f"https://api.octopus.energy/v1/products/AGILE-FLEX-22-11-25/electricity-tariffs/E-1R-AGILE-FLEX-22-11-25-C/standard-unit-rates/"

response = requests.get(data_url, params=params)

if response.status_code != 200:
    print("Failed to retrieve package info:", response.text)
    exit(1)
else: 
    print("API retrieved successfully.")

data = response.json()

try:
    result_list = data.get('results', [])
    if result_list:
        full_data.extend(result_list)
        print(f"Successfully added {len(full_data)} entries.")
    else:
        print(f"No results found in API response.")

except Exception as e:
    print(f"Failed to process data: {e}")

print("Data saved successfully.")

print(pd.DataFrame(full_data).head())