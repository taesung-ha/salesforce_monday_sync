from services.monday_service import get_monday_item_details
from services.salesforce_service import update_salesforce_lead
from services.log_service import log_to_db 

async def handle_update_name(event):
    new_name = event.get('value', {}).get('name', '')
    board_id = event.get('boardId')
    item_id = event.get('pulseId')
    
    item_data = get_monday_item_details(item_id, board_id)
    lead_id = item_data.get("event", {}).get("columnValues", {}).get('text_mkryhch5', {}).get('value', '')
    
    if lead_id.startswith('00Q'):
        update_salesforce_lead(lead_id, {"Company": new_name})
        log_to_db("update_name", board_id, item_id, "", "success", response_data = {"lead_id": lead_id, "Company": new_name})
        print(f"✅ Updated Lead Company for {lead_id}")
        return {"status": f"✅ Updated Lead Company for {lead_id}"}
    
    log_to_db("update_name", board_id, item_id, "", "skipped", response_data={"msg": "No Lead Id"})
    print("⏩ Skipped: No Lead Id")
    return {"status": "⏩ Skipped: No Lead Id"}
    