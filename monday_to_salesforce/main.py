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
{'event': {'app': 'monday', 'type': 'create_pulse', 'triggerTime': '2025-07-12T06:11:24.507Z', 'subscriptionId': 541697599, 'isRetry': True, 'userId': -6, 'originalTriggerUuid': None, 'boardId': 9378000505, 'pulseId': 9575061505, 'pulseName': 'Organization Name', 'groupId': 'group_mkry9yes', 'groupName': 'Lead', 'groupColor': '#00c875', 'isTopGroup': True, 
'columnValues': 
{'text_mks821t': {'value': 'www.test.org'}, v 
'color_mksfebkh': {'label': {'index': 13, 'text': 'Other', 'style': {'color': '#ff5ac4', 'border': '#e04fac', 'var_name': 'light-pink'}, 'is_done': False}, 'post_id': None}, 
'text_mksfswxm': {'value': 'Industy_please_specify'}, 
'color_mksf6mtf': {'label': {'index': 12, 'text': 'Other', 'style': {'color': '#ff007f', 'border': '#e01279', 'var_name': 'dark-pink'}, 'is_done': False}, 'post_id': None}, 
'text_mksfjsre': {'value': 'Other_please_specify'}, 'text_mkry13cw': {'value': 'First Name'}, 
'text_mkry1xy1': {'value': 'Last Name'}, 'text_mksf27hv': {'value': 'Title'}, 
'text_mkrymwp3': {'value': 'Email'}, 'text_mkryhzq7': {'value': 'Phone'}, 
'text_mkrym6fa': {'value': 'City'}, 'text_mkryz0sr': {'value': 'State'}, 
'text_mkryrr5y': {'value': 'Zip Code'}, 'dropdown_mksfe98g': {'chosenValues': [{'id': 8, 'name': 'Other'}]},
'long_text_mksf3snn': {'text': 'Which covered populations_please_specify', 'changed_at': '2025-07-12T06:08:23.211Z'}, 
'dropdown_mksfyfqp': {'chosenValues': [{'id': 9, 'name': 'Other'}]}, 'long_text_mksfzsqt': {'text': 'What are your needs - please specify', 'changed_at': '2025-07-12T06:08:23.212Z'}, 
'color_mksf6q5r': {'label': {'index': 1, 'text': '$500 - $1,500', 'style': {'color': '#00c875', 'border': '#00b461', 'var_name': 'green-shadow'}, 'is_done': True}, 'post_id': None}, 
'dropdown_mksf2z7p': {'chosenValues': [{'id': 0, 'name': 'Donations'}, {'id': 3, 'name': 'Other'}]}, 
'text_mksfsgjw': {'value': 'Funding Type-Other'},
'long_text_mksfhq35': {'text': 'Main challenges', 'changed_at': '2025-07-12T06:08:23.216Z'}, 
'dropdown_mksf657r': {'chosenValues': [{'id': 10, 'name': 'Other'}]}, 
'text_mksfjtqd': {'value': 'where did you hear-please specify'}, 
'short_textzb4g11iz': {'value': 'MondayForm'}}, 'triggerUuid': 'c4d09d07a52de2707c7a0f40479f7f89'}}
'''