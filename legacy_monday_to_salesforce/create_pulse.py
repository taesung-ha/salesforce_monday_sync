#create_pulse.py
from services.monday_service import get_monday_item_details, update_monday_column
from services.salesforce_service import create_salesforce_lead, update_salesforce_lead
from services.log_service import log_to_db, send_telegram_alert

async def handle_create_pulse(event):
    board_id = event.get('boardId')
    item_id = event.get('itemId')
    column_values = event.get('columnValues', {})
    
    if column_values.get('short_textzb4g11iz', {}).get('value') != 'MondayForm':
        return {"messages": "⏩ Skipped: Not from MondayForm"}
    
    item_data = get_monday_item_details(item_id, board_id)
    
    lead_id, response = create_salesforce_lead(item_data)
    
    if lead_id and lead_id.startswith('00Q'):
        update_monday_column(item_id, board_id, 'text_mkryhch5', lead_id)
        log_to_db("create_pulse", board_id, item_id, "", "success", response_data=response)
        print(f"✅ Lead created successfully: {lead_id}")
        return {"messages": f"✅ Lead created successfully: {lead_id}"}

    else:
        send_telegram_alert(f"❌ Failed to create lead for item {item_id} on board {board_id}: {response}")
        log_to_db("create_pulse", board_id, item_id, "", "failed", response_data=response)
        print(f"❌ Failed to create lead: {response}")
        return {"status": f"❌ Failed to create lead: {response}"}
