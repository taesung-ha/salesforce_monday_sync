# config.py
#%%
import os

def get_envs():
    try:
        import streamlit as st  # ⬅️ 함수 안으로 이동

        # _secrets가 None일 수도 있으므로, 강제로 dict로 변환
        safe_secrets = dict(getattr(st.secrets, "_secrets", {}) or {})

        if all(k in safe_secrets for k in [
            "SF_CLIENT_ID", "SF_CLIENT_SECRET", "SF_USERNAME", "SF_PASSWORD", "MONDAY_TOKEN"
        ]):
            return {
                "SF_CLIENT_ID": st.secrets["SF_CLIENT_ID"],
                "SF_CLIENT_SECRET": st.secrets["SF_CLIENT_SECRET"],
                "SF_USERNAME": st.secrets["SF_USERNAME"],
                "SF_PASSWORD": st.secrets["SF_PASSWORD"],
                "MONDAY_TOKEN": st.secrets["MONDAY_TOKEN"]
            }
    except Exception:
        pass

    try:
        from dotenv import load_dotenv  # ⬅️ 여기만 수정
        load_dotenv()
    except Exception:
        pass

    return {
        "SF_CLIENT_ID": os.getenv("SF_CLIENT_ID"),
        "SF_CLIENT_SECRET": os.getenv("SF_CLIENT_SECRET"),
        "SF_USERNAME": os.getenv("SF_USERNAME"),
        "SF_PASSWORD": os.getenv("SF_PASSWORD"),
        "MONDAY_TOKEN": os.getenv("MONDAY_TOKEN")
    }


# 아래 부분 유지 – 기존 구조 유지
env = get_envs()
SF_CLIENT_ID = env["SF_CLIENT_ID"]
SF_CLIENT_SECRET = env["SF_CLIENT_SECRET"]
SF_USERNAME = env["SF_USERNAME"]
SF_PASSWORD = env["SF_PASSWORD"]
MONDAY_TOKEN = env["MONDAY_TOKEN"]

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