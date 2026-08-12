def peak_hour_analysis(df):
    return df.groupby("Hour",as_index=False)["Traffic_Volume"].mean()

def congestion_by_hour(df):
    return df.groupby("Hour",as_index=False)["Congestion_Score"].mean()

def location_risk(df):
    return (df.groupby(["Location","Latitude","Longitude"],as_index=False)
              .agg(Avg_Traffic=("Traffic_Volume","mean"),
                   Avg_Risk_Score=("Risk_Score","mean"),
                   Accidents=("Accident_Count","sum"))
              .sort_values("Avg_Risk_Score",ascending=False))

def weekday_weekend(df):
    return df.groupby("Is_Weekend",as_index=False)["Traffic_Volume"].mean()
