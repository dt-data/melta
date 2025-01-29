import pandas as pd
import streamlit as st
import json

with open('data/original.json', 'r') as f:
    data = json.load(f)

df = pd.json_normalize(data)
df = df.astype(str)

st.title("Local JSON Data in Streamlit")
df_long = df.melt(ignore_index=False, var_name='Field', value_name='Description')

st.subheader("Editable Data Editor")
edited_df = st.data_editor(df_long, num_rows="dynamic")