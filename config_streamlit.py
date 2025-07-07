import streamlit as st

SF_CLIENT_ID = st.secrets["SF_CLIENT_ID"]
SF_CLIENT_SECRET = st.secrets["SF_CLIENT_SECRET"]
SF_USERNAME = st.secrets["SF_USERNAME"]
SF_PASSWORD = st.secrets["SF_PASSWORD"]
MONDAY_TOKEN = st.secrets["MONDAY_TOKEN"]

API_URL = "https://api.monday.com/v2"
HEADERS = {
    "Authorization": MONDAY_TOKEN,
    "Content-Type": "application/json"
}