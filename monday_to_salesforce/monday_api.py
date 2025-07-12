# monday_api.py
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
                return {
                    col['id']: json.loads(col['value']) if col['value'] else {}
                    for col in item['column_values']
                }
        cursor = result['data']['boards'][0]['items_page']['cursor']
        if not cursor:
            break
    return {}
