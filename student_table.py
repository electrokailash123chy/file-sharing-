import streamlit as st
import pandas as pd
st.title("Student Information Table")
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [23, 22, 24],
    "Major": ["Physics", "Mathematics", "Computer Science"]
}
st.write("### Student DataFrame")
pd.DataFrame(data)