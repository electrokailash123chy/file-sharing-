import streamlit as st
import pandas as pd
st.title("🌡️ IoT Sensor Data")
df=pd.DataFrame({
    "Time":["10:00","10:05","10:10"],
    "Temperature":[28,29,30]})
st.line_chart (df.set_index("Time"))
