# config.py
#%%
import os
import urllib.parse as urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.getenv("DATABASE_URL"))

SF_LEAD_PARTNER_RECORDTYPE_ID = "0123p000000EILJAA4"

DB_CONFIG = {
    "dbname": url.path[1:],
    "user": url.username,
    "password": url.password,
    "host": url.hostname,
    "port": url.port,
}

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

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

CONNECTIONS = [
    {
        "name": "Opportunity → Account",
        "source_board": 9378000036,
        "target_board": 9378000326,
        "source_col": "text_mkryman1",  # OPPORTUNITY_ACCOUNT_ID_COL
        "target_col": "text_mkrykpx4",  # ACCOUNT_ID_COL
        "connect_col": "board_relation_mks9nfzc",  # OPPORTUNITY_CONNECT_COL_ID_ACCOUNT
    },
    {
        "name": "Opportunity → Contact",
        "source_board": 9378000036,
        "target_board": 9429890440,
        "source_col": "text_mkrya4jj",  # OPPORTUNITY_CONTACT_ID_COL
        "target_col": "text_mks6ner3",  # CONTACT_ID_COL
        "connect_col": "board_relation_mks9pr9d",  # OPPORTUNITY_CONNECT_COL_ID_CONTACT
    },
    {
        "name": "Lead → Account",
        "source_board": 9378000505,
        "target_board": 9378000326,
        "source_col": "text_mkryp43z",  # LEAD_ACCOUNT_ID_COL
        "target_col": "text_mkrykpx4",  # ACCOUNT_ID_COL
        "connect_col": "board_relation_mks9cjfs",  # LEAD_CONNECT_COL_ID_ACCOUNT
    },
    {
        "name": "Lead → Contact",
        "source_board": 9378000505,
        "target_board": 9429890440,
        "source_col": "text_mkry53df",  # LEAD_CONTACT_ID_COL
        "target_col": "text_mks6ner3",  # CONTACT_ID_COL
        "connect_col": "board_relation_mks95q",  # LEAD_CONNECT_COL_ID_CONTACT
    },
    {
        "name": "Lead → Opportunity",
        "source_board": 9378000505,
        "target_board": 9378000036,
        "source_col": "text_mkry581q",  # LEAD_OPPORTUNITY_ID_COL
        "target_col": "text_mkry20c9",  # OPPORTUNITY_ID_COL
        "connect_col": "board_relation_mksdqfg0",  # LEAD_CONNECT_COL_ID_OPPORTUNITY
    },
    {
        "name": "Contact → Account",
        "source_board": 9429890440,
        "target_board": 9378000326,
        "source_col": "text_mks61vvy",  # CONTACT_ACCOUNT_ID_COL
        "target_col": "text_mkrykpx4",  # ACCOUNT_ID_COL
        "connect_col": "board_relation_mks98dnn",  # CONTACT_CONNECT_COL_ID_ACCOUNT
    },
]

