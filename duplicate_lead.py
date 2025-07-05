#%%
import requests, json
import os
import json
from config import (
    SF_CLIENT_ID,
    SF_CLIENT_SECRET,
    SF_USERNAME,
    SF_PASSWORD,
    MONDAY_TOKEN
)
#%%

monday_board_id = "9501303800" #duplicate_lead board ID
salesforce_column_id = "text_mkryhch5"
salesforce_select_fields = "Id, LastName, Website, FirstName, ConvertedAccountId, ConvertedContactId, RecordTypeId, ConvertedOpportunityId, CreatedDate, LastModifiedDate, Company, Street, City, State, PostalCode, Country, StateCode, CountryCode, Address, Phone, MobilePhone, Email, Description, Status, OwnerId, IsConverted, CreatedById, LastModifiedById, Role__c, Record_Type_ID_Text__c, LeadSource"
salesforce_object = "Lead"
salesforce_condition = "Role__c = 'Partner' AND CreatedDate >= 2024-07-01T00:00:00Z"
field_mapping = {
        "text_mkryhch5": {"field": "Id", "type": "text"},
        "text_mkry1xy1": {"field": "LastName", "type": "text"},
        "text_mkry13cw": {"field": "FirstName", "type": "text"},
        "text_mks821t": {"field": "Website", "type": "text"},
        "text_mkryp43z": {"field": "ConvertedAccountId", "type": "text"},
        "text_mkry427s": {"field": "RecordTypeId", "type": "text"},
        "text_mkry53df": {"field": "ConvertedContactId", "type": "text"},
        "text_mkry581q": {"field": "ConvertedOpportunityId", "type": "text"},
        "text_mkryzhzt": {"field": "CreatedDate", "type": "datetime"},
        "text_mkryr3pj": {"field": "LastModifiedDate", "type": "datetime"},
        "text_mkrykrc2": {"field": "Company", "type": "text"},
        "text_mkryq1r8": {"field": "Street", "type": "text"},
        "text_mkrym6fa": {"field": "City", "type": "text"},
        "text_mkryz0sr": {"field": "State", "type": "text"},
        "text_mkryrr5y": {"field": "PostalCode", "type": "text"},
        "text_mkrym3j7": {"field": "Country", "type": "text"},
        "text_mkryamt0": {"field": "StateCode", "type": "text"},
        "text_mkrye90n": {"field": "CountryCode", "type": "text"},
        "text_mkry40xt": {"field": "Address", "type": "text"},
        "text_mkryhzq7": {"field": "Phone", "type": "text"},
        "text_mkryhpf0": {"field": "MobilePhone", "type": "text"},
        "text_mkrymwp3": {"field": "Email", "type": "text"},
        "long_text_mkshtq2k": {"field": "Description", "type": "long_text"},
        "color_mksfe7m5": {"field": "Status", "type": "color"},
        "text_mkryxqtf": {"field": "IsConverted", "type": "text"},
        "text_mkryf4cd": {"field": "Role__c", "type": "text"},
        "text_mkrycwgc": {"field": "LeadSource", "type": "text"}
    }
#%%
MONDAY_API_URL = "https://api.monday.com/v2"


def get_salesforce_access_token(client_id, client_secret, username, password):
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
 
    while not result.get('done', True): #만약 result.get('done', True)가 False를 반환하면, not False가 되므로 while True가 되어 걔속 반복됨. 
        next_url = f"{instance_url}{result['nextRecordsUrl']}" #그런데, 만약 result.get('done',True)가 True를 반환하면, not True가 되므로 while False, 즉 반복문이 종료됨
        response = requests.get(next_url, headers=headers)
        result = response.json()
        records.extend(result['records'])

    return records

def get_monday_items(monday_board_id, monday_token, salesforce_id_column_id):
    monday_items = {}
    cursor = None

    while True:
        query = '''
            query ($boardId: ID!, $cursor: String) {
            boards(ids: [$boardId]) {
                items_page(limit: 100, cursor: $cursor) {
                    cursor
                    items {
                        id
                        column_values {
                            id
                            text
                        }
                    }
                }
            }
        }
        '''

        variables = {"boardId": monday_board_id, "cursor": cursor}
        response = requests.post(
            MONDAY_API_URL,
            headers={"Authorization": monday_token},
            json={"query": query, "variables": variables}
        )


        result = response.json()


        if "errors" in result:
            print("❌ GraphQL error:", json.dumps(result["errors"], indent=2))
            break

        items_data = result['data']['boards'][0]['items_page']
        items = items_data['items']
        for item in items:
            cols = {cv['id']: cv.get('text', '') for cv in item['column_values']}
            lead_id = cols.get(salesforce_id_column_id) #Salesforce ID column ID in monday.com
            if lead_id:
                monday_items[lead_id] = {
                    "item_id": item['id'],
                    "column_values": cols
                }

        # 다음 페이지로 이동
        cursor = items_data.get('cursor')
        if not cursor:
            break

    return monday_items

