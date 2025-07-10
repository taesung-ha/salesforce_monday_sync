# salesforce_api.py
import requests

ACCESS_TOKEN = "YOUR_SF_ACCESS_TOKEN"
INSTANCE_URL = "https://YOUR_INSTANCE.salesforce.com"  # 로그인 후 URL 확인
API_VERSION = "v59.0"

def send_to_salesforce(name, board_id):
    url = f"{INSTANCE_URL}/services/data/{API_VERSION}/sobjects/Lead"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "LastName": name,
        "Company": f"Board {board_id}"
    }
    res = requests.post(url, headers=headers, json=data)

    if res.status_code == 201:
        return "✅ Sent to Salesforce"
    else:
        return f"❌ Error: {res.text}"
