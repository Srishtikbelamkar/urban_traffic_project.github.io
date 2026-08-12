# 🚦 Urban Traffic Congestion Analysis & Risk Prediction System

## Project Flow
Excel/CSV → Data Preprocessing → EDA → Peak-Hour Analysis → Congestion Pattern Detection → ML Prediction → Risk Map → Streamlit Dashboard

## Features
- Traffic volume vs time
- Peak congestion hours
- Congestion intensity
- Weekday vs weekend comparison
- Accident-prone location map
- Logistic Regression and Decision Tree prediction
- Interactive Streamlit dashboard

## Run
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Dataset
`data/urban_traffic_data.xlsx` contains:
- Traffic_Data sheet: 2,500 traffic records
- Accident_Data sheet: accident records with location, weather, traffic volume and severity
