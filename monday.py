import requests, json

MONDAY_API_URL = "https://api.monday.com/v2"

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
            "https://api.monday.com/v2",
            headers={"Authorization": monday_token},
            json={"query": query, "variables": variables}
        )
        
        print("Rate Limit Remaining:", response.headers.get('X-RateLimit-Remaining', 'No Rate Limit Info'))
        print("Total Rate Limit:", response.headers.get("x-ratelimit-limit"))
        
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

def create_or_update_monday_item(record, monday_items, monday_board_id, monday_token, field_mapping):
    salesforce_id = record.get("Id")
    if not salesforce_id:
        return

    item_name = record.get('Name') or f"{record.get('FirstName', '')} {record.get('LastName', '')}".strip()
    
    column_values = {
        column_id: str(record.get(sf_field, ""))
        for column_id, sf_field in field_mapping.items()
    }

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
            "https://api.monday.com/v2",
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
                "https://api.monday.com/v2",
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
            
    print("Rate Limit Remaining:", r.headers.get('X-RateLimit-Remaining', 'No Rate Limit Info'))
    print("Total Rate Limit:", r.headers.get("x-ratelimit-limit"))