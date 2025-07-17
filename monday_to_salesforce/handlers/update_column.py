from services.monday_service import get_monday_item_details
from services.salesforce_service import update_salesforce_lead
from services.log_service import log_to_db
from utils.mappings import COLUMN_MAPPING

async def handle_update_column(event):
    board_id = event.get('boardId')
    item_id = event.get('pulseId')
    column_id = event.get('columnId')
    
    item_data = get_monday_item_details(item_id, board_id)
    column_values = item_data.get("event", {}).get("columnValues", {})
    lead_id = column_values.get('text_mkrych5', {}).get('value', '')
    
    if not lead_id.startswith('00Q'):
        log_to_db("update_column_value", board_id, item_id, column_id, status="skipped", response_data={"msg": "Lead ID missing"})
        print("⏩ Skipped: No Salesforce Lead Id")
        return {"status": "⏩ Skipped: No Salesforce Lead Id"}
    
    if column_id in COLUMN_MAPPING:
        sf_field, value_key, transform_fn = COLUMN_MAPPING[column_id]
        raw_value = column_values.get(column_id, {}).get(value_key, "")
        value = transform_fn(raw_value) if transform_fn else raw_value

        if value:
            update_salesforce_lead(lead_id, {sf_field: value})
            log_to_db("update_column_value", board_id, item_id, column_id, status='success', response_data = {'lead_id': lead_id, 'field': sf_field, 'value': value})
            print(f"✅ Updated {sf_field} for Lead {lead_id}")
            return {"status": f"✅ Updated {sf_field} for Lead {lead_id}"}
        
    log_to_db("update_column_value", board_id, item_id, column_id, status="skipped", response_data={"msg": "No mapping"})
    print("⏩ Skipped: No mapping for column")
    return {"status": "⏩ Skipped: No mapping for column"}