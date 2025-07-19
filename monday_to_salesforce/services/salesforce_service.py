#salesforce_service.py
import requests
from config.config import SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD

API_VERSION = 'v59.0'

def get_salesforce_access_token(client_id, client_secret, username, password):
    import requests
    url = "https://login.salesforce.com/services/oauth2/token"
    data = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password
    }
    
    response = requests.post(url, data=data)
    if response.status_code != 200:
        raise Exception(f"Error getting access token: {response.text}")

    res = response.json()

    access_token = res['access_token']
    instance_url = res['instance_url']
    
    return access_token, instance_url

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