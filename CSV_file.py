import streamlit as st
import pandas as pd

st.title("📂 CSV File Viewer")

file = st.file_uploader("Upload CSV file", type="csv")

if file:
    df = pd.read_csv(file)
    st.dataframe(df)
