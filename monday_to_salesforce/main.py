from fastapi import FastAPI, Request
from salesforce_api import send_to_salesforce

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await req.json()
    print (f"Received data: {data}")
    
    try:
        item_name = data['event']['pulseName']
        board_id = data['event']['board']
    except KeyError:
        return {"error": "Invalid payload"}
    
    result = send_to_salesforce(item_name, board_id)
    return {"status": "success", "result": result}