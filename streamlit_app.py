import json
import datetime
import requests
import pandas as pd
import streamlit as st

BIN_ID = "6799ff90e41b4d34e4809426"
SECRET_KEY = "$2a$10$SQgyOb5fT/7eNJDfHeGvkuDOqn4j.l41IYD6rvVngsOkvdj24mm1e"
BASE_URL = "https://api.jsonbin.io/v3/b"
HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": SECRET_KEY
}

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

if len(data) == 0:
    data = [
        {
            "datetime": None,
            "values": {
                "id": None,
                "name": None,
                "description": None,
                "created_at": None
            }
        }
    ]

last_item = data[-1]
values_dict = last_item.get("values", {})

df = pd.DataFrame([values_dict])
df_long = df.melt(ignore_index=True, var_name="Field", value_name="Description")

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
    update_data(data)
