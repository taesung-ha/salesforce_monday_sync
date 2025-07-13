# salesforce_api.py
import requests
from salesforce import get_salesforce_access_token
from config import SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD

ACCESS_TOKEN, INSTANCE_URL = get_salesforce_access_token(SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD)
API_VERSION = "v59.0"

import json


def create_salesforce_lead_from_monday(data: dict):
    organization_name = data['event']['pulseName']
    column_values = data['event']['columnValues']

    # 필터: MondayForm으로부터 들어온 리드만 처리
    if column_values.get('short_textzb4g11iz', {}).get('value') != 'MondayForm':
        return {"messages": "Skipped: Not from MondayForm"}

    # Industry
    if column_values['color_mksfebkh']['label'] == 'Other':
        industry = column_values.get('text_mksfswxm', {}).get('value', 'Other')
    else:
        industry = column_values['color_mksfebkh']['label']

    # Sector
    if column_values['color_mksf6mtf']['label'] == 'Other':
        sector = column_values.get('text_mksfjsre', {}).get('value', 'Other')
    else:
        sector = column_values['color_mksf6mtf']['label']

    # WhichCoveredPopulations (dropdown_mksfe98g)
    a_labels = column_values.get('dropdown_mksfe98g', {}).get('labels', [])
    if 'Other' in a_labels:
        which_covered_populations = column_values.get('long_text_mksf3snn', {}).get('value', 'Other')
    else:
        which_covered_populations = ", ".join(a_labels)

    # WhatAreYourNeeds (dropdown_mksfyfqp)
    b_labels = column_values.get('dropdown_mksfyfqp', {}).get('labels', [])
    if 'Other' in b_labels:
        what_are_your_needs = column_values.get('long_text_mksfzsqt', {}).get('value', 'Other')
    else:
        what_are_your_needs = ", ".join(b_labels)

    # WhatIsYourEstimatedFunding (dropdown_mksf2z7p)
    c_labels = column_values.get('dropdown_mksf2z7p', {}).get('labels', [])
    if 'Other' in c_labels:
        what_is_your_estimated_funding = column_values.get('text_mksfsgjw', {}).get('value', 'Other')
    else:
        what_is_your_estimated_funding = ", ".join(c_labels)

    # WhereDidYouHear (dropdown_mksf657r)
    d_labels = column_values.get('dropdown_mksf657r', {}).get('labels', [])
    if 'Other' in d_labels:
        where_did_you_hear = column_values.get('text_mksfjtqd', {}).get('value', 'Other')
    else:
        where_did_you_hear = ", ".join(d_labels)

    # Salesforce로 보낼 payload 구성
    salesforce_payload = {
        "Name": column_values.get('text_mkrykrc2', {}).get('value', ''),
        "Website": column_values.get('text_mks821t', {}).get('value', ''),
        "Industry": industry,
        "Sector__c": sector, 
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