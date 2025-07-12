# salesforce_api.py
import requests
from salesforce import get_salesforce_access_token
from config import SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD

ACCESS_TOKEN, INSTANCE_URL = get_salesforce_access_token(SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD)
API_VERSION = "v59.0"

def create_salesforce_lead_from_monday(data: dict):
    organization_name = data['event']['pulseName']
    column_values = data['event']['columnValues']

    # 필터: MondayForm으로부터 들어온 리드만 처리
    if column_values.get('short_textzb4g11iz', {}).get('value') != 'MondayForm':
        return {"messages": "Skipped: Not from MondayForm"}

    # Industry
    if column_values['color_mksfebkh']['label']['text'] == 'Other':
        industry = column_values.get('text_mksfswxm', {}).get('value', 'Other')
    else:
        industry = column_values['color_mksfebkh']['label']['text']

    # Sector
    if column_values['color_mksf6mtf']['label']['text'] == 'Other':
        sector = column_values.get('text_mksfjsre', {}).get('value', 'Other')
    else:
        sector = column_values['color_mksf6mtf']['label']['text']

    # WhichCoveredPopulations (dropdown_mksfe98g)
    choices = column_values.get('dropdown_mksfe98g', {}).get('chosenValues', [])
    if any(c.get('name') == 'Other' for c in choices):
        which_covered_populations = column_values.get('long_text_mksf3snn', {}).get('text', 'Other')
    else:
        which_covered_populations = ", ".join(c.get('name', '') for c in choices)

    # WhatAreYourNeeds (dropdown_mksfyfqp)
    choices = column_values.get('dropdown_mksfyfqp', {}).get('chosenValues', [])
    if any(c.get('name') == 'Other' for c in choices):
        what_are_your_needs = column_values.get('long_text_mksfzsqt', {}).get('text', 'Other')
    else:
        what_are_your_needs = ", ".join(c.get('name', '') for c in choices)

    # WhatIsYourEstimatedFunding (dropdown_mksf2z7p)
    choices = column_values.get('dropdown_mksf2z7p', {}).get('chosenValues', [])
    if any(c.get('name') == 'Other' for c in choices):
        what_is_your_estimated_funding = column_values.get('text_mksfsgjw', {}).get('value', 'Other')
    else:
        what_is_your_estimated_funding = ", ".join(c.get('name', '') for c in choices)

    # WhereDidYouHear (dropdown_mksf657r)
    choices = column_values.get('dropdown_mksf657r', {}).get('chosenValues', [])
    if any(c.get('name') == 'Other' for c in choices):
        where_did_you_hear = column_values.get('text_mksfjtqd', {}).get('value', 'Other')
    else:
        where_did_you_hear = ", ".join(c.get('name', '') for c in choices)

    # Salesforce로 보낼 payload 구성
    salesforce_payload = {
        "Name": column_values.get('text_mkrykrc2', {}).get('value', ''),
        "Website": column_values.get('text_mks821t', {}).get('value', ''),
        "Industry": industry,
        "Sector__c": sector,  # Salesforce에 커스텀 필드로 생성 필요
        "FirstName": column_values.get('text_mkry13cw', {}).get('value', ''),
        "LastName": column_values.get('text_mkry1xy1', {}).get('value', ''),
        "Title": column_values.get('text_mksf27hv', {}).get('value', ''),
        "Email": column_values.get('text_mkrymwp3', {}).get('value', ''),
        "Phone": column_values.get('text_mkryhzq7', {}).get('value', ''),
        "City": column_values.get('text_mkrym6fa', {}).get('value', ''),
        "State": column_values.get('text_mkryz0sr', {}).get('value', ''),
        "PostalCode": column_values.get('text_mkryrr5y', {}).get('value', ''),
        "WhichCoveredPopulations__c": which_covered_populations,
        "WhatAreYourNeeds__c": what_are_your_needs,
        "WhatisYourEstimatedFunding__c": what_is_your_estimated_funding,
        "MainChallenges__c": column_values.get('long_text_mksfhq35', {}).get('text', ''),
        "WhereDidYouHear__c": where_did_you_hear,
        "LeadSource": column_values.get('short_textzb4g11iz', {}).get('value', ''),
        "Company": organization_name
    }

    url = f"{INSTANCE_URL}/services/data/{API_VERSION}/sobjects/Lead"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=salesforce_payload)

    if response.status_code == 201:
        return {"messages": "✅ Lead created successfully"}
    else:
        return {
            "message": "❌ Failed to create lead",
            "status_code": response.status_code,
            "response": response.text
        }