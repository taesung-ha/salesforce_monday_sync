# utils.py

import psycopg2
from psycopg2.extras import Json
from config import DB_CONFIG, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
import requests

def create_log_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS webhook_logs (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        event_type VARCHAR(50),
        board_id INTEGER,
        item_id INTEGER,
        column_id VARCHAR(50),
        status VARCHAR(50),
        message TEXT,
        request_payload JSONB,
        response_payload JSONB
    );
""")
    conn.commit()
    cur.close()
    conn.close()

def log_to_db(event_type, board_id, item_id, column_id, status, message=None, request_data=None, response_data=None):
    try: 
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO webhook_logs (event_type, board_id, item_id, column_id, status, message, request_payload, response_payload)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (event_type, board_id, item_id, column_id, status,
        message if message else '', Json(request_data), Json(response_data)))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Logging failed: {e}")

def send_telegram_alert(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram token or chat ID is not set.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)
    