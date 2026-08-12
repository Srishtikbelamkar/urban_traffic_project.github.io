import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("data/traffic_data.csv")
df["DateTime"]=pd.to_datetime(df["Date"]+" "+df["Time"])
df["Hour"]=df["DateTime"].dt.hour
hourly=df.groupby("Hour")["Traffic_Volume"].mean()

plt.figure(figsize=(10,5))
plt.plot(hourly.index,hourly.values,marker="o")
plt.xlabel("Hour"); plt.ylabel("Average Traffic Volume")
plt.title("Traffic Volume vs Time"); plt.grid(True); plt.tight_layout()
plt.show()
