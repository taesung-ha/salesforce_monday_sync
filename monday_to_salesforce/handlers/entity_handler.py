from config.entity_config import ENTITY_CONFIG
from services.monday_service import get_monday_item_details, update_monday_column
from services.salesforce_service import update_salesforce_record, create_salesforce_record
from services.log_service import log_to_db, send_telegram_alert
from utils.transformer import split_name, get_newly_linked_ids
from datetime import datetime, timezone

async def handle_update_column(event, entity_type):
    config = ENTITY_CONFIG[entity_type]
    board_id = event.get("boardId")
    item_id = event.get("pulseId")
    column_id = event.get("columnId")

    # Monday item 상세 데이터 가져오기
    item_data = get_monday_item_details(item_id, board_id)
    column_values = item_data.get("event", {}).get("columnValues", {})
    sf_id = column_values.get(config["sf_id_column"], {}).get("value", "")
    """
    item_data 구조:
    {
        "event": {
            "pulseName": "CompanyName",
            "columnValues": {
                "short_textzb4g11iz": {"value": "MondayForm"},
                "email_mksx3vtp": {"value": "test@example.com"},
                ...
            }
        }
    }
    """
    if not sf_id:
        log_to_db("update_column_value", board_id, item_id, column_id, "skipped",
                  response_data={"msg": "No Salesforce ID"})
        
        print(f"⏩ Skipped: No Salesforce ID for item {item_id} on board {board_id}")
        return {"status": "⏩ Skipped: No Salesforce ID"}

    # 컬럼 매핑 확인
    if column_id in config["field_mapping"]:
        sf_field, value_key, transform_fn = config["field_mapping"][column_id]
        col_data = column_values.get(column_id, {})
    
        if isinstance(col_data, (int, float)):
            value = col_data
        else:
            raw_value = col_data.get(value_key, "")
            value = transform_fn(raw_value) if transform_fn else raw_value

        success = update_salesforce_record(config["object_name"], sf_id, {sf_field: value})
        log_to_db("update_column_value", board_id, item_id, column_id,
                    "success" if success else "failed",
                    response_data={"sf_id": sf_id, "field": sf_field, "value": value})
        print(f"✅ Updated {sf_field} for {entity_type} {sf_id}, Updated value: {value}")
        return {"status": f"Updated {sf_field} for {entity_type} {sf_id}, Updated value: {value}"}
    
    log_to_db("update_column_value", board_id, item_id, column_id, "skipped",
              response_data={"msg": f"No mapping for column {column_id}"})
    
    print(f"⏩ Skipped: No mapping for column {column_id} in {entity_type}")
    return {"status": "⏩ Skipped: No mapping for this column"}


async def handle_create_pulse(event, entity_type):
    config = ENTITY_CONFIG[entity_type]
    board_id = event.get("boardId")
    item_id = event.get("pulseId")
    item_data = get_monday_item_details(item_id, board_id)
    column_values = item_data.get("event", {}).get("columnValues", {})
    """
    item_data 구조:
    {
        "event": {
            "pulseName": "CompanyName",
            "columnValues": {
                "short_textzb4g11iz": {"value": "MondayForm"},
                "email_mksx3vtp": {"value": "test@example.com"},
                ...
            }
        }
    }
    """
    # Salesforce 생성용 Payload 구성
    sf_payload = {}
    
    if entity_type == "Lead":
        sf_payload['Company'] = item_data.get("event", {}).get("pulseName", "")
        sf_payload['LastName'] = 'Unknown'  # Lead는 LastName 필수, 기본값 설정

    elif entity_type == "Account":
        sf_payload['Name'] = item_data.get("event", {}).get("pulseName", "")

    elif entity_type == "Opportunity":
        sf_payload['Name'] = item_data.get("event", {}).get("pulseName", "")
        sf_payload['StageName'] = 'Need Analysis'  # 기본 Stage 설정
        sf_payload['CloseDate'] = datetime.now(timezone.utc).strftime('%Y-%m-%d') # 기본 CloseDate 설정

    else:
        full_name = item_data.get("event", {}).get("pulseName", "")
        first_name, last_name = split_name(full_name)
        sf_payload['FirstName'] = first_name
        sf_payload['LastName'] = last_name
    
    if config.get("record_type", ""):
        sf_payload["RecordTypeId"] = config["record_type"]
    
    for col_id, (sf_field, value_key, transform_fn) in config["field_mapping"].items():
        raw_value = column_values.get(col_id, {}).get(value_key, "")
        value = transform_fn(raw_value) if transform_fn else raw_value
        if value:
            sf_payload[sf_field] = value

    sf_id = create_salesforce_record(config["object_name"], sf_payload)
    
    if sf_id:
        update_monday_column(item_id, board_id, config["sf_id_column"], sf_id)
        log_to_db("create_pulse", board_id, item_id, "", "success", response_data={"sf_id": sf_id})
        print(f"✅ {entity_type} created: {sf_id}")
        return {"messages": f"✅ {entity_type} created: {sf_id}"}

    send_telegram_alert(f"❌ Failed to create {entity_type} for item {item_id}")
    log_to_db("create_pulse", board_id, item_id, "", "failed")
    print(f"❌ Failed to create {entity_type} for item {item_id}")
    return {"status": f"❌ Failed to create {entity_type}"}


