import pandas as pd

def load_traffic_data(path="data/traffic_data.csv"):
    df = pd.read_csv(path)
    df["DateTime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
    df["Hour"] = df["DateTime"].dt.hour
    df["DayOfWeek"] = df["DateTime"].dt.dayofweek
    return df

def load_accident_data(path="data/accident_data.csv"):
    df = pd.read_csv(path)
    df["DateTime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
    return df

def clean_data(df):
    df = df.copy()
    for col in ["Traffic_Volume","Average_Speed_kmph","Accident_Count",
                "Congestion_Score","Risk_Score"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())
    return df.dropna(subset=["Location","Congestion_Level"])
