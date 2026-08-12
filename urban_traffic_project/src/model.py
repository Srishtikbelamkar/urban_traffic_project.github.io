import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

FEATURES=["Traffic_Volume","Average_Speed_kmph","Accident_Count","Hour","Is_Weekend","Weather"]
TARGET="Congestion_Level"

def train_model(df, model_type="logistic"):
    X=df[FEATURES].copy()
    y=df[TARGET].copy()
    pre=ColumnTransformer([
        ("num",StandardScaler(),["Traffic_Volume","Average_Speed_kmph","Accident_Count","Hour"]),
        ("cat",OneHotEncoder(handle_unknown="ignore"),["Is_Weekend","Weather"])
    ])
    clf = (DecisionTreeClassifier(max_depth=6,random_state=42)
           if model_type=="tree" else LogisticRegression(max_iter=2000))
    pipe=Pipeline([("preprocessor",pre),("model",clf)])
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.20,random_state=42,stratify=y)
    pipe.fit(Xtr,ytr)
    pred=pipe.predict(Xte)
    return pipe,accuracy_score(yte,pred),classification_report(yte,pred,zero_division=0)

def predict_one(model, traffic_volume, speed, accidents, hour, weekend, weather):
    row=pd.DataFrame([{
        "Traffic_Volume":traffic_volume,"Average_Speed_kmph":speed,
        "Accident_Count":accidents,"Hour":hour,
        "Is_Weekend":"Yes" if weekend else "No","Weather":weather
    }])
    return model.predict(row)[0]
