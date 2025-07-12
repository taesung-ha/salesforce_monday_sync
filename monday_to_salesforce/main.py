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
    
    #result = send_to_salesforce(item_name, board_id)
    #return {"status": result}

'''
{'event': {'app': 'monday', 'type': 'create_pulse', 'triggerTime': '2025-07-12T03:41:18.949Z', 'subscriptionId': 541152729, 'isRetry': False, 'userId': 75857771, 'originalTriggerUuid': None, 'boardId': 9378000505, 'pulseId': 9574928089, 'pulseName': 'SI Test Org', 'groupId': 'group_mkry9yes', 'groupName': 'Lead', 'groupColor': '#00c875', 'isTopGroup': True, 
'columnValues': {'text_mkryhch5': {'value': '00QUO00000EekC92AJ'}, 
'text_mkry1xy1': {'value': 'Ebook Form'}, 
'text_mkry13cw': {'value': 'Test SectorIndustry'}, 
'text_mks821t': {'value': 'None'}, 
'text_mkryp43z': {'value': 'None'}, 
'text_mkry427s': {'value': '0123p000000EILJAA4'}, 
'text_mkry53df': {'value': 'None'}, 
'text_mkry581q': {'value': 'None'}, 
'text_mkryzhzt': {'value': '2025-02-10T19:35:49.000+0000'}, 
'text_mkryr3pj': {'value': '2025-02-10T19:36:28.000+0000'}, 
'text_mkrykrc2': {'value': 'Test SectorIndustry Ebook Form'}, 
'text_mkryq1r8': {'value': 'None'}, 
'text_mkrym6fa': {'value': 'None'}, 
'text_mkryz0sr': {'value': 'Colorado'}, 
'text_mkryrr5y': {'value': 'None'}, 
'text_mkrym3j7': {'value': 'United States'}, 'text_mkryamt0': {'value': 'CO'}, 
'text_mkrye90n': {'value': 'US'}, 
'text_mkry40xt': {'value': "{'city': None, 'country': 'United States', 'countryCode': 'US', 'geocodeAccuracy': None, 'latitude': None, 'longitude': None, 'postalCode': None, 'state': 'Colorado', 'stateCode': 'CO', 'street': None}"}, 
'text_mkryhzq7': {'value': 'None'}, 'text_mkryhpf0': {'value': 'None'}, 
'text_mkrymwp3': {'value': 'testbusdev1@gmail.com'}, 
'long_text_mksjh7w5': {'text': 'None', 'changed_at': '2025-07-12T03:41:17.634Z'}, 
'color_mksj2adq': {'label': {'index': 2, 'text': 'Closed - Converted', 'style': {'color': '#df2f4a', 'border': '#ce3048', 'var_name': 'red-shadow'}, 'is_done': False}, 'post_id': None}, 
'text_mkryxqtf': {'value': 'True'}, 'text_mkryf4cd': {'value': 'Partner'}, 'short_textzb4g11iz': {'value': 'Ebook Download'}}, 
'triggerUuid': '53ad5813cb2daa5bd366478bbfdaaece'}}
'''