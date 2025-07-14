# main.py
from fastapi import FastAPI, Request
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, WebhookLog
from fastapi.responses import JSONResponse
from salesforce_api import create_salesforce_lead_from_monday
from monday_api import get_monday_item_details, update_monday_column
import json

app = FastAPI()

@app.post('/webhook')
async def monday_webhook(req: Request):
    try:
        data = await req.json()
        print("Received from Monday:", data)
        
        if "challenge" in data:
            return JSONResponse(content={"challenge": data["challenge"]})

        event = data.get("event", {})
        column_id = event.get("columnId", "")
        new_value = event.get("value", {})
        status_label = ""
    
        if new_value and isinstance(new_value, dict):
            status_label = new_value.get("label", {}).get("text", "")
            
        log_data = {
            "event_type": event.get("type"),
            "board_id": event.get("boardId"),
            "item_id": event.get("pulseId"),
            "column_id": column_id,
            "new_value": json.dumps(new_value)
        }

        if column_id == "color_mksj2adq" and status_label == "Qualified":
            item_id = event.get("pulseId", "")
            board_id = event.get("boardId", "")
            item_data = get_monday_item_details(item_id, board_id)

            lead_source = item_data['event']['columnValues'].get('short_textzb4g11iz', {}).get('value', '')
            if not isinstance(lead_source, str):
                lead_source = ''

            if lead_source != 'MondayForm':
                print({"status": "⏩ Skipped: Not from MondayForm"})
                return JSONResponse(content={"status": "⏩ Skipped: Not from MondayForm"})

            lead_id = create_salesforce_lead_from_monday(item_data)
            
            if isinstance(lead_id, str) and lead_id.startswith("00Q"):
                update_monday_column(item_id=item_id, board_id='9378000505', column_id='text_mkryhch5', value=lead_id)
            else:
                return JSONResponse(content={"status": f"❌ Failed to create lead: {lead_id}"})

        return JSONResponse(content={"status": "⏩ Skipped: Not Qualified update"})

    except Exception as e:
          return JSONResponse(status_code=500, content={"error": str(e)})