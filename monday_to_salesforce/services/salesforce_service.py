#salesforce_service.py
import requests
import json
from config import SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD
from salesforce import get_salesforce_access_token

API_VERSION = 'v59.0'

def update_salesforce_record(object_name: str, record_id: str, fields: dict):
    ACCESS_TOKEN, INSTANCE_URL = get_salesforce_access_token(
        SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD
    )
    url = f"{INSTANCE_URL}/services/data/{API_VERSION}/sobjects/{object_name}/{record_id}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    response = requests.patch(url, headers=headers, json=fields)
    return response.status_code == 204

def create_salesforce_record(object_name: str, fields: dict):
    ACCESS_TOKEN, INSTANCE_URL = get_salesforce_access_token(
        SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD
    )
    url = f"{INSTANCE_URL}/services/data/{API_VERSION}/sobjects/{object_name}/"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=fields)
    if response.status_code == 201:
        return response.json().get("id")
    return None