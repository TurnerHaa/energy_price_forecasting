# ===============================
# import packages
# ===============================
import pandas as pd
from datetime import datetime as dt
from pathlib import Path

# ===============================
# system paths
# ===============================
script_dir = Path(__file__).resolve().parents[1]
output_dir = script_dir / "data"

csv_dir = output_dir / "csv"

csv_dir.mkdir(parents=True, exist_ok=True)

script_dir = Path(__file__).resolve().parents[1]
output_dir = script_dir / "data"

csv_dir = output_dir / "csv"
seeds_dir = script_dir / "energy_transform/seeds"

csv_dir.mkdir(parents=True, exist_ok=True)
seeds_dir.mkdir(parents=True, exist_ok=True)

# ===============================
# pull data
# ===============================
print('Beginning data collection...')

data = pd.read_csv('https://api.neso.energy/dataset/7a12172a-939c-404c-b581-a6128b74f588/resource/177f6fa4-ae49-4182-81ea-0c6b35f26ca6/download/demanddataupdate.csv')

data.to_csv(csv_dir / 'demand_update.csv', index=False)
data.to_csv(seeds_dir / 'demand_update.csv', index=False)

print(f'Success! Saved {len(data)} rows.')
