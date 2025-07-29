import json
import os
from datetime import datetime, timedelta, timezone

sync_file = 'last_sync_time.txt'

def get_last_sync_time():
    if not os.path.exists(sync_file):
        print("No previous sync time found. Defaulting to 10000 days ago.")
        return (datetime.now(timezone.utc) - timedelta(days=10000)).isoformat()
    
    try:
        with open(sync_file, 'r') as f:
            data = json.load(f)
            return data.get('last_sync_time')
        
    except Exception as e:
        print(f"Error reading last sync time: {e}")
        return (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    
def save_sync_time():
    now = datetime.now(timezone.utc).isoformat()
    
    try:
        with open(sync_file, 'w') as f:
            json.dump({"last_sync_time": now}, f)
    except Exception as e:
        print(f'Error saving sync time: {e}')
        return