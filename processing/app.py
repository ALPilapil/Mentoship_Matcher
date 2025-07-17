# super simple front end
# save as app.py
import streamlit as st
import pandas as pd

def match_people(df):
    # your matching logic, return a DataFrame
    # for demo, we'll just echo the input
    return df

st.title("People Matcher")

uploaded = st.file_uploader("Upload responses CSV", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
    result = match_people(df)
    st.dataframe(result)                         # preview
    csv = result.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download matches CSV",
        data=csv,
        file_name="matches.csv",
        mime="text/csv",
    )
