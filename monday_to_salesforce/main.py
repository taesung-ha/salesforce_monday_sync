#%%
# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from handlers.create_pulse import handle_create_pulse
from handlers.update_column import handle_update_column
from handlers.update_name import handle_update_name
from services.log_service import create_log_table, send_telegram_alert

app = FastAPI()

@app.on_event("startup")
def setup():
    try:
        create_log_table()
        print("✅ Log table created successfully.")
    except Exception as e:
        print(f"Error during setup: {e}")

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/webhook")
async def monday_webhook(req: Request):
    try:
        data = await req.json()
        print("📥 Received from Monday:", data)
        
        if "challenge" in data:
            return JSONResponse(content={"challenge": data["challenge"]})
        
        event = data.get("event", {})
        event_type = event.get("type", "")
        
        if event_type == "create_pulse":
            return await handle_create_pulse(event)
        elif event_type == "update_column_value":
            return await handle_update_column(event)
        elif event_type == "update_name":
            return await handle_update_name(event)
        
        return JSONResponse(content={"status": "✅ Webhook received but no action taken"})
    
    except Exception as e:
        send_telegram_alert(f"❌ Error in webhook processing: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})