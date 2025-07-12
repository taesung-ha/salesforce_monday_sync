# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from salesforce_api import create_salesforce_lead_from_monday
from monday_api import get_monday_item_details

app = FastAPI()

@app.post('/webhook')
async def monday_webhook(req: Request):
    data = await req.json()
    print("Received from Monday:", data)
    
    if "challenge" in data:
        return JSONResponse(content={"challenge": data["challenge"]})
    
    event = data.get("event", {})
    column_id = event.get("columnId", "")
    new_value = event.get("value", {})
    status_label = new_value.get("label", {}).get("text", "")
    
    if column_id == "color_mksj2adq" and status_label == "Qualified":
        item_id = event.get("pulseId", "")
        board_id = event.get("boardId", "")
        
        item_data = get_monday_item_details(item_id, board_id)
        lead_source = item_data.get('short_textzb4g11iz')
        if not isinstance(lead_source, str):
            lead_source = ''

        if lead_source != 'MondayForm':
            return {"status": "⏩ Skipped: Not from MondayForm"}

        result = create_salesforce_lead_from_monday(item_data)
        return {"status": result}

    return {"status": "⏩ Skipped: Not Qualified update"}



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

'''
{'event': 
{'app': 'monday', 'type': 'update_column_value', 'triggerTime': '2025-07-12T09:48:32.792Z', 
'subscriptionId': 542173598, 'isRetry': False, 'userId': 75857771, 'originalTriggerUuid': None, 'boardId': 9378000505, 
'groupId': 'group_mkry9yes', 'pulseId': 9575061505, 'pulseName': 'Organization Name', 'columnId': 'color_mksj2adq', 
'columnType': 'color', 'columnTitle': 'Status', 'value': {'label': {'index': 4, 'text': 'Review New Lead', 
'style': {'color': '#9d50dd', 'border': '#9238af', 'var_name': 'purple'}, 'is_done': False}, 'post_id': None}, 
'previousValue': {'label': {'index': 1, 'text': 'Open - Not Contacted', 
'style': {'color': '#00c875', 'border': '#00b461', 'var_name': 'green-shadow'}, 'is_done': True}, 'post_id': None}, 
'changedAt': 1752313712.3719661, 'isTopGroup': True, 'triggerUuid': '2e3c2e4bc271f90f8032dd1a30ca6ef1'}}
'''

'''
item_data: 
{'text_mkrykrc2': {}, 'short_textzb4g11iz': 'MondayForm', 
'text_mkryhch5': {}, 'multiple_person_mks8n9aj': {}, 
'color_mksj2adq': {'index': 7, 'post_id': None, 'changed_at': '2025-07-12T10:34:37.736Z'}, 
'board_relation_mksdqfg0': {}, 'board_relation_mks9cjfs': {}, 'board_relation_mks95q': {}, 
'text_mkrymwp3': 'Email', 'text_mkryhzq7': 'Phone', 'text_mkry13cw': 'First Name', 
'text_mkry1xy1': 'Last Name', 'text_mks821t': 'www.test.org', 
'color_mksfebkh': {'index': 13, 'post_id': None, 'changed_at': '2025-07-12T06:08:23.198Z'}, 
'color_mksf6mtf': {'index': 12, 'post_id': None, 'changed_at': '2025-07-12T06:08:23.200Z'}, 
'text_mksf27hv': 'Title', 'text_mksfswxm': 'Industy_please_specify', 
'text_mksfjsre': 'Other_please_specify', 'text_mkrym6fa': 'City', 'text_mkryzhzt': {}, 
'text_mkryz0sr': 'State', 'text_mkryq1r8': {}, 'text_mkryrr5y': 'Zip Code', 'text_mkryamt0': {}, 
'text_mkrym3j7': {}, 'dropdown_mksfe98g': {'ids': [8], 'changed_at': '2025-07-12T06:08:23.209Z'}, 
'dropdown_mksfyfqp': {'ids': [9], 'changed_at': '2025-07-12T06:08:23.211Z'}, 
'color_mksf6q5r': {'index': 1, 'post_id': None, 'changed_at': '2025-07-12T06:08:23.213Z'}, 
'dropdown_mksf2z7p': {'ids': [0, 3], 'changed_at': '2025-07-12T06:08:23.214Z'}, 
'long_text_mksfhq35': {'text': 'Main challenges', 'changed_at': '2025-07-12T06:08:23.216Z'}, 
'dropdown_mksf657r': {'ids': [10], 'changed_at': '2025-07-12T06:08:23.217Z'}, 
'text_mksfjtqd': 'where did you hear-please specify', 'text_mksfsgjw': 'Funding Type-Other', 
'long_text_mksf3snn': {'text': 'Which covered populations_please_specify', 'changed_at': '2025-07-12T06:08:23.211Z'}, 
'long_text_mksfzsqt': {'text': 'What are your needs - please specify', 'changed_at': '2025-07-12T06:08:23.212Z'}, 
'text_mkrye90n': {}, 'text_mkry40xt': {}, 'text_mkryhpf0': {}, 'long_text_mksjh7w5': {}, 'text_mkryf4cd': {}, 'text_mkryxqtf': {}, 
'text_mkry427s': {}, 'text_mkryr3pj': {}, 'text_mkry53df': {}, 'text_mkryp43z': {}, 
'text_mkry581q': {}, 'date_mkspa7vk': {'date': '2025-07-11', 'changed_at': '2025-07-12T06:08:27.423Z'}}
'''