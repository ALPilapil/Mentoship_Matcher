# app.py
import streamlit as st
import pandas as pd
import main

st.title("People Matcher")
st.write("For best use, have your uploaded csv contain only the following: name, role (ie. big/little), and information you want to match people on")
st.write("See below for more information")

# UI controls for labels, N, precision
name_col_label = st.text_input("Name column label", value="name (first, last)")
role_col_label = st.text_input("Role column label", value="I wanna be a...")
topN     = st.number_input("How many matches per person ", min_value=1, value=3, step=1)
precision = st.number_input("Decimal places for scores",        min_value=0, value=3, step=1)

# manual
if st.button("See manual"):
    manual = st.text_area(
        "How to use",
        "Upload a CSV file of the responses associated with responses from bigs and littles."
        "In the 'Name column label' box you will put the name of the column that contains the names of bigs and littles. "
        "In the 'Role column label' box you will put the name of the column that contains the role of each person, ie. big/little. "
        "note that 'both' is also an acceptable label and will not cause issues. "
        "How many matches simply means you will see that many top candidates per big. "
        "Decimal places for scores determine to what decimal place you see each score. "
    )

if st.button("Detalied use"):
    important = st.text_area(
        "For best use and how it works",
        "For best use upload a csv that contains ONLY each individual's name, role, and the columns which you"
        " deem important for matching people together based on their similarity. For example: you would want to exclude logistical "
        "questions such as phone number, student ID, instagram etc. This is because the program rates people better or worse based on "
        " how *similar* their responses to the same question are. So for example, if two people both responded to 'what's your favorite food?' "
        " with 'i love pizza' and 'pizza is my favorite' respectively, the program would rate them a good match. However, leaving unnecessary information "
        "such as student ID may sort students together based on that."
    )

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
        role_col_name=role_col_label,         
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
