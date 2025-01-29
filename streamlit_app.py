import streamlit as st
import pandas as pd

st.title("Melta")
st.header("Meta Data Management")

# This script demonstrates how to load data from a local JSON file and display it in Streamlit's data editor.
#
# Prerequisites:
#     - Make sure you have Streamlit installed (pip install streamlit).
#
# Usage:
#     1. Place your JSON file at 'data/original.json'.
#     2. Run 'streamlit run public_google_sheet_import.py' from the terminal.

import pandas as pd
import streamlit as st
import json

# Load data from the local JSON file
with open('data/original.json', 'r') as f:
    data = json.load(f)

# Convert the loaded JSON (a dict) to a DataFrame
df = pd.json_normalize(data)

# Convert all columns to string type if desired
df = df.astype(str)

# Streamlit App
st.title("Local JSON Data in Streamlit")

st.subheader("Original Data")
st.dataframe(df)

st.subheader("Editable Data Editor")
# The data_editor allows editing rows and columns in real time
edited_df = st.data_editor(df, num_rows="dynamic")

st.write("""
## Edited Data
Here is the result of your edits:
""")
st.dataframe(edited_df)


