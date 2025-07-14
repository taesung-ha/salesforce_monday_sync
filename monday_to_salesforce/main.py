#%%
# main.py
from fastapi import FastAPI, Request
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

        event = data.get('event', {})
        event_type = event.get('type', '')
        column_id = event.get('columnId', '')
        item_id = event.get('pulseId', '')
        board_id = event.get('boardId', '')
        column_values = event.get('columnValues', {})

        if event_type == "create_pulse": #create_pulse 이벤트 처리
            if column_values.get('short_textzb4g11iz', {}).get('value', '') == 'MondayForm':

                item_data = get_monday_item_details(item_id, board_id)
                lead_id = create_salesforce_lead_from_monday(item_data)

                if isinstance(lead_id, str) and lead_id.startswith("00Q"): #Monday.com에 Salesforce Lead ID 업데이트
                    update_monday_column(item_id=item_id, board_id=board_id, column_id='text_mkryhch5', value=lead_id)
                else:
                    return JSONResponse(content={"status": f"❌ Failed to create lead: {lead_id}"})

            else:
                print({"status": "⏩ Skipped: Not from MondayForm"})
                return JSONResponse(content={"status": "⏩ Skipped: Not from MondayForm"})

        return JSONResponse(content={"status": "✅ Webhook received but no action taken"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    

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
Received from Monday: 
{'event': 
{'app': 'monday', 'type': 'update_column_value', 'triggerTime': '2025-07-13T01:26:52.397Z', 
'subscriptionId': 542173598, 'isRetry': False, 'userId': 75857771, 'originalTriggerUuid': None, 
'boardId': 9378000505, 'groupId': 'group_mkry9yes', 'pulseId': 9575061505, 
'pulseName': 'Organization Name', 'columnId': 'color_mksj2adq', 'columnType': 'color', 
'columnTitle': 'Status', 
'value': 
{'label': {'index': 7, 'text': 'Qualified', 'style': {'color': '#579bfc', 'border': '#4387e8', 'var_name': 'bright-blue'}, 
'is_done': False}, 'post_id': None}, 
'previousValue': {'label': {'index': 5, 'text': None, 
'style': {'color': '#c4c4c4', 'border': '#b0b0b0', 'var_name': 'grey'}, 'is_done': False}, 'post_id': None}, 
'changedAt': 1752370012.0153196, 'isTopGroup': True, 'triggerUuid': 'e87d900d930bec8f6dfb70deba1f5b5c'}}
'''



'''
Received from Monday: 
{'event': 
{'app': 'monday', 'type': 'create_pulse', 'triggerTime': '2025-07-14T05:19:35.448Z', 'subscriptionId': 541697599, 'isRetry': False, 'userId': -6, 
'originalTriggerUuid': None, 'boardId': 9378000505, 'pulseId': 9579254502, 'pulseName': 'Test For Migration org', 'groupId': 'group_mkry9yes', 
'groupName': 'Lead', 'groupColor': '#00c875', 'isTopGroup': True, 
'columnValues': {'text_mks821t': {'value': 'www.test.org'}, 'color_mksfebkh': {'label': {'index': 2, 'text': 'Digital Equity', 
'style': {'color': '#df2f4a', 'border': '#ce3048', 'var_name': 'red-shadow'}, 'is_done': False}, 'post_id': None}, 
'color_mksf6mtf': {'label': {'index': 0, 'text': 'Disability', 'style': {'color': '#fdab3d', 'border': '#e99729', 'var_name': 'orange'}, 'is_done': False}, 'post_id': None}, 
'text_mkrykrc2': {'value': 'Tae Sung Ha'}, 'text_mkry13cw': {'value': 'Tae Sung'}, 'text_mkry1xy1': {'value': 'Ha'}, 
'dropdown_mkstb9d4': {'chosenValues': [{'id': 5, 'name': 'Alaska'}]}, 'text_mksf27hv': {'value': 'Data Volunteer'}, 
'text_mkrymwp3': {'value': 'taesungha6502@gmail.com'}, 'text_mkryhzq7': {'value': '12341251'}, 'text_mkrym6fa': {'value': 'Ann Arbor'}, 
'text_mkryrr5y': {'value': '12515'}, 
'dropdown_mksfe98g': {'chosenValues': [{'id': 2, 'name': 'Incarcerated and recently released incarcerated individuals (as defined by the State of California)'}]}, 'dropdown_mksfyfqp': 
{'chosenValues': [{'id': 2, 'name': 'Digital Navigator and/or Instructor Training'}]}, 
'color_mksf6q5r': {'label': {'index': 1, 'text': '$500 - $1,500', 'style': {'color': '#00c875', 'border': '#00b461', 'var_name': 'green-shadow'}, 'is_done': True}, 'post_id': None}, 
'dropdown_mksf2z7p': {'chosenValues': [{'id': 1, 'name': 'Grant'}]}, 
'long_text_mksfhq35': {'text': 'test for mirgration main challenges', 'changed_at': '2025-07-14T05:19:34.318Z'}, 
'dropdown_mksf657r': {'chosenValues': [{'id': 12, 'name': 'Web Search (Google, Bing, etc.)'}]}, 
'short_textzb4g11iz': {'value': 'MondayForm'}}, 'triggerUuid': '53d96e100aba6ef2ac5667117e800915'}}
'''

'''
Received from Monday: 
{'event': 
{'app': 'monday', 'type': 'update_column_value', 'triggerTime': '2025-07-14T05:19:39.271Z', 'subscriptionId': 542173598, 'isRetry': False, 
'userId': -4, 'originalTriggerUuid': None, 'boardId': 9378000505, 'groupId': 'group_mkry9yes', 'pulseId': 9579254502, 
'pulseName': 'Test For Migration org', 'columnId': 'date_mkspa7vk', 'columnType': 'date', 'columnTitle': 'Date', 
'value': {'date': '2025-07-13', 'icon': None, 'time': None, 'changed_at': '2025-07-14T05:19:38.194Z'}, 'previousValue': None, 
'changedAt': 1752470378.923688, 'isTopGroup': True, 'triggerUuid': '9a6acc5885cf719ff528f9580956ad09'}}
'''