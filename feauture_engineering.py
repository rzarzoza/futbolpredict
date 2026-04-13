import pandas as pd
from numpy import mean
from pathlib import Path

path = Path("/Users/rzarzoza/Documents/Proyectos/futbolpredict/data/processed/all_matches.csv")

df = pd.read_csv(path, low_memory=False)

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, format="mixed")
df = df.sort_values("Date")
rows = []

leagues_names = {
    "D1": "germany",
    "E0": "england",
    "F1": "france",
    "I1": "italy",
    "SP1": "spain"
}

#iteramos por liga
for league in df["Div"].unique():
    df_league = df[df["Div"]==league]
    all_teams = set(df_league["HomeTeam"].unique()) | set(df_league["AwayTeam"].unique())

    # creamos un histograma que almacena esta informacion por equipo 
    history = {team: {"pts": [], 
                      "gf":[], 
                      "ga":[], 
                      "sot":[], 
                      "shots":[], 
                      "corners":[],

                      } for team in all_teams}

    for index, match in df_league.iterrows():
        # teams in the match
        hteam = match["HomeTeam"]
        ateam = match["AwayTeam"]

        if(len(history[hteam]["pts"][-5:])!=0 and len(history[ateam]["pts"][-5:])!=0):
            has_history = True if len(history[hteam]["pts"][-5:])>=3 and len(history[ateam]["pts"][-5:])>=3 else False
            
            home_form = mean(history[hteam]["pts"][-5:])
            away_form = mean(history[ateam]["pts"][-5:])

            home_gf = mean(history[hteam]["gf"][-5:])
            away_gf = mean(history[ateam]["gf"][-5:])

            home_ga = mean(history[hteam]["ga"][-5:])
            away_ga = mean(history[ateam]["ga"][-5:])

            home_shots = mean(history[hteam]["shots"][-5:])
            away_shots = mean(history[ateam]["shots"][-5:])

            home_sot = mean(history[hteam]["sot"][-5:])
            away_sot = mean(history[ateam]["sot"][-5:])

            home_corners = mean(history[hteam]["corners"][-5:])
            away_corners = mean(history[ateam]["corners"][-5:])

            rows.append({
                "home_form": home_form,
                "home_gf": home_gf,
                "home_ga": home_ga,
                "home_shots": home_shots,
                "home_sot": home_sot,
                "home_corners": home_corners,

                "away_form": away_form,
                "away_gf": away_gf,
                "away_ga": away_ga,
                "away_shots": away_shots,
                "away_sot": away_sot,
                "away_corners": away_corners,

                "form_diff": home_form - away_form,
                "goals_diff": home_gf - away_gf,
                "shots_diff": home_shots - away_shots,
                "sot_diff": home_sot - away_sot,
                "corners_diff": home_corners - away_corners,

                "has_history": has_history,
                "result": match["FTR"],
                "league": leagues_names[league] 

            })
        

        # goals
        hgoals = match["FTHG"]
        agoals = match["FTAG"]

        # shots on target
        hsot = match["HST"]
        asot = match["AST"]

        # shots
        hshots = match["HS"]
        ashots = match["AS"]

        # corners
        hcorn = match["HC"]
        acorn = match["AC"]

        history[hteam]["pts"].append(3 if hgoals>agoals else (1 if hgoals==agoals else 0))
        history[ateam]["pts"].append(3 if agoals>hgoals else (1 if hgoals==agoals else 0))

        history[hteam]["gf"].append(hgoals)
        history[ateam]["gf"].append(agoals)
        
        history[hteam]["ga"].append(agoals)
        history[ateam]["ga"].append(hgoals)

        history[hteam]["shots"].append(hshots)
        history[ateam]["shots"].append(ashots)

        history[hteam]["sot"].append(hsot)
        history[ateam]["sot"].append(asot)

        history[hteam]["corners"].append(hcorn)
        history[ateam]["corners"].append(acorn)


pd.DataFrame(rows).to_csv("data/processed/features.csv")