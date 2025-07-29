#%%
import requests
from services.mapping_service import save_mapping
from config.config import MONDAY_TOKEN
from config.entity_config import ENTITY_CONFIG

MONDAY_API_URL = "https://api.monday.com/v2"

def fetch_items_page(board_id, cursor=None):
    query = """
    query ($board_id: ID!, $cursor: String) {
        boards(ids: [$board_id]) {
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
    """
    variables = {"board_id": board_id, "cursor": cursor}

    response = requests.post(
        MONDAY_API_URL,
        headers={"Authorization": MONDAY_TOKEN, "Content-Type": "application/json"},
        json={"query": query, "variables": variables}
    )

    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")

    data = response.json()
    if "errors" in data:
        raise Exception(f"GraphQL error: {data['errors']}")

    return data["data"]["boards"][0]["items_page"]

def fetch_all_items(board_id):
    all_items = []
    cursor = None

    while True:
        page_data = fetch_items_page(board_id, cursor)
        items = page_data["items"]
        all_items.extend(items)

        cursor = page_data.get("cursor")
        if not cursor:
            break

    return all_items

def migrate_existing_data():
    for entity_type, config in ENTITY_CONFIG.items():
        board_id = config["board_id"]
        sf_id_column = config["sf_id_column"]

        print(f"▶ Migrating {entity_type} from board {board_id}...")
        items = fetch_all_items(board_id)

        for item in items:
            item_id = item["id"]
            sf_id = None
            for col in item["column_values"]:
                if col["id"] == sf_id_column:
                    sf_id = col.get("text")
                    break

            if sf_id:
                save_mapping(item_id, board_id, sf_id, entity_type)
                print(f"✅ Migrated {entity_type} item {item_id} → SF_ID {sf_id}")