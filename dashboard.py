import streamlit as st
import sqlite3
import pandas as pd

st.title("📊 ESP32 IoT Dashboard (Random Data)")

conn = sqlite3.connect("iot.db")
df = pd.read_sql("SELECT * FROM data ORDER BY id DESC LIMIT 20", conn)

if len(df) > 0:
    st.metric("🌡 Temperature (°C)", df.iloc[0]["temperature"])
    st.metric("💧 Humidity (%)", df.iloc[0]["humidity"])
    st.line_chart(df[["temperature", "humidity"]])
else:
    st.info("Waiting for ESP32 data...")
