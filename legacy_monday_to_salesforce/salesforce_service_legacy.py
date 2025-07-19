import requests
import json
from config import SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD, SF_LEAD_PARTNER_RECORDTYPE_ID
from salesforce import get_salesforce_access_token

API_VERSION = 'v59.0'

def create_salesforce_lead(monday_data: dict):
    """
    Create a Salesforce Lead from Monday.com item data.
    monday_data 구조:
    {
        "event": {
            "pulseName": "CompanyName",
            "columnValues": {
                "short_textzb4g11iz": {"value": "MondayForm"},
                "email_mksx3vtp": {"value": "test@example.com"},
                ...
            }
        }
    }
    """
    try:
        ACCESS_TOKEN, INSTANCE_URL = get_salesforce_access_token(
            SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD
        )
        
        organization_name = monday_data['event']['pulseName']  # Company
        column_values = monday_data['event']['columnValues']
        
        if column_values.get('short_textzb4g11iz', {}).get('value') != 'MondayForm':
            return None, {"messages": "Skipped: Not from MondayForm"}
        
        def cv(key): return column_values.get(key, {}).get('value', '').strip()
        def label(key): return column_values.get(key, {}).get('label', '').strip() # status -> label
        def dropdown_labels(key): # dropdown에서 labels를 가져오는 함수
            labels = column_values.get(key, {}).get('labels', [])
            return ';'.join(label.strip() for label in labels).strip()
        
        # Industry
        industry = label('color_mksfebkh')
        other_industry = cv('text_mksfswxm') if industry == 'Other' else ''
        
        # Sector
        sector = label('color_mksf6mtf')
        other_sector = cv('text_mksfjsre') if sector == 'Other' else ''
        
        # State
        state_labels = column_values.get('dropdown_mkstb9d4', {}).get('labels', [])
        state = state_labels[0].strip() if state_labels else ''
        
        # WhatAreYourNeeds (dropdown_mksfyfqp) -> Capacity_Building_Needs__c
        what_are_your_needs = dropdown_labels('dropdown_mksfyfqp')
        other_what_are_your_needs = cv('long_text_mksfzsqt') if 'Other' in what_are_your_needs else ''
        
        # WhichCoveredPopulations (dropdown_mksfe98g) -> Covered_Population__c
        which_covered_populations = dropdown_labels('dropdown_mksfe98g')
        other_which_covered_populations = cv('long_text_mksf3snn') if 'Other' in which_covered_populations else ''
        
        # WhatisYourEstimatedBudget (color_mksf6q5r) -> WhatisYourEstimatedBudget__c
        what_is_your_estimated_budget = label('color_mksf6q5r')
        
        # Funding (dropdown_mksf2z7p) -> Funding__c
        funding_type = dropdown_labels('dropdown_mksf2z7p')
        other_funding_type = cv('text_mksfsgjw') if 'Other' in funding_type else ''
        
        # WhereDidYouHearAboutCTN (dropdown_mksf657r) -> Where_did_you_hear_about_CTN__c
        where_did_you_hear = dropdown_labels('dropdown_mksf657r')
        other_where_did_you_hear = cv('text_mksfjtqd') if 'Other' in where_did_you_hear else ''
        
        salesforce_payload = {
            "RecordTypeId": SF_LEAD_PARTNER_RECORDTYPE_ID,
            "Company": organization_name,
            "LeadSource": cv('short_textzb4g11iz'),
            "Email": cv('email_mksx3vtp'),
            "FirstName": cv('text_mkry13cw'),
            "LastName": cv('text_mkry1xy1'),
            "Website": cv('text_mks821t'),
            "Industry": industry,
            "Other_Industry__c": other_industry,
            "Sector__c": sector,
            "Other_Sector__c": other_sector,
            "Title": cv('text_mksf27hv'),
            "City": cv('text_mkrym6fa'),
            "State": state,
            "PostalCode": cv('text_mkryrr5y'),
            "Capacity_Building_Needs__c": what_are_your_needs,
            "Other_Capacity_Building_Needs__c": other_what_are_your_needs,
            "Covered_Population__c": which_covered_populations,
            "OtherCoveredPopulations__c": other_which_covered_populations,
            "WhatisYourEstimatedBudget__c": what_is_your_estimated_budget,
            "Funding__c": funding_type,
            "Other_Funding__c": other_funding_type,
            "Where_did_you_hear_about_CTN__c": where_did_you_hear,
            "OtherWhereDidYouHearAboutCTN__c": other_where_did_you_hear,
            "Main_Challenges__c": cv('long_text_mksfhq35'),
        }
        
        url = f"{INSTANCE_URL}/services/data/{API_VERSION}/sobjects/Lead"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, json=salesforce_payload)
        print(json.dumps(salesforce_payload, indent=2))
        
        # API 응답 처리
        if response.status_code == 201:
            try:
                response_data = response.json()
                lead_id = response_data.get('id', '')
                print(f"✅ Lead created successfully: {lead_id}")
                return {
                    "success": True,
                    "lead_id": lead_id,
                    "data": response_data
                }
            except ValueError as e:
                print(f"❌ JSON 파싱 오류: {e}")
                return {
                    "success": False,
                    "error": "JSON 응답 파싱 실패",
                    "response_text": response.text
                }
        else:
            try:
                response_data = response.json()
            except ValueError:
                response_data = {"error": "Invalid JSON response", "text": response.text}
            
            print("❌ Salesforce lead creation failed:")
            print("Payload:", json.dumps(salesforce_payload, indent=2))
            print("Response:", response_data)
            
            return {
                "success": False,
                "error": "Lead 생성 실패",
                "status_code": response.status_code,
                "response": response_data
            }
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 네트워크 오류: {str(e)}")
        return {
            "success": False,
            "error": f"네트워크 오류: {str(e)}"
        }
    except Exception as         e:
        print(f"❌ 예상치 못한 오류: {str(e)}")
        return {
            "success": False,
            "error": f"예상치 못한 오류: {str(e)}"
        }



def update_salesforce_lead(lead_id: str, fields: dict):
    """
    Salesforce Lead 업데이트 함수
    """
    try:
        ACCESS_TOKEN, INSTANCE_URL = get_salesforce_access_token(
            SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD
        )
        
        url = f"{INSTANCE_URL}/services/data/{API_VERSION}/sobjects/Lead/{lead_id}"
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}", 
            "Content-Type": "application/json"
        }
        
        response = requests.patch(url, headers=headers, json=fields)
        
        if response.status_code == 204:
            print(f"✅ Lead {lead_id} Updated Successfully!")
            return {
                "success": True,
                "message": f"Lead {lead_id} Updated Successfully!"
            }
        else:
            try:
                error_data = response.json()
            except ValueError:
                error_data = {"error": "Invalid JSON response", "text": response.text}

            print(f"❌ Lead {lead_id} Update Failed:")
            print("Response:", error_data)
            
            return {
                "success": False,
                "error": "Lead Update Failed",
                "status_code": response.status_code,
                "response": error_data
            }
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 네트워크 오류: {str(e)}")
        return {
            "success": False,
            "error": f"네트워크 오류: {str(e)}"
        }
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {str(e)}")
        return {
            "success": False,
            "error": f"예상치 못한 오류: {str(e)}"
        }
    