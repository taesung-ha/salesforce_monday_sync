# config.py
#%%
from dotenv import load_dotenv
import os

load_dotenv()

SF_CLIENT_ID = os.getenv("SF_CLIENT_ID")
SF_CLIENT_SECRET = os.getenv("SF_CLIENT_SECRET")
SF_USERNAME = os.getenv("SF_USERNAME")
SF_PASSWORD = os.getenv("SF_PASSWORD")
SF_SELECT_FIELDS = os.getenv("SF_SELECT_FIELDS")

MONDAY_TOKEN = os.getenv("MONDAY_TOKEN")
MONDAY_BOARD_ID = os.getenv("MONDAY_BOARD_ID")
# %%
