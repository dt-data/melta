import json
import os
import datetime
import requests
import pandas as pd
import streamlit as st

# BIN_ID = st.secrets["JSON_BIN_ID"]
BIN_ID = "679a08ede41b4d34e4809a03"

# SECRET_KEY = st.secrets["JSON_BIN_SECRET"]
SECRET_KEY = "$2a$10$c00.38k9KVzPX5hxOezV4.rLYbG6n.w8Z7HklWFrS8Tbzl1TCrQ.6"

BASE_URL = "https://api.jsonbin.io/v3/b"
HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": SECRET_KEY
}

st.set_page_config(layout="wide")

def fetch_data():
    url = f"{BASE_URL}/{BIN_ID}/latest"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        return resp.json()["record"]
    else:
        st.error(f"Failed to load data: {resp.status_code}, {resp.text}")
        st.stop()

def update_data(new_data):
    url = f"{BASE_URL}/{BIN_ID}"
    payload = json.dumps(new_data)
    resp = requests.put(url, headers=HEADERS, data=payload)
    if resp.status_code == 200:
        st.success("Updated data on JSONBin!")
    else:
        st.error(f"Failed to update data: {resp.status_code}, {resp.text}")

data = fetch_data()

table_names = [item["table_name"] for item in data]
selected_table_name = st.sidebar.selectbox("Select a Table", table_names)

table_data = next((t for t in data if t["table_name"] == selected_table_name), None)

if not table_data:
    st.error("No table found.")
    st.stop()

rows = table_data.get("data", [])

if len(rows) == 0:
    st.warning("No rows for this table.")
    st.stop()

last_item = rows[-1]
columns_dict = last_item.get("columns", {})

st.title("Melta Editor")
st.subheader(f"Table: {selected_table_name}")

table_description = last_item.get("table_description", "")

desc_input = st.text_input("Table Description", value=table_description)

df = pd.DataFrame([columns_dict])
df_long = df.melt(ignore_index=True, var_name="Field", value_name="Description")
edited_df = st.data_editor(df_long, num_rows="dynamic", use_container_width=True)

if st.button("Submit"):
    updated_values = dict(zip(edited_df["Field"], edited_df["Description"]))
    new_item = {
        "melta_datetime": datetime.datetime.now().isoformat(),
        "table_description": desc_input,
        "columns": updated_values
    }
    rows.append(new_item)
    update_data(data)
