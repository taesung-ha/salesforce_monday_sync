from collections import defaultdict
import requests, json
from config import API_URL, HEADERS

def fetch_items_with_column(board_id, value_col_id, extra_col_id=None):
    items = defaultdict(dict)
    cursor = None
    total_count = 0
    empty_count = 0

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
                  value
                }
              }
            }
          }
        }
        '''

        variables = {"boardId": board_id, "cursor": cursor}
        res = requests.post(API_URL, headers=HEADERS, json={"query": query, "variables": variables})
        data = res.json()["data"]["boards"][0]["items_page"]
        cursor = data.get("cursor")

        for item in data["items"]:
            item_id = item["id"]
            columns = {cv["id"]: cv for cv in item["column_values"]}

            value = columns.get(value_col_id, {}).get("text")
            connected_ids_json = columns.get(extra_col_id, {}).get("value") if extra_col_id else None

            total_count += 1
            if not value:
                empty_count += 1
                continue

            # 저장 구조
            items[value] = {
                "item_id": item_id,
                "connected_ids": connected_ids_json
            }

        if cursor is None:
            break

    print(f"📊 총 {total_count}개 항목 중 {empty_count}개 항목에 '{value_col_id}' 값이 없습니다.")
    return items
# %%
def connect_items(source_board_id, target_board_id, source_key_col_id, target_key_col_id, connect_col_id):
    print(f"📥 Target 보드({target_board_id}) 데이터 불러오는 중...")
    target_map_raw = fetch_items_with_column(target_board_id, target_key_col_id)
    # target_map을 item_id만 남기는 dict로 변환
    target_map = {k: [int(v["item_id"])] for k, v in target_map_raw.items()}

    print(f"📥 Source 보드({source_board_id}) 데이터 불러오는 중...")
    source_map = fetch_items_with_column(source_board_id, source_key_col_id, extra_col_id=connect_col_id)

    print(f"🔗 {len(source_map)}개의 항목 연결 시도 중...")

    for key, source_data in source_map.items():
        target_item_ids = target_map.get(key)
        source_item_id = int(source_data["item_id"])

        if not target_item_ids:
            print(f"⚠️ Matching Failed: '{key}' (Source item {source_item_id})")
            continue

        # 현재 연결된 항목이 있는지 확인
        existing_connected = []
        if source_data["connected_ids"]:
            try:
                parsed = json.loads(source_data["connected_ids"])
                existing_connected = [int(x) for x in parsed.get("item_ids", [])]
            except Exception as e:
                print(f"⚠️ 연결 정보 파싱 실패: {e}")

        if all(tid in existing_connected for tid in target_item_ids):
            print(f"⏩ 이미 연결됨: Source {source_item_id} → Target {target_item_ids}")
            continue

        value_json = json.dumps({"item_ids": target_item_ids})
        mutation = '''
        mutation ($boardId: ID!, $itemId: ID!, $columnId: String!, $value: JSON!) {
          change_column_value(
            board_id: $boardId,
            item_id: $itemId,
            column_id: $columnId,
            value: $value
          ) {
            id
          }
        }
        '''
        variables = {
            "boardId": source_board_id,
            "itemId": source_item_id,
            "columnId": connect_col_id,
            "value": value_json
        }

        res = requests.post(API_URL, headers=HEADERS, json={"query": mutation, "variables": variables})
        if "errors" in res.json():
            print(f"❌ 연결 실패: Source {source_item_id} → Target {target_item_ids}", flush=True)
            print(res.text)
        else:
            print(f"✅ 연결 완료: Source {source_item_id} → Target {target_item_ids}", flush=True)

    print("🎉 모든 연결 시도 완료.")