async def handle_update_name(event, entity_type):
    config = ENTITY_CONFIG[entity_type]
    new_name = event.get("value", {}).get("name", "")
    board_id = event.get("boardId")
    item_id = event.get("pulseId")

    item_data = get_monday_item_details(item_id, board_id)
    sf_id = item_data.get("event", {}).get("columnValues", {}).get(config["sf_id_column"], {}).get("value", "")

    success = False

    if sf_id:
        if entity_type == "Lead":
            # Lead의 경우 Company 필드 업데이트
            success = update_salesforce_record(config["object_name"], sf_id, {"Company": new_name})
        elif entity_type in ["Account", "Opportunity"]:
            success = update_salesforce_record(config["object_name"], sf_id, {"Name": new_name})
        else:
            first_name, last_name = split_name(new_name)
            success = update_salesforce_record(config["object_name"], sf_id, {"FirstName": first_name, "LastName": last_name})

        log_to_db("update_name", board_id, item_id, "", "success" if success else "failed",
                response_data={"sf_id": sf_id, "Name": new_name})
        
        if success:
            print(f"✅ Updated Name for {entity_type} {sf_id}")
            return {"status": f"✅ Updated Name for {entity_type} {sf_id}"}
        
        else:
            send_telegram_alert(f"❌ Failed to update Name for {entity_type} {sf_id}")
            print(f"❌ Failed to update Name for {entity_type} {sf_id}")
            return {"status": f"❌ Failed to update Name for {entity_type}"}

    log_to_db("update_name", board_id, item_id, "", "skipped", response_data={"msg": "No Salesforce ID"})
    print(f"⏩ Skipped: No Salesforce ID for item {item_id} on board {board_id}")
    return {"status": "⏩ Skipped: No Salesforce ID"}
    
async def handle_board_connection(event, entity_type):
    config = ENTITY_CONFIG[entity_type]
    board_id = event.get('boardId')
    source_item_id = event.get('pulseId')
    column_id = event.get('columnId')
    
    source_item = get_monday_item_details(source_item_id, board_id)
    column_values = source_item.get('event', {}).get('columnValues', {})
    source_sf_id = column_values.get(ENTITY_CONFIG[entity_type]["sf_id_column"], {}).get("value", "")
    
    if not source_sf_id:
        print(f"⏩ Skipped: No Salesforce ID for item {source_item_id} on board {board_id}")
        return {"status": "⏩ Skipped: No Salesforce ID"}
    
    linked_ids = get_newly_linked_ids(event)
    if not linked_ids:
        print(f"⏩ Skipped: No newly linked items for {source_item_id} on board {board_id}")
        return {"status": "⏩ Skipped: No newly linked items"}
    
    link_mapping = ENTITY_CONFIG[entity_type].get("link_mappings", {}).get(column_id)
    if not link_mapping:
        print(f"⏩ Skipped: No link mapping for column {column_id} in {entity_type}")
        return {"status": "⏩ Skipped: No link mapping for this column"}
    
    target_entity, sf_field = link_mapping
    
    for target_item_id in linked_ids:
        target_config = ENTITY_CONFIG[target_entity]
        target_item = get_monday_item_details(target_item_id, target_config["board_id"])
        target_sf_id = target_item.get("event", {}).get("columnValues", {}).get(target_config["sf_id_column"], {}).get("value", "")
        
        if target_sf_id:
            success = update_salesforce_record(config['object_name'], source_sf_id, {sf_field: target_sf_id})
            log_to_db('update_relation', board_id, source_item_id, column_id, "success" if success else "failed",
                      response_data={"source_sf_id": source_sf_id, "target_sf_id": target_sf_id, "field": sf_field})
            print(f"✅ Linked {target_entity} ({target_sf_id}) to {entity_type} ({source_sf_id}) via {sf_field}")
        else:
            log_to_db('update_relation', board_id, source_item_id, column_id, "skipped",
                      response_data={"msg": f"Target item {target_item_id} has no Salesforce ID"})
            print(f"⚠️ Target item {target_item_id} has no Salesforce ID")
        
    return {"status": f"✅ Linked {len(linked_ids)} items"}

'''
    {'event': 
    {'app': 'monday', 'type': 'update_column_value', 
    'triggerTime': '2025-07-17T08:56:17.956Z', 'subscriptionId': 542173598, 
    'isRetry': False, 'userId': 75857771, 'originalTriggerUuid': None, 
    'boardId': 9378000505, 'groupId': 'group_mkry9yes', 'pulseId': 9605887058, 
    'pulseName': 'Solo Leveling Rank E', 'columnId': 'board_relation_mks95q', 
    'columnType': 'board-relation', 'columnTitle': 'Converted_Contact', 
    'value': {'linkedPulseIds': [{'linkedPulseId': 9607665733}, 
    {'linkedPulseId': 9607679534}, {'linkedPulseId': 9607685328}, 
    {'linkedPulseId': 9608173291}], 'changed_at': '2025-07-17T08:56:15.739Z'}, 
    'previousValue': {'changed_at': '2025-07-17T08:56:03.591Z', 
    'linkedPulseIds': [{'linkedPulseId': 9607679534}, 
    {'linkedPulseId': 9607685328}, {'linkedPulseId': 9608173291}]}, 
    'changedAt': 1752742577.5786905, 'isTopGroup': True, 
    'triggerUuid': 'd8bb08692722451b36a4450816534b37'}}
'''


