
# ⚽ FutbolPredict

A machine learning system that predicts football match outcomes (home win, draw, or away win) using historical match data from Europe's top 5 leagues.

## What it does

FutbolPredict analyzes historical match data to build predictive features like recent form, goals scored/conceded, shots on target, and corners. It trains and compares three classification models to estimate the probability of each result.

## Leagues covered

- La Liga (Spain)
- Premier League (England)
- Bundesliga (Germany)
- Serie A (Italy)
- Ligue 1 (France)

## How it works

1. **Data collection** — Match results and stats from 7+ seasons across 5 leagues sourced from football-data.co.uk
2. **Feature engineering** — Rolling stats per team calculated chronologically to avoid data leakage: form (avg points over last 5 matches), goals for/against, shots, shots on target, corners, plus derived features like form_diff and goals_diff
3. **Model training** — Three models compared:
   - Logistic Regression: ~51%
   - Random Forest: ~50%
   - XGBoost: ~50%
   - Naive baseline (always predict home win): ~43%

## Project structure

```
futbolpredict/
├── data/
│   ├── raw/                  # Original CSVs from football-data.co.uk
│   └── processed/
│       ├── all_matches.csv   # Combined dataset
│       └── features.csv      # Calculated features for training
├── models/                   # Trained models (.pkl)
├── feature_engineering.py    # Builds rolling features per team
├── train_model.py            # Trains and evaluates models
├── requirements.txt
└── README.md
```

## Running locally

### Prerequisites (Mac)
```bash
brew install libomp
```

### Setup
```bash
git clone https://github.com/yourusername/futbolpredict.git
cd futbolpredict
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Download data
Download CSV files from [football-data.co.uk](https://www.football-data.co.uk/data.php) for each league and season, place them in `data/raw/`.

### Train
```bash
python feature_engineering.py
python train_model.py
```

## Note on accuracy

Football is inherently unpredictable. A three-class problem (home/draw/away) where even professional betting models top out around 52-55%. All three models consistently beat the naive baseline (~43%), which validates that the features capture real patterns.

## Stack

Python, pandas, NumPy, scikit-learn, XGBoost

## Built by

A CS student at Rice University who watches too much football.
```