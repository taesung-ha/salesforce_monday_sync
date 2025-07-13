#%%
# monday_api.py
import requests, json
from config import MONDAY_TOKEN

MONDAY_API_URL = "https://api.monday.com/v2"

import json

def transform_monday_item(item):
    column_dict = {}
    for cv in item['column_values']:
        col_id = cv['id']
        col_type = cv['type']
        text = cv.get('text', '')
        value = cv.get('value')
        parsed_value = None

        if col_type == 'status' and value:
            value = json.loads(value)
            parsed_value = {"label": text, "index": value.get("index")}

        elif col_type == 'date' and value:
            value = json.loads(value)
            parsed_value = {"date": value.get("date")}

        elif col_type == 'people' and value:
            value = json.loads(value)
            parsed_value = {"personsAndTeams": value.get("personsAndTeams", [])}

        elif col_type == 'numbers' and text:
            try:
                parsed_value = float(text)
            except:
                parsed_value = None

        elif col_type == 'long-text' and value:
            value = json.loads(value)
            parsed_value = {"text": value.get("text", "")}

        elif col_type == 'dropdown':
            if value:
                value = json.loads(value)
                labels = value.get("labels")
                if labels is None and text:
                    labels = [t.strip() for t in text.split(',')]
                parsed_value = {"labels": labels or []}
            elif text:
                parsed_value = {"labels": [t.strip() for t in text.split(',')]}
            else:
                parsed_value = {"labels": []}

        else:
            parsed_value = {"value": text}

        column_dict[col_id] = parsed_value

    return {
        "event": {
            "pulseName": item.get("name", ""),
            "columnValues": column_dict
        }
    }

def get_monday_item_details(item_id, board_id):
    query = """
    query ($boardId: ID!, $cursor: String) {
      boards(ids: [$boardId]) {
        items_page(limit: 100, cursor: $cursor) {
          cursor
          items {
            id
            name
            column_values {
              id
              text
              value
              type
            }
          }
        }
      }
    }
    """
    cursor = None
    while True:
        variables = {"boardId": int(board_id), "cursor": cursor}
        response = requests.post(
            MONDAY_API_URL,
            headers={"Authorization": MONDAY_TOKEN},
            json={"query": query, "variables": variables}
        )
        result = response.json()
        items = result['data']['boards'][0]['items_page']['items']
        for item in items:
            if item['id'] == str(item_id):  # API에서 ID는 str로 반환됨
                return transform_monday_item(item)
        cursor = result['data']['boards'][0]['items_page']['cursor']
        if not cursor:
            break
    return {}


