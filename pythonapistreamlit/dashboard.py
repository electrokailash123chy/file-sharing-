import streamlit as st
import requests
import pandas as pd
import time

API_URL = "http://localhost:8001/data"  # change after deployment

st.set_page_config(page_title="IoT Dashboard", layout="centered")
st.title("🌡 ESP32 IoT Live Dashboard")

placeholder = st.empty()

while True:
    try:
        res = requests.get(API_URL)
        data = res.json()

        if data:
            df = pd.DataFrame(data)
            df["temperature"] = df["temperature"].astype(float)
            df["humidity"] = df["humidity"].astype(float)

            with placeholder.container():
                st.subheader("Latest Readings")
                st.metric("Temperature (°C)", df.iloc[-1]["temperature"])
                st.metric("Humidity (%)", df.iloc[-1]["humidity"])

                st.line_chart(df[["temperature", "humidity"]])
        else:
            st.warning("Waiting for ESP32 data...")

    except:
        st.error("API not reachable")

    time.sleep(2)
