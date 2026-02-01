import streamlit as st
import pandas as pd
import requests

st.title("Horizon Bed Forecast")

st.sidebar.header("Inputs")
ed = st.sidebar.slider("ED arrivals", 0, 500, 120)
elec = st.sidebar.slider("Elective surgeries", 0, 100, 20)
dow = st.sidebar.selectbox("Day of week", list(range(7)), index=0)
month = st.sidebar.selectbox("Month", list(range(1, 13)), index=0)
weekend = st.sidebar.selectbox("Is weekend?", [0, 1], index=0)


st.sidebar.header("Scenario Simulation")

ed_change = st.sidebar.slider("Change ED arrivals (%)", -50, 50, 0)
elec_change = st.sidebar.slider("Change elective surgeries (%)", -50, 50, 0)

ed_adj = ed * (1 + ed_change / 100)
elec_adj = elec * (1 + elec_change / 100)


if st.button("Forecast"):
    payload = {
        "ed_arrivals": ed_adj,
        "elective_surgeries": elec_adj,
        "dow": dow,
        "month": month,
        "is_weekend": weekend
    }
    res = requests.post("http://localhost:8000/predict", json=payload)
    prediction = res.json()["prediction"]
    st.metric("Forecasted admissions", f"{prediction:.1f}")



from horizon_forecast.scenario.config import SCENARIOS

preset = st.sidebar.selectbox("Choose a preset", ["None"] + list(SCENARIOS.keys()))
if preset != "None":
    ed_adj = SCENARIOS[preset]["ed_arrivals"]
    elec_adj = SCENARIOS[preset]["elective_surgeries"]


with open("artifacts/metrics.json") as f:
    metrics = json.load(f)

st.sidebar.subheader("Model Performance")
for k, v in metrics.items():
    st.write(f"{k}: {v:.2f}")

    