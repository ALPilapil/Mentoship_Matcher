# app.py
import streamlit as st
import pandas as pd
import main

st.title("People Matcher")

# UI controls for labels, N, precision
name_col_label = st.text_input("Name column label", value="name (first, last)")
role_col_label = st.text_input("Role column label", value="I wanna be a...")
topN     = st.number_input("How many matches per person (top N)", min_value=1, value=3, step=1)
precision = st.number_input("Decimal places for scores",        min_value=0, value=3, step=1)

uploaded = st.file_uploader("Upload responses CSV", type="csv")
if not uploaded:
    st.info("Please upload a CSV to continue.")
    st.stop()

df = pd.read_csv(uploaded)

# 1️ figure out which columns need weights
feature_cols = [c for c in df.columns
                if c not in (name_col_label, role_col_label)]

st.subheader("Set feature weights")
weights = {}
for col in feature_cols:
    # you can tune min, max, step to your needs
    weights[col] = st.number_input(f"Weight for '{col}'",
                                   min_value=0.0,
                                   value=1.0,
                                   step=0.1)
    
weights_array = weights.values()
    

# 2️ run your matching logic, passing those weights in
if st.button("press to run calculation"):
    st.write("This may take a bit")
    detailed_df, base_df = main.main(
        df,
        topN=topN,
        precision=precision,
        weights=weights_array,         
    )

    st.subheader("Detailed Matches")
    st.dataframe(detailed_df)

    detailed_csv = detailed_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download detailed matches CSV",
        key=1,
        data=detailed_csv,
        file_name="matches_base.csv",
        mime="text/csv",
    )

    st.subheader("Base Matches")
    st.dataframe(base_df)

    base_csv = base_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download base matches CSV",
        key=2,
        data=base_csv,
        file_name="matches_base.csv",
        mime="text/csv",
    )
