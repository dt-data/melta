import json
import datetime
import pandas as pd
import streamlit as st

with open('data/melta_table.json', 'r') as f:
    data = json.load(f)

last_item = data[-1]
values_dict = last_item.get("values", {})

df = pd.DataFrame([values_dict])
df_long = df.melt(ignore_index=True, var_name='Field', value_name='Description')

st.title("Melta Editor")

edited_df = st.data_editor(df_long, num_rows="dynamic")

st.write("""
## Edited Data
Here is the result of your edits:
""")
st.dataframe(edited_df)

if st.button("Submit"):
    updated_values = dict(zip(edited_df["Field"], edited_df["Description"]))
    new_item = {
        "melta_datetime": datetime.datetime.now().isoformat(),
        "values": updated_values
    }
    data.append(new_item)
    with open('data/melta_table.json', 'w') as f:
        json.dump(data, f, indent=2)
    st.success("Added a new item to the JSON!")
