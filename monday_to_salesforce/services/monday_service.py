#%%
# monday_service.py
import requests, json
from config import MONDAY_TOKEN

MONDAY_API_URL = "https://api.monday.com/v2"

def get_monday_item_details(item_id, board_id):
    query = """
    query ($boardId: ID!, $cursor: String) {
      boards(ids: [$boardId]) {
        items_page(limit: 100, cursor: $cursor) {
          cursor
          items {
            id
            name
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
    cursor = None
    while True:
        variables = {"boardId": int(board_id), "cursor": cursor}
        response = requests.post(
            MONDAY_API_URL,
            headers={"Authorization": MONDAY_TOKEN},
            json={"query": query, "variables": variables}
        )
        result = response.json()
        items = result['data']['boards'][0]['items_page']['items']
        for item in items:
            if item['id'] == str(item_id):  # API에서 ID는 str로 반환됨
                return transform_monday_item(item)
        cursor = result['data']['boards'][0]['items_page']['cursor']
        if not cursor:
            break
    return {}

def transform_monday_item(item):
    column_dict = {}
    for cv in item['column_values']:
        col_id = cv['id']
        col_type = cv['type']
        text = cv.get('text', '')
        value = cv.get('value')
        parsed_value = None

        if col_type == 'status' and value:
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
            parsed_value = {"text": value.get("text", "")}

        elif col_type == 'dropdown':
            if value:
                value = json.loads(value)
                labels = value.get("labels")
                if labels is None and text:
                    labels = [t.strip() for t in text.split(',')]
                parsed_value = {"labels": labels or []}
            elif text:
                parsed_value = {"labels": [t.strip() for t in text.split(',')]}
            else:
                parsed_value = {"labels": []}

        else:
            parsed_value = {"value": text}

        column_dict[col_id] = parsed_value

    return {
        "event": {
            "pulseName": item.get("name", ""),
            "columnValues": column_dict
        }
    }

def update_monday_column(item_id: str, board_id: str, column_id: str, value: str):
    query = """
    mutation ($board_id: ID!, $item_id: ID!, $column_id: String!, $value: JSON!) {
      change_column_value(board_id: $board_id, item_id: $item_id, column_id: $column_id, value: $value) {
        id
      }
    }
    """
    variables = {
        "board_id": board_id,            # ⬅ 추가
        "item_id": str(item_id),         # ⬅ Int가 아닌 str(ID type)
        "column_id": column_id,
        "value": json.dumps(value)
    }

    headers = {
        "Authorization": MONDAY_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.post(
        MONDAY_API_URL,
        json={"query": query, "variables": variables},
        headers=headers
    )
    
    if not response.ok:
        print("❌ Monday update failed:", response.text)
    else:
        print(f"✅ Column {column_id} updated {value} successfully for item {item_id} on board {board_id}")
