# salesforce_api.py
import requests
from salesforce import get_salesforce_access_token
from config import SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD

ACCESS_TOKEN, INSTANCE_URL = get_salesforce_access_token(SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD)
API_VERSION = "v59.0"

def send_to_salesforce(name, board_id):
    url = f"{INSTANCE_URL}/services/data/{API_VERSION}/sobjects/Lead"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "Name": name,
        "Company": f"Board {board_id}"
    }
    res = requests.post(url, headers=headers, json=data)

    print("📡 Salesforce 응답:", res.status_code, res.text)

    if res.status_code == 201:
        return "✅ Sent to Salesforce"
    else:
        return f"❌ Error: {res.text}"
