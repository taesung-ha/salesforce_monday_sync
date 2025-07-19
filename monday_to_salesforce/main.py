#main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from handlers.entity_handler import handle_update_column, handle_create_pulse, handle_update_name
from config.entity_config import ENTITY_CONFIG

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "ok"} 

@app.post("/webhook")
async def monday_webhook(req: Request):
    try:
        data = await req.json()
        print("📥 Received from Monday:", data)

        # Webhook 검증 (challenge 처리)
        if "challenge" in data:
            return JSONResponse(content={"challenge": data["challenge"]})

        event = data.get("event", {})
        board_id = event.get("boardId")
        event_type = event.get("type")

        # ENTITY_CONFIG에서 entity_type 식별
        entity_type = None
        for name, config in ENTITY_CONFIG.items():
            if config["board_id"] == board_id:
                entity_type = name
                break

        if not entity_type:
            print(f"⚠️ Unknown board: {board_id}")
            return {"status": "Skipped: Unknown board"}

        # 이벤트 타입별 핸들러 호출
        if event_type == "update_column_value":
            return await handle_update_column(event, entity_type)
        elif event_type == "create_pulse":
            return await handle_create_pulse(event, entity_type)
        elif event_type == "update_name":
            return await handle_update_name(event, entity_type)

        print(f"ℹ️ Event type {event_type} not handled.")
        return {"status": f"Unhandled event type: {event_type}"}

    except Exception as e:
        print(f"❌ Error in webhook: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})