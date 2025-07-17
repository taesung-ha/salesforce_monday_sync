#log_service.py 
import psycopg2
from psycopg2.extras import Json
from config import DB_CONFIG, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
import requests

def create_log_table():
    """
    Create the webhook_logs table if it does not exist.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS webhook_logs (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            event_type VARCHAR(50),
            board_id VARCHAR(50),
            item_id VARCHAR(50),
            column_id VARCHAR(50),
            status VARCHAR(50),
            request_payload JSONB,
            response_payload JSONB
        );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Log table created or already exists.")
    except Exception as e:
        print(f"❌ Error creating log table: {str(e)}")

def log_to_db(event_type, board_id, item_id, column_id, status, message=None, request_data=None, response_data=None):
    """
    Insert a log entry into the webhook_logs table.
    """
    try: 
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO webhook_logs (event_type, board_id, item_id, column_id, status, request_payload, response_payload)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (event_type, board_id, item_id, column_id, status,
        Json(request_data), Json(response_data)))
        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Log inserted for event: {event_type}, item: {item_id}")
    except Exception as e:
        print(f"❌ Logging failed: {str(e)}")

def send_telegram_alert(message):
    """
    Send a message to a Telegram chat using the bot API.
    """
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram token or chat ID is not set.")
        return
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Telegram alert sent successfully.")
        else:
            print(f"❌ Failed to send Telegram alert: {response.text}")

    except Exception as e:
        print(f"❌ Error sending Telegram alert: {str(e)}")
    