import streamlit as st
import pandas as pd
import requests

st.title("Horizon Bed Demand Forecast")

start_date = st.date_input("Start date")
end_date = st.date_input("End date")
ed_mult = st.slider("ED arrivals multiplier", 0.5, 1.5, 1.0, 0.05)
elec_mult = st.slider("Elective surgeries multiplier", 0.5, 1.5, 1.0, 0.05)

if st.button("Run forecast"):
    payload = {
        "start_date": str(start_date),
        "end_date": str(end_date),
        "scenario_ed_multiplier": ed_mult,
        "scenario_elective_multiplier": elec_mult,
    }
    resp = requests.post("http://api:8000/forecast", json=payload)
    st.json(resp.json())