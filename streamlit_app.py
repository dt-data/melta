import streamlit as st
import pandas as pd

st.title("Melta")
st.header("Meta Data Management")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)


url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSKhCMTNxdjJiRx19g1p4TCyGEirJcgdJ_YKkNYl5U_DuCNtyIRYiidIeaHOux5ekZbOvRblqpiXVic/pub?gid=0&single=true&output=csv'
df = pd.read_csv(url, dtype=str)

# The data_editor allows editing rows and columns in real time
edited_df = st.data_editor(df, num_rows="dynamic")

st.write("\n## Edited Data\nHere is the result of your edits:")
st.dataframe(edited_df)

