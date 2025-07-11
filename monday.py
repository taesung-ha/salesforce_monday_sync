import json

MONDAY_API_URL = "https://api.monday.com/v2"

def get_monday_items(monday_board_id, monday_token, salesforce_id_column_id):
    import requests
    monday_items = {}
    cursor = None

    while True:
        query = """
        query ($boardId: ID!, $cursor: String) {
            boards(ids: [$boardId]) {
                items_page(limit: 100, cursor: $cursor) {
                    cursor
                    items {
                        id
                        column_values {
                            id
                            text
                            value
                            type
                        }
                    }
                }
            }
        }
        """

        variables = {"boardId": monday_board_id, "cursor": cursor}
        response = requests.post(
            MONDAY_API_URL,
            headers={"Authorization": monday_token},
            json={"query": query, "variables": variables}
        )

        result = response.json()
        if "errors" in result:
            print("❌ GraphQL error:", json.dumps(result["errors"], indent=2), flush=True)
            break

        items_data = result['data']['boards'][0]['items_page']
        items = items_data['items']

        for item in items:
            column_dict = {}
            for cv in item['column_values']:
                col_id = cv['id']
                col_type = cv['type']
                text = cv.get('text', '')
                value = cv.get('value')
                parsed_value = None
                
                if col_type == 'status' and value:
                    # 예: {"index": 0, "post_id": null, "changed_at": "..."}
                    value = json.loads(value)
                    parsed_value = {"label": text, "index": value.get("index")}

                elif col_type == 'date' and value:
                    value = json.loads(value)
                    parsed_value = {"date": value.get("date")}

                elif col_type == 'people' and value:
                    value = json.loads(value)
                    parsed_value = {"personsAndTeams": value.get("personsAndTeams", [])}

                elif col_type == 'numbers' and text:
                    try:
                        parsed_value = float(text)
                    except:
                        parsed_value = None

                elif col_type == 'long-text' and value:
                    value = json.loads(value)
                    parsed_value = value.get("text", "")

                elif col_type == 'dropdown' and value:
                    # 예: {"ids":[...],"labels":["Option A", "Option B"]}
                    value = json.loads(value)
                    parsed_value = {"labels": value.get("labels", [])}

                else:
                    parsed_value = text  # fallback: use plain text

                column_dict[col_id] = {
                    "type": col_type,
                    "value": parsed_value
                }
    
            salesforce_entry = column_dict.get(salesforce_id_column_id)
            if salesforce_entry:
                salesforce_id = salesforce_entry.get("value")
                if salesforce_id:
                    monday_items[salesforce_id] = {
                        "item_id": item['id'],
                        "column_values": column_dict
                    }

        cursor = items_data.get('cursor')
        if not cursor:
            break

    return monday_items

def format_value_for_column(value, col_type):
    if col_type == 'status':
        return {"label": value}
    elif col_type == 'date':
        return {"date": value}
    elif col_type == 'people':
        try:
            return {"personsAndTeams": [{"id": int(value), "kind": "person"}]}
        except:
            return {}
    elif col_type == 'dropdown':
        if isinstance(value, list):
            return {"labels": value}
        elif isinstance(value, str):
            return {"labels": [value]}
        else:
            return {}
    elif col_type == 'long-text':
        return {"text": value}
    elif col_type == 'numbers':
        try:
            return float(value)
        except:
            return 0
    else:
        return str(value)  # fallback: treat as text

def create_or_update_monday_item(record, monday_items, monday_board_id, monday_token, field_mapping):
    import requests
    salesforce_id = record.get("Id")
    if not salesforce_id:
        return
    
    if monday_board_id == "9378000505":
        item_name = record.get('Company')
    else:
        item_name = record.get('Name') or f"{record.get('FirstName', '')} {record.get('LastName', '')}".strip()

    # Step 1: 변환 대상 만들기
    column_values = {} #이 monday컬럼에는 이 값이 들어가야해~ 하는 dict
    for monday_col_id, sf_field in field_mapping.items(): # 가령 monday_col_id = "text_mkrykrc2", sf_field = "Name"
        value = record.get(sf_field, "") # value = record.get('Name', "") = 'Stesting Stesstee'
        # 기존 monday item이 있다면 type 재활용
        if salesforce_id in monday_items: # 00QUO00000F8FAv2AN가 monday_items에 있다면
            col_type = monday_items[salesforce_id]["column_values"].get(monday_col_id, {}).get("type", "text") #현재 Stesstee의 컬럼 타입을 가져옴
        else:
            col_type = "text"
        column_values[monday_col_id] = format_value_for_column(value, col_type)
        #column_values = {monday_col_id: {"label": value}}
        #GraphQL 형식 맞춰서 Salesforce로부터 받은 data를 monday.com의 컬럼 type에 맞게 Monday.com으로 밀어넣으려고. 
        
    # Step 2: Create
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
            "columnValues": json.dumps(column_values)
        }

        r = requests.post(MONDAY_API_URL, headers={"Authorization": monday_token}, json={"query": query, "variables": variables})
        response = r.json()
        if "errors" in response:
            print(f"❌ Failed to create item: {item_name}")
            print(response["errors"])
        else:
            print(f"✅ Created: {item_name}", flush=True)
        return

    # Step 3: Update
    current = monday_items[salesforce_id]['column_values']
    updated = {}
    for k, v in column_values.items(): #column_values는 salesforce에서 가져온 값이고, current는 monday_items에서 가져온 값임
        current_val = current.get(k, {}).get("value")
        if v != current_val:
            updated[k] = v

    if updated:
        query = '''
        mutation ($itemId: ID!, $boardId: ID!, $columnValues: JSON!) {
            change_multiple_column_values(item_id: $itemId, board_id: $boardId, column_values: $columnValues) {
                id
            }
        }
        '''
        variables = {
            "itemId": monday_items[salesforce_id]['item_id'],
            "boardId": monday_board_id,
            "columnValues": json.dumps(updated)
        }
        r = requests.post(MONDAY_API_URL, headers={"Authorization": monday_token}, json={"query": query, "variables": variables})
        response = r.json()
        if "errors" in response:
            print(f"❌ Update error for {item_name}")
            print(response["errors"])
        else:
            print(f"🔁 Updated: {item_name}", flush=True)
    else:
        print(f"⏩ Skipped (no change): {item_name}", flush=True)