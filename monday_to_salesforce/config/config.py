# config.py
#%%
import os
import urllib.parse as urlparse

def load_env():
    try:
        # Streamlit 환경 (Streamlit에서만 실행되는 경우)
        import streamlit as st
        if hasattr(st, "secrets") and "SF_CLIENT_ID" in st.secrets:
            SF_CLIENT_ID = st.secrets["SF_CLIENT_ID"]
            SF_CLIENT_SECRET = st.secrets["SF_CLIENT_SECRET"]
            SF_USERNAME = st.secrets["SF_USERNAME"]
            SF_PASSWORD = st.secrets["SF_PASSWORD"]
            MONDAY_TOKEN = st.secrets["MONDAY_TOKEN"]
            return SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD, MONDAY_TOKEN
    except Exception:
        pass

    # 로컬 개발 or Render 배포 환경
    from dotenv import load_dotenv
    load_dotenv()

    SF_CLIENT_ID = os.getenv("SF_CLIENT_ID")
    SF_CLIENT_SECRET = os.getenv("SF_CLIENT_SECRET")
    SF_USERNAME = os.getenv("SF_USERNAME")
    SF_PASSWORD = os.getenv("SF_PASSWORD")
    MONDAY_TOKEN = os.getenv("MONDAY_TOKEN")

    return SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD, MONDAY_TOKEN


SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD, MONDAY_TOKEN = load_env()

API_URL = "https://api.monday.com/v2"
HEADERS = {
    "Authorization": MONDAY_TOKEN,
    "Content-Type": "application/json"
}

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.getenv("DATABASE_URL"))

DB_CONFIG = {
    "dbname": url.path[1:],
    "user": url.username,
    "password": url.password,
    "host": url.hostname,
    "port": url.port,
}

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")