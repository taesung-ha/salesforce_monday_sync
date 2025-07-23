# mapping_service.py
import psycopg2
from config.config import DB_CONFIG

def create_mapping_table():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS item_sf_mapping (
        item_id VARCHAR(50),
        board_id VARCHAR(50) NOT NULL,
        sf_id VARCHAR(50) NOT NULL,
        entity_type VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (item_id, board_id)
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_mapping(item_id, board_id, sf_id, entity_type):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO item_sf_mapping (item_id, board_id, sf_id, entity_type)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (item_id, board_id) DO UPDATE SET sf_id = EXCLUDED.sf_id;
    """, (item_id, board_id, sf_id, entity_type))
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Mapping saved: {item_id} -> {sf_id} for board {board_id}")

def get_sf_id(item_id, board_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("SELECT sf_id FROM item_sf_mapping WHERE item_id = %s AND board_id = %s;", (str(item_id), str(board_id)))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None

def delete_mapping(item_id, board_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
    DELETE FROM item_sf_mapping WHERE item_id = %s AND board_id = %s;
    """, (str(item_id), str(board_id)))
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Mapping deleted: {item_id} for board {board_id}")