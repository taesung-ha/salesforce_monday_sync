from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from salesforce_api import send_to_salesforce

app = FastAPI()

@app.post('/webhook')
async def monday_webhook(req: Request):
    data = await req.json()
    print("Received from Monday:", data)
    
    if "challenge" in data:
        return JSONResponse(content={"challenge": data["challenge"]})
    
    try:
        item_name = data['event']['pulseName']
        board_id = data['event']['boardId']
    except KeyError:
        return {"error": "Invalid payload"}
    
    result = send_to_salesforce(item_name, board_id)
    return {"status": result}