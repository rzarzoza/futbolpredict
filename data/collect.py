from pathlib import Path
import pandas as pd

directory_path = Path('/Users/rzarzoza/Documents/Proyectos/futbolpredict/data/raw')

csv_files = list(directory_path.glob("*.csv"))

df = pd.concat([pd.read_csv(file, low_memory=False) for file in csv_files], ignore_index=True)

df.to_csv("data/processed/all_matches.csv", index=False)

