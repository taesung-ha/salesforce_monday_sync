#%%
# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from salesforce_api import create_salesforce_lead_from_monday
from monday_api import get_monday_item_details, update_monday_column
from utils import log_to_db, send_telegram_alert, create_log_table
import json

app = FastAPI()

@app.on_event("startup")
def setup():
    try:
        create_log_table()
        print("Log table created successfully.")
    except Exception as e:
        print(f"Error during setup: {e}")

@app.get("/")
def root():
    return {"status": "ok"}

@app.post('/webhook')
async def monday_webhook(req: Request):
    try:
        data = await req.json()
        print("Received from Monday:", data)

        if "challenge" in data:
            return JSONResponse(content={"challenge": data["challenge"]})

        event = data.get('event', {})
        event_type = event.get('type', '')
        column_id = event.get('columnId', '')
        item_id = event.get('pulseId', '')
        board_id = event.get('boardId', '')
        column_values = event.get('columnValues', {})
        
        log_to_db(event_type, board_id, item_id, column_id, status="received", request_data=data)

        if event_type == "create_pulse": #create_pulse 이벤트 처리
            if column_values.get('short_textzb4g11iz', {}).get('value', '') == 'MondayForm':

                item_data = get_monday_item_details(item_id, board_id)
                lead_id, response_data = create_salesforce_lead_from_monday(item_data)

                if isinstance(lead_id, str) and lead_id.startswith("00Q"): #Monday.com에 Salesforce Lead ID 업데이트
                    update_monday_column(item_id=item_id, board_id=board_id, column_id='text_mkryhch5', value=lead_id)
                    print(response_data)
                    log_to_db(event_type, board_id, item_id, column_id, status="success", response_data=response_data)
                else:
                    log_to_db(event_type, board_id, item_id, column_id, status="failed", response_data=response_data)
                    send_telegram_alert(f"❌ Failed to create lead: {item_id}")
                    return JSONResponse(content={"status": f"❌ Failed to create lead: {lead_id}"})

            else:
                print({"status": "⏩ Skipped: Not from MondayForm"})
                return JSONResponse(content={"status": "⏩ Skipped: Not from MondayForm"})

        return JSONResponse(content={"status": "✅ Webhook received but no action taken"})

    except Exception as e:
        send_telegram_alert(f"❌ Error in webhook processing: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})