def format_value(value, col_type):
    if not value:
        return None  # 빈 값은 None으로 처리

    if col_type in ["text", "long-text"]:
        return str(value)

    elif col_type == "date":
        return {"date": value[:10]}  # ISO YYYY-MM-DD

    elif col_type == "status":
        return {"label": str(value)}

    elif col_type == "phone":
        return {"phone": str(value), "countryShortName": "US"}

    elif col_type == "email":
        return {"email": str(value), "text": str(value)}

    elif col_type == "link":
        return {"url": str(value), "text": str(value)}

    return str(value)

def create_or_update_monday_item(record, monday_items, monday_board_id, monday_token, field_mapping):
    salesforce_id = record.get("Id")
    if not salesforce_id:
        return

    item_name = record.get('Name') or f"{record.get('FirstName', '')} {record.get('LastName', '')}".strip()

    column_values = {}
    for column_id, map_info in field_mapping.items():
        sf_field = map_info["field"]
        col_type = map_info.get("type", "text")  # 기본값은 text
        value = record.get(sf_field)
        column_values[column_id] = format_value(value, col_type)

    cleaned = {k: str(v) if v else "" for k, v in column_values.items()}

    # create new item
    if salesforce_id not in monday_items:
        query = '''
        mutation ($boardId: ID!, $itemName: String!, $columnValues: JSON!) {
                create_item (board_id: $boardId, item_name: $itemName, column_values: $columnValues) {
                    id
            }
        }
        '''
        variables = {
            "boardId": monday_board_id,
            "itemName": item_name,
            "columnValues": json.dumps(cleaned)
        }
        r = requests.post(
            MONDAY_API_URL,
            headers={"Authorization": monday_token},
            json={"query": query, "variables": variables}
        )

        try:
            response = r.json()
            if "errors" in response:
                print(f"❌ Failed to create item: {item_name}\nReason: {response['errors'][0]['message']}")

            else:
                print(f"✅ Created: {item_name}")
                print(f"📎 Created Item ID: {response['data']['create_item']['id']}")

        except ValueError:
            print(f"❌ Json parsing failure (abnormal response):")
            print(r.text)
        except Exception as e:
            print(f"❌ Exception occurred: {e}")
    
    else: 
        # update existing item
        current = monday_items[salesforce_id]['column_values']
        updated = {}
        for k in cleaned:
            if cleaned[k] != current.get(k, ""):
                updated[k] = cleaned[k]
        if updated:
            updated = {k: str(v) for k, v in updated.items() if v}
            query = '''
            mutation ($itemId: ID!, $boardId: ID!, $columnValues: JSON!) {
                change_multiple_column_values(item_id: $itemId, board_id: $boardId, column_values: $columnValues) {
                    id
                }
            }
            '''
            variables = {
                "itemId": str(monday_items[salesforce_id]['item_id']),
                "boardId": str(monday_board_id),
                "columnValues": json.dumps(updated)
            }
            r = requests.post(
                MONDAY_API_URL,
                headers={"Authorization": monday_token},
                json={"query": query, "variables": variables}
            )
            if 'errors' in r.json():
                print("❌ GraphQL error occurred:")
                for err in r.json()['errors']:
                    print(f"  - {err['message']}")
                    if "locations" in err:
                        print(f"  location: {err['locations']}")
                    if "extensions" in err:
                        print(f"  code: {err['extensions'].get('code')}")
            else:
                print(f"🔁 Updated: {item_name}")
        else:
            print(f"⏩ Skipped (no change): {item_name}")




# %%
access_token, instance_url = get_salesforce_access_token(
    SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD)
records = fetch_salesforce_records(
    instance_url=instance_url, 
    access_token=access_token, 
    object_name=salesforce_object, 
    select_fields=salesforce_select_fields, 
    conditions=salesforce_condition
)
# %%
records[:5]
# %%
monday_items = get_monday_items(monday_board_id, MONDAY_TOKEN, salesforce_column_id)
monday_items
# %%
item_id = "9501436444"
status_column_id = "color_mksfe7m5"
label = "Qualified"

column_values = {status_column_id: format_value(label, "status")}

query = '''
mutation ($itemId: ID!, $boardId: ID!, $columnValues: JSON!) {
  change_multiple_column_values(item_id: $itemId, board_id: $boardId, column_values: $columnValues) {
    id
  }
}
'''

variables = {
    "itemId": item_id,
    "boardId": monday_board_id,
    "columnValues": json.dumps(column_values)
}

# API 요청
response = requests.post(
    MONDAY_API_URL,
    headers={"Authorization": MONDAY_TOKEN},
    json={"query": query, "variables": variables}
)

# 결과 출력
print("✅ Response:")
print(json.dumps(response.json(), indent=2))
# %%
print(format_value("Qualified", "status"))
# %%
\