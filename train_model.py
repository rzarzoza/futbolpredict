import warnings
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

warnings.filterwarnings("ignore")



features = Path("/Users/rzarzoza/Documents/Proyectos/futbolpredict/data/processed/features.csv")

df = pd.read_csv(features)
df = df.dropna()
df = df.replace([np.inf, -np.inf], np.nan).dropna()

print(df.shape)

df = pd.get_dummies(df, columns=["league"])
df = df[df["has_history"]==True]

y = df["result"]
x = df.drop(columns=["has_history", "result"])

# numerizes the data entries
le = LabelEncoder()
le.fit(["H", "D", "A"])

y = y.values
y = le.transform(y)

# normaliza los resultados para que sigan una desviacion estandar de 1 y una media de 0
scaler = StandardScaler()

x = x.values
x = scaler.fit_transform(x)



# divide los datos para entrenar los modelos siguiendo la proporcion natural de los resultados
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y)

# models
lr = LogisticRegression()
lr.fit(x_train, y_train)

rf = RandomForestClassifier(n_estimators=150, max_depth=8)
rf.fit(x_train, y_train)

xgb = XGBClassifier(n_estimators=150, max_depth = 5, learning_rate = 0.1)
xgb.fit(x_train, y_train)

# prediction
lr_pred = lr.predict(x_test)
rf_pred = rf.predict(x_test)
xgb_pred = xgb.predict(x_test)

# evaluation of results
print("Logistic Regression: \n", accuracy_score(y_test, lr_pred))
print("RandomForestClassifier: \n", accuracy_score(y_test, rf_pred))
print("XGB Classifier: \n", accuracy_score(y_test, xgb_pred))

print("------------------------------------------------------------")

print("Logistic Regression: \n", classification_report(y_test, lr_pred))
print("RandomForestClassifier: \n", classification_report(y_test, rf_pred))
print("XGB Classifier: \n", classification_report(y_test, xgb_pred))

