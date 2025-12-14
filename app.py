
import streamlit as st
import pandas as pd

st.title("📊 Pandas with Streamlit - Beginner")

# Create DataFrame
data = {
    "Name": ["Kailash", "Ram", "Sita"],
    "Age": [21, 22, 20],
    "Branch": ["ECE", "EEE", "CSE"]
}

df = pd.DataFrame(data)

st.write("### Sample DataFrame")
st.dataframe(df)
st.write(df.head())
st.write(df.tail())
st.write("Rows & Columns:", df.shape)
st.write("Columns:", df.columns)






