#main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mangum import Mangum
from handlers.entity_handler import handle_board_connection, handle_update_column, handle_create_pulse, handle_update_name, handle_item_deleted
from services.mapping_service import create_mapping_table
from services.log_service import create_log_table
from config.entity_config import ENTITY_CONFIG
import traceback

print("✅ Lambda started execution")

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("Connecting to DB")
    create_mapping_table()
    create_log_table()
    print("✅ Mapping and log tables checked/created.")

@app.get("/")
def root():
    return {"message": "Hello from Lambda"}

handler = Mangum(app)

@app.get("/health")
def health_check():
    return {"status": "ok"} 

@app.post("/webhook")
async def monday_webhook(req: Request):
    try:
        data = await req.json()
        print("📥 Received from Monday:", data)

        # Webhook check (challenge processing)
        if "challenge" in data:
            return JSONResponse(content={"challenge": data["challenge"]})

        event = data.get("event", {})
        board_id = event.get("boardId")
        event_type = event.get("type")
        column_type = event.get("columnType", "")

        # Identify entity_type from ENTITY_CONFIG
        entity_type = None
        for name, config in ENTITY_CONFIG.items():
            if config["board_id"] == board_id:
                entity_type = name
                break

        if not entity_type:
            print(f"⚠️ Unknown board: {board_id}")
            return {"status": "Skipped: Unknown board"}

        # Call handler for each event type
        if event_type == "update_column_value" and column_type == 'board-relation':
            return await handle_board_connection(event, entity_type)
        elif event_type == "update_column_value":
            return await handle_update_column(event, entity_type)
        elif event_type == "create_pulse":
            return await handle_create_pulse(event, entity_type)
        elif event_type == "update_name":
            return await handle_update_name(event, entity_type)
        elif event_type == 'delete_pulse':
            return await handle_item_deleted(event, entity_type)
        else:
            print(f"ℹ️ Event type {event_type} not handled.")
            result = {"status": f"Unhandled event type: {event_type}"}
        
        return result

    except Exception as e:
        print(f"❌ Error in webhook: {str(e)}")
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
