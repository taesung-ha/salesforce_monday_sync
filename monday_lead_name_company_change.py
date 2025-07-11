#%%
import requests
import json
import time
from config import MONDAY_TOKEN
BOARD_ID = "9378000505"
COMPANY_COL_ID = "text_mkrykrc2"  # 'Company' 컬럼의 실제 column_id
headers = {
    "Authorization": MONDAY_TOKEN,
    "Content-Type": "application/json"
}
MONDAY_URL = "https://api.monday.com/v2"
items = []
cursor = None
#%%
# Step 1: 모든 아이템 불러오기
while True:
    query = '''
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
            }
          }
        }
      }
    }
    '''
    variables = {"boardId": BOARD_ID, "cursor": cursor}

    response = requests.post(
        MONDAY_URL,
        headers=headers,
        json={"query": query, "variables": variables}
    )
    res_json = response.json()

    if "errors" in res_json:
        print("❌ Error fetching items:", json.dumps(res_json["errors"], indent=2))
        break

    data = res_json['data']['boards'][0]['items_page']
    items.extend(data['items'])

    cursor = data['cursor']
    if not cursor:
        break

    time.sleep(0.3)  # rate limit 보호용
#%%
# Step 2: 각 아이템의 item name과 company 컬럼 값 교환
for item in items:
    item_id = item['id']
    item_name = item['name']
    company_value = None

    for col in item['column_values']:
        if col['id'] == COMPANY_COL_ID:
            company_value = col['text']
            break

    # 둘 다 비어있지 않을 때만 교환
    if company_value and item_name and company_value != item_name:
        mutation = '''
    mutation (
      $itemId: ID!, 
      $boardId: ID!, 
      $newNameValue: JSON!, 
      $newCompanyValue: JSON!
    ) {
      nameUpdate: change_column_value(
        item_id: $itemId, 
        board_id: $boardId, 
        column_id: "name", 
        value: $newNameValue
      ) {
        id
      }
      companyUpdate: change_column_value(
        item_id: $itemId, 
        board_id: $boardId, 
        column_id: "%s", 
        value: $newCompanyValue
      ) {
        id
      }
    }
    ''' % COMPANY_COL_ID

    variables = {
        "itemId": str(item_id),
        "boardId": str(BOARD_ID),
        "newNameValue": json.dumps(company_value),
        "newCompanyValue": json.dumps(item_name)
    }

    response = requests.post(MONDAY_URL, headers=headers, json={"query": mutation, "variables": variables})
    res_json = response.json()

    if "errors" in res_json:
        print(f"❌ Failed to swap item {item_id}: {res_json['errors']}")
    else:
        print(f"✅ Swapped item {item_id}: item_name='{company_value}', company='{item_name}'")
# %%
