import streamlit as st
import requests

st.title("Karachi AQI Dashboard")
data = requests.get("http://localhost:8000/predict").json()
st.metric("Current AQI", data["aqi"])
