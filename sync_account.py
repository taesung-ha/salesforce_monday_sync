import json
from collections import defaultdict
from config import SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD, MONDAY_TOKEN
from salesforce import get_salesforce_access_token
from monday import get_monday_items, create_or_update_monday_item
from sync_utils import get_last_sync_time


def load_account_config(path="mapping_config/account.json"):
    with open(path, "r") as f:
        return json.load(f)


def chunked(iterable, size=1000):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]


def get_id_set_for_account(instance_url, access_token, last_sync):
    import requests
    query_url = f"{instance_url}/services/data/v58.0/query"
    headers = {"Authorization": f"Bearer {access_token}"}
    id_dict = defaultdict(list)

    # 1. Opportunity
    query = f'''
    SELECT AccountId, ContactId, LastModifiedDate
    FROM Opportunity
    WHERE RecordTypeId = '0123p000000EILEAA4'
    '''
    
    if last_sync:
        query += f" AND LastModifiedDate >= {last_sync}"
    
    res = requests.get(query_url, headers=headers, params={"q": query})
    
    if res.status_code != 200:
        print(f"❌ Failed to query Opportunity: {res.status_code} - {res.text}")
        return set()
    for record in res.json().get('records', []):
        id_dict['bizdev_AccountId'].append(record['AccountId'])
        id_dict['bizdev_ContactId'].append(record['ContactId'])

    # 2. Lead
    query = f'''
    SELECT ConvertedAccountId, ConvertedContactId, LastModifiedDate
    FROM Lead
    WHERE Role__c = 'Partner' AND CreatedDate >= 2024-07-01T00:00:00Z
    '''
    
    if last_sync:
        query += f" AND LastModifiedDate >= {last_sync}"
    
    res = requests.get(query_url, headers=headers, params={"q": query})
    if res.status_code != 200:
        print(f"❌ Failed to query Lead: {res.status_code} - {res.text}")
        return set()
    for record in res.json().get('records', []):
        id_dict['bizdev_AccountId'].append(record['ConvertedAccountId'])
        id_dict['bizdev_ContactId'].append(record['ConvertedContactId'])

    # 3. Contact → Account
    bizdev_contact_ids = [cid for cid in id_dict['bizdev_ContactId'] if cid]
    if bizdev_contact_ids:
        for chunk in chunked(bizdev_contact_ids):
            soql_ids = '(' + ', '.join(f"'{cid}'" for cid in chunk) + ')'
            query = f'''
            SELECT AccountId
            FROM Contact
            WHERE Id IN {soql_ids}
            '''
            if last_sync:
                query += f" AND LastModifiedDate >= {last_sync}"
            
            res = requests.get(query_url, headers=headers, params={"q": query})
            if res.status_code != 200:
                print(f"❌ Failed to query Contact: {res.status_code} - {res.text}")
                continue
            for record in res.json().get('records', []):
                id_dict['bizdev_AccountId'].append(record['AccountId'])

    return set(filter(None, id_dict['bizdev_AccountId']))


def sync_account_records():
    import requests
    config = load_account_config()
    monday_board_id = config["board_id"]
    salesforce_column_id = config["salesforce_id_column_id"]
    selected_fields = config["salesforce_select_fields"]
    field_mapping = config["field_mapping"]

    if isinstance(selected_fields, list):
        selected_fields = ", ".join(selected_fields)

    access_token, instance_url = get_salesforce_access_token(
        SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD)
    if not access_token:
        print("❌ Failed to authenticate with Salesforce.")
        return

    print("🔑 Salesforce authenticated.")

    # 🔁 Get last sync time
    last_sync = get_last_sync_time()
    print(f"⏱️ Last sync time: {last_sync}")

    # 🧾 Filter by modified date
    account_ids = get_id_set_for_account(instance_url, access_token, last_sync)
    if not account_ids:
        print("📭 No Account IDs found.")
        return

    print(f"🔍 Retrieved {len(account_ids)} Account IDs")

    records = []
    query_url = f"{instance_url}/services/data/v58.0/query"
    headers = {"Authorization": f"Bearer {access_token}"}

    for chunk in chunked(list(account_ids)):
        soql_ids = ', '.join(f"'{aid}'" for aid in chunk)
        query = f"""
        SELECT {selected_fields}
        FROM Account
        WHERE Id IN ({soql_ids})
        """
        if last_sync:
            query += f" AND LastModifiedDate >= {last_sync}"
        res = requests.get(query_url, headers=headers, params={"q": query})
        if res.status_code != 200:
            print(f"❌ Failed to query Account: {res.status_code} - {res.text}")
            continue
        records.extend(res.json().get('records', []))

    if not records:
        print("📭 No Account records found.")
        return

    monday_items = get_monday_items(monday_board_id, MONDAY_TOKEN, salesforce_column_id)
    for record in records:
        create_or_update_monday_item(record, monday_items, monday_board_id, MONDAY_TOKEN, field_mapping)

    print(f"✅ Synced {len(records)} Account records to Monday.com.", flush=True)


if __name__ == "__main__":
    sync_account_records()
