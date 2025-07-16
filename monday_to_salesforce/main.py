#%%
# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from salesforce_api import create_salesforce_lead_from_monday, update_salesforce_lead
from monday_api import get_monday_item_details, update_monday_column
from utils import log_to_db, send_telegram_alert, create_log_table
import json

app = FastAPI()

@app.on_event("startup")
def setup():
    try:
        create_log_table()
        print("Log table created successfully.")
    except Exception as e:
        print(f"Error during setup: {e}")

@app.get("/")
def root():
    return {"status": "ok"}

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
        
        log_to_db(event_type, board_id, item_id, column_id, status="received", response_data=data)

        if event_type == "create_pulse": #create_pulse 이벤트 처리
            if column_values.get('short_textzb4g11iz', {}).get('value', '') == 'MondayForm':

                item_data = get_monday_item_details(item_id, board_id)
                lead_id, response_data = create_salesforce_lead_from_monday(item_data)

                if isinstance(lead_id, str) and lead_id.startswith("00Q"): #Monday.com에 Salesforce Lead ID 업데이트
                    update_monday_column(item_id=item_id, board_id=board_id, column_id='text_mkryhch5', value=lead_id)
                    print(response_data)
                    log_to_db(event_type, board_id, item_id, column_id, status="success", response_data=response_data)
                else:
                    log_to_db(event_type, board_id, item_id, column_id, status="failed", response_data=response_data)
                    send_telegram_alert(f"❌ Failed to create lead: {item_id}")
                    return JSONResponse(content={"status": f"❌ Failed to create lead: {lead_id}"})

            else:
                print({"status": "⏩ Skipped: Not from MondayForm"})
                return JSONResponse(content={"status": "⏩ Skipped: Not from MondayForm"})

        elif event_type == "update_column_value": #update_column_value 이벤트 처리
            monday_item_details = get_monday_item_details(item_id, board_id)
            column_values = monday_item_details.get('event', {}).get('columnValues', {})
            lead_id = monday_item_details.get('event', {}).get('columnValues', {}).get('text_mkryhch5', {}).get('value', '')
            if isinstance(lead_id, str) and lead_id.startswith("00Q"):
                fields = {}
                if column_id == 'text_mkry13cw': # 'First Name' 컬럼 업데이트
                    fields = {"FirstName": column_values.get('text_mkry13cw', {}).get('value', '')}
                elif column_id == 'text_mkry1xy1': # 'Last Name' 컬럼 업데이트
                    fields = {"LastName": column_values.get('text_mkry1xy1', {}).get('value', '')}
                elif column_id == 'color_mksj2adq': # 'Status' 컬럼 업데이트
                    fields = {"Status": column_values.get('color_mksj2adq', {}).get('value', '')}
                elif column_id == 'text_mkrymwp3': # 'Email' 컬럼 업데이트
                    fields = {"Email": column_values.get('text_mkrymwp3', {}).get('value', '')}
                elif column_id == 'short_textzb4g11iz': # 'Lead Source' 컬럼 업데이트
                    fields = {"LeadSource": column_values.get('short_textzb4g11iz', {}).get('value', '')}
                elif column_id == 'text_mkryhzq7': # 'Phone' 컬럼 업데이트
                    fields = {"Phone": column_values.get('text_mkryhzq7', {}).get('value', '')}
                elif column_id == 'text_mks821t': # 'Website' 컬럼 업데이트
                    fields = {"Website": column_values.get('text_mks821t', {}).get('value', '')}
                elif column_id == 'color_mksfebkh': # 'Industry' 컬럼 업데이트
                    fields = {"Industry": column_values.get('color_mksfebkh', {}).get('value', '')}
                elif column_id == 'text_mksfswxm': # 'Industry (Please Specify)' 컬럼 업데이트
                    fields = {"Other_Industry__c": column_values.get('text_mksfswxm', {}).get('value', '')}
                elif column_id == 'color_mksf6mtf': # 'Sector' 컬럼 업데이트
                    fields = {"Sector__c": column_values.get('color_mksf6mtf', {}).get('value', '')}
                elif column_id == 'text_mksfjsre': # 'Sector (Please Specify)' 컬럼 업데이트
                    fields = {"Other_Sector__c": column_values.get('text_mksfjsre', {}).get('value', '')}
                elif column_id == 'text_mksf27hv': # 'Title' 컬럼 업데이트
                    fields = {"Title": column_values.get('text_mksf27hv', {}).get('value', '')}
                elif column_id == 'text_mkrym6fa': # 'City' 컬럼 업데이트
                    fields = {"City": column_values.get('text_mkrym6fa', {}).get('value', '')}
                elif column_id == 'text_mkryq1r8': # 'Street' 컬럼 업데이트
                    fields = {"Street": column_values.get('text_mkryq1r8', {}).get('value', '')}
                elif column_id == 'text_mkryrr5y': # 'Postal Code' 컬럼 업데이트
                    fields = {"PostalCode": column_values.get('text_mkryrr5y', {}).get('value', '')}
                elif column_id == 'dropdown_mkstb9d4': # 'State' 컬럼 업데이트
                    fields = {"State": column_values.get('dropdown_mkstb9d4', {}).get('value', '')}
                elif column_id == 'text_mkryamt0': # 'StateCode' 컬럼 업데이트
                    fields = {"StateCode": column_values.get('text_mkryamt0', {}).get('value', '')}
                elif column_id == 'text_mkrym3j7': # 'Country' 컬럼 업데이트
                    fields = {"Country": column_values.get('text_mkrym3j7', {}).get('value', '')}
                elif column_id == 'dropdown_mksfyfqp': # 'Capacity Building Needs' 컬럼 업데이트
                    a_labels = column_values.get('dropdown_mksfyfqp', {}).get('labels', [])
                    a_labels = [label.strip() for label in a_labels]
                    a_labels = ';'.join(a_labels)
                    fields = {"Capacity_Building_Needs__c": a_labels}
                elif column_id == 'long_text_mksfzsqt': # 'Other Capacity Building Needs' 컬럼 업데이트
                    fields = {"Other_Capacity_Building_Needs__c": column_values.get('long_text_mksfzsqt', {}).get('value', '')}
                elif column_id == 'dropdown_mksfe98g': # 'Covered Population' 컬럼 업데이트
                    b_labels = column_values.get('dropdown_mksfe98g', {}).get('labels', [])
                    b_labels = [label.strip() for label in b_labels]
                    b_labels = ';'.join(b_labels)
                    fields = {"Covered_Population__c": b_labels}
                elif column_id == 'long_text_mksf3snn': # 'Other Covered Populations' 컬럼 업데이트
                    fields = {"OtherCoveredPopulations__c": column_values.get('long_text_mksf3snn', {}).get('value', '')}
                elif column_id == 'dropdown_mksf657r': # 'Where Did You Hear About CTN' 컬럼 업데이트
                    d_labels = column_values.get('dropdown_mksf657r', {}).get('labels', [])
                    d_labels = [label.strip() for label in d_labels]
                    d_labels = ';'.join(d_labels)
                    fields = {"Where_did_you_hear_about_CTN__c": d_labels}
                elif column_id == 'text_mksfjtqd': # 'Other Where Did You Hear About CTN' 컬럼 업데이트
                    fields = {"OtherWhereDidYouHearAboutCTN__c": column_values.get('text_mksfjtqd', {}).get('value', '')}
                elif column_id == 'color_mksf6q5r': # 'What is Your Estimated Budget' 컬럼 업데이트
                    fields = {"WhatisYourEstimatedBudget__c": column_values.get('color_mksf6q5r', {}).get('label', '')}
                elif column_id == 'dropdown_mksf2z7p': # 'Funding Type' 컬럼 업데이트
                    e_labels = column_values.get('dropdown_mksf2z7p', {}).get('labels', [])
                    e_labels = [label.strip() for label in e_labels]
                    e_labels = ';'.join(e_labels)
                    fields = {"Funding__c": e_labels}
                elif column_id == 'text_mksfsgjw': # 'Other Funding Type'
                    fields = {"Other_Funding__c": column_values.get('text_mksfsgjw', {}).get('value', '')}
                elif column_id == 'long_text_mksfhq35': # 'Main Challenges' 컬럼 업데이트
                    fields = {"MainChallenges__c": column_values.get('long_text_mksfhq35', {}).get('text', '')}
                elif column_id == 'text_mkrye90n': # 'CountryCode' 컬럼 업데이트
                    fields = {"CountryCode": column_values.get('text_mkrye90n', {}).get('value', '')}
                elif column_id == 'text_mkryhpf0': # 'MobilePhone' 컬럼 업데이트
                    fields = {"MobilePhone": column_values.get('text_mkryhpf0', {}).get('value', '')}
                elif column_id == 'long_text_mksjh7w5': # 'Description' 컬럼 업데이트
                    fields = {"Description": column_values.get('long_text_mksjh7w5', {}).get('text', '')}
                
                if fields:
                    update_salesforce_lead(lead_id, fields)
                    print(f"✅ Updated Salesforce Lead {lead_id} with fields: {fields} successfully")
                    log_to_db(event_type, board_id, item_id, column_id, status="success", response_data={"lead_id": lead_id, "fields": fields})
                else:
                    log_to_db(event_type, board_id, item_id, column_id, status="skipped", response_data={"message": "No fields to update"})
                    print(f"Skipped updating Salesforce Lead {lead_id} - no fields to update")
            else:
                log_to_db(event_type, board_id, item_id, column_id, status="skipped", response_data={"message": "No fields to update"})
                print(f"Skipped updating Salesforce Lead {lead_id} - no fields to update")

        return JSONResponse(content={"status": "✅ Webhook received but no action taken"})

    except Exception as e:
        send_telegram_alert(f"❌ Error in webhook processing: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})
