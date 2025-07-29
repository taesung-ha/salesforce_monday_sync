import json

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

def fetch_salesforce_records(instance_url, access_token, object_name, select_fields, conditions = None, from_datetime=None):
    import requests
    query = f"SELECT {select_fields} FROM {object_name}"

    where_clauses = []
    if conditions:
        where_clauses.append(conditions)

    if from_datetime:
        where_clauses.append(f"LastModifiedDate >= {from_datetime}")

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    print(f"🔍 Salesforce Query: {query}")

    params = {"q": query}
    records = []
    query_url = f"{instance_url}/services/data/v58.0/query"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(query_url, headers=headers, params=params)

    if response.status_code != 200:
        try:
            error_json = response.json()
            print("🔴 Salesforce API Error Details:")
            print(json.dumps(error_json, indent=2))
        except Exception:
            print("🔴 Raw error response:")
            print(response.text)
        raise Exception(f"[{response.status_code}] Failed initial fetch.")

    result = response.json()
    records.extend(result['records'])
 
    while not result.get('done', True):
        next_url = f"{instance_url}{result['nextRecordsUrl']}" 
        response = requests.get(next_url, headers=headers)
        result = response.json()
        records.extend(result['records'])

    return records