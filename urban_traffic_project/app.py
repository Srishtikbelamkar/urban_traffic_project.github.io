import streamlit as st
import pandas as pd
import plotly.express as px
from src.preprocessing import load_traffic_data,load_accident_data,clean_data
from src.analysis import peak_hour_analysis,congestion_by_hour,location_risk,weekday_weekend
from src.model import train_model,predict_one

st.set_page_config(page_title="Urban Traffic Analysis",page_icon="🚦",layout="wide")
st.title("🚦 Urban Traffic Congestion Analysis & Risk Prediction System")
st.caption("Traffic patterns • Peak hours • Accident zones • ML prediction")

@st.cache_data
def get_data():
    return clean_data(load_traffic_data()),load_accident_data()
df,accidents=get_data()

st.sidebar.header("Filters")
loc=st.sidebar.selectbox("Location",["All"]+sorted(df.Location.unique()))
wx=st.sidebar.selectbox("Weather",["All"]+sorted(df.Weather.unique()))
f=df.copy()
if loc!="All": f=f[f.Location==loc]
if wx!="All": f=f[f.Weather==wx]

c1,c2,c3,c4=st.columns(4)
c1.metric("Records",f"{len(f):,}")
c2.metric("Avg Traffic",f"{f.Traffic_Volume.mean():.0f}")
c3.metric("Avg Risk",f"{f.Risk_Score.mean():.1f}")
c4.metric("Accidents",f"{f.Accident_Count.sum():,}")

t1,t2,t3,t4=st.tabs(["📊 Traffic Analysis","🔥 Risk Map","🤖 ML Prediction","📋 Data"])

with t1:
    hourly=f.groupby("Hour",as_index=False).Traffic_Volume.mean()
    st.plotly_chart(px.line(hourly,x="Hour",y="Traffic_Volume",markers=True,
                            title="Traffic Volume vs Time"),use_container_width=True)
    st.plotly_chart(px.bar(peak_hour_analysis(f),x="Hour",y="Traffic_Volume",
                           title="Peak Congestion Hours"),use_container_width=True)
    st.plotly_chart(px.area(congestion_by_hour(f),x="Hour",y="Congestion_Score",
                            title="Congestion Intensity"),use_container_width=True)
    st.plotly_chart(px.bar(weekday_weekend(f),x="Is_Weekend",y="Traffic_Volume",
                           title="Weekday vs Weekend Traffic"),use_container_width=True)

with t2:
    risk=location_risk(f)
    fig=px.scatter_map(risk,lat="Latitude",lon="Longitude",size="Accidents",
                       color="Avg_Risk_Score",hover_name="Location",
                       hover_data=["Avg_Traffic","Accidents"],zoom=11,height=600)
    fig.update_layout(map_style="open-street-map")
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(risk,use_container_width=True)

with t3:
    choice=st.radio("ML Model",["Logistic Regression","Decision Tree"],horizontal=True)
    model,acc,report=train_model(f,"tree" if choice=="Decision Tree" else "logistic")
    st.metric("Model Accuracy",f"{acc*100:.2f}%")
    with st.expander("Classification Report"): st.text(report)

    a,b,c=st.columns(3)
    with a:
        vol=st.number_input("Traffic Volume",50,3000,1000)
        speed=st.number_input("Average Speed (km/h)",5.0,80.0,25.0)
    with b:
        ac=st.number_input("Accident Count",0,10,1)
        hr=st.slider("Hour",0,23,18)
    with c:
        wk=st.checkbox("Weekend")
        weather=st.selectbox("Weather",["Clear","Cloudy","Rain","Fog"])
    if st.button("🔮 Predict Congestion"):
        result=predict_one(model,vol,speed,ac,hr,wk,weather)
        st.success(f"Predicted Congestion Level: **{result}**")

with t4:
    st.dataframe(f,use_container_width=True)
    st.download_button("⬇️ Download Filtered CSV",f.to_csv(index=False),
                       "filtered_traffic.csv","text/csv")