item = {'id': '9575061505', 'name': 'Organization Name', 
'column_values': 
[{'id': 'text_mkrykrc2', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'short_textzb4g11iz', 'text': 'MondayForm', 'value': '"MondayForm"', 'type': 'text'},
{'id': 'text_mkryhch5', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'multiple_person_mks8n9aj', 'text': '', 'value': None, 'type': 'people'}, 
{'id': 'color_mksj2adq', 'text': 'Qualified', 'value': '{"index":7,"post_id":null,"changed_at":"2025-07-12T11:06:19.522Z"}', 'type': 'status'}, 
{'id': 'board_relation_mksdqfg0', 'text': None, 'value': None, 'type': 'board_relation'}, 
{'id': 'board_relation_mks9cjfs', 'text': None, 'value': None, 'type': 'board_relation'}, 
{'id': 'board_relation_mks95q', 'text': None, 'value': None, 'type': 'board_relation'}, 
{'id': 'text_mkrymwp3', 'text': 'Email', 'value': '"Email"', 'type': 'text'}, 
{'id': 'text_mkryhzq7', 'text': 'Phone', 'value': '"Phone"', 'type': 'text'}, 
{'id': 'text_mkry13cw', 'text': 'First Name', 'value': '"First Name"', 'type': 'text'}, 
{'id': 'text_mkry1xy1', 'text': 'Last Name', 'value': '"Last Name"', 'type': 'text'}, 
{'id': 'text_mks821t', 'text': 'www.test.org', 'value': '"www.test.org"', 'type': 'text'}, 
{'id': 'color_mksfebkh', 'text': 'Other', 'value': '{"index":13,"post_id":null,"changed_at":"2025-07-12T06:08:23.198Z"}', 'type': 'status'}, 
{'id': 'color_mksf6mtf', 'text': 'Other', 'value': '{"index":12,"post_id":null,"changed_at":"2025-07-12T06:08:23.200Z"}', 'type': 'status'}, 
{'id': 'text_mksf27hv', 'text': 'Title', 'value': '"Title"', 'type': 'text'}, 
{'id': 'text_mksfswxm', 'text': 'Industy_please_specify', 'value': '"Industy_please_specify"', 'type': 'text'}, 
{'id': 'text_mksfjsre', 'text': 'Other_please_specify', 'value': '"Other_please_specify"', 'type': 'text'}, 
{'id': 'text_mkrym6fa', 'text': 'City', 'value': '"City"', 'type': 'text'}, 
{'id': 'text_mkryzhzt', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'text_mkryz0sr', 'text': 'State', 'value': '"State"', 'type': 'text'}, 
{'id': 'text_mkryq1r8', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'text_mkryrr5y', 'text': 'Zip Code', 'value': '"Zip Code"', 'type': 'text'}, 
{'id': 'text_mkryamt0', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'text_mkrym3j7', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'dropdown_mksfe98g', 'text': 'Other', 'value': '{"ids":[8],"changed_at":"2025-07-12T06:08:23.209Z"}', 'type': 'dropdown'}, 
{'id': 'dropdown_mksfyfqp', 'text': 'Other', 'value': '{"ids":[9],"changed_at":"2025-07-12T06:08:23.211Z"}', 'type': 'dropdown'}, 
{'id': 'color_mksf6q5r', 'text': '$500 - $1,500', 'value': '{"index":1,"post_id":null,"changed_at":"2025-07-12T06:08:23.213Z"}', 'type': 'status'}, 
{'id': 'dropdown_mksf2z7p', 'text': 'Donations, Other', 'value': '{"ids":[0,3],"changed_at":"2025-07-12T06:08:23.214Z"}', 'type': 'dropdown'}, 
{'id': 'long_text_mksfhq35', 'text': 'Main challenges', 'value': '{"text":"Main challenges","changed_at":"2025-07-12T06:08:23.216Z"}', 'type': 'long_text'}, 
{'id': 'dropdown_mksf657r', 'text': 'Other', 'value': '{"ids":[10],"changed_at":"2025-07-12T06:08:23.217Z"}', 'type': 'dropdown'}, 
{'id': 'text_mksfjtqd', 'text': 'where did you hear-please specify', 'value': '"where did you hear-please specify"', 'type': 'text'}, 
{'id': 'text_mksfsgjw', 'text': 'Funding Type-Other', 'value': '"Funding Type-Other"', 'type': 'text'}, 
{'id': 'long_text_mksf3snn', 'text': 'Which covered populations_please_specify', 'value': '{"text":"Which covered populations_please_specify","changed_at":"2025-07-12T06:08:23.211Z"}', 'type': 'long_text'}, 
{'id': 'long_text_mksfzsqt', 'text': 'What are your needs - please specify', 'value': '{"text":"What are your needs - please specify","changed_at":"2025-07-12T06:08:23.212Z"}', 'type': 'long_text'}, 
{'id': 'text_mkrye90n', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'text_mkry40xt', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'text_mkryhpf0', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'long_text_mksjh7w5', 'text': '', 'value': None, 'type': 'long_text'}, 
{'id': 'text_mkryf4cd', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'text_mkryxqtf', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'text_mkry427s', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'text_mkryr3pj', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'text_mkry53df', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'text_mkryp43z', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'text_mkry581q', 'text': '', 'value': None, 'type': 'text'}, 
{'id': 'date_mkspa7vk', 'text': '2025-07-11', 'value': '{"date":"2025-07-11","changed_at":"2025-07-12T06:08:27.423Z"}', 'type': 'date'}]}

#%%
transform_monday_item(item)
# %%
