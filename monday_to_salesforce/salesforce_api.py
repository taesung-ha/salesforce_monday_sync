# salesforce_api.py
import requests
from salesforce import get_salesforce_access_token
from config import SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD

ACCESS_TOKEN, INSTANCE_URL = get_salesforce_access_token(SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD)
API_VERSION = "v59.0"

import json


def create_salesforce_lead_from_monday(data: dict):
    organization_name = data['event']['pulseName'] #Company
    column_values = data['event']['columnValues']

    # 필터: MondayForm으로부터 들어온 리드만 처리
    if column_values.get('short_textzb4g11iz', {}).get('value') != 'MondayForm':
        return {"messages": "Skipped: Not from MondayForm"}

    # Industry
    industry = ''
    other_industry = ''
    if column_values['color_mksfebkh']['label'] == 'Other':
        other_industry = column_values.get('text_mksfswxm', {}).get('value', 'Other')
    else:
        industry = column_values['color_mksfebkh']['label']

    # Sector
    sector = ''
    other_sector = ''
    if column_values['color_mksf6mtf']['label'] == 'Other':
        other_sector = column_values.get('text_mksfjsre', {}).get('value', 'Other')
    else:
        sector = column_values['color_mksf6mtf']['label']

    # WhatAreYourNeeds (dropdown_mksfyfqp) -> Capacity_Building_Needs__c
    other_what_are_your_needs = ''
    what_are_your_needs = ''
    a_labels = column_values.get('dropdown_mksfyfqp', {}).get('labels', [])
    if 'Other' in a_labels:
        other_what_are_your_needs = column_values.get('long_text_mksfzsqt', {}).get('value', 'Other')
    else:
        what_are_your_needs = ";".join(a_labels)

    # WhichCoveredPopulations (dropdown_mksfe98g) -> Covered_Population__c
    other_which_covered_populations = ''
    which_covered_populations = ''
    b_labels = column_values.get('dropdown_mksfe98g', {}).get('labels', [])
    if 'Other' in b_labels:
        other_which_covered_populations = column_values.get('long_text_mksf3snn', {}).get('value', 'Other')
    else:
        which_covered_populations = ";".join(b_labels)

    # WhatisYourEstimatedBudget (color_mksf6q5r)
    what_is_your_estimated_budget = column_values.get('color_mksf6q5r', {}).get('label', 'Other')

    # Funding Type (dropdown_mksf2z7p)
    other_funding_type = ''
    funding_type = ''
    c_labels = column_values.get('dropdown_mksf2z7p', {}).get('labels', [])
    if 'Other' in c_labels:
        other_funding_type = column_values.get('text_mksfsgjw', {}).get('value', 'Other')
    else:
        funding_type = ";".join(c_labels)

    # WhereDidYouHear (dropdown_mksf657r) <- 여기부터
    d_labels = column_values.get('dropdown_mksf657r', {}).get('labels', [])
    if 'Other' in d_labels:
        where_did_you_hear = column_values.get('text_mksfjtqd', {}).get('value', 'Other')
    else:
        where_did_you_hear = ";".join(d_labels)

    # Salesforce로 보낼 payload 구성
    salesforce_payload = {
        "Company": organization_name,
        "LeadSource": column_values.get('short_textzb4g11iz', {}).get('value', ''),
        "Email": column_values.get('text_mkrymwp3', {}).get('value', ''),
        "Phone": column_values.get('text_mkryhzq7', {}).get('value', ''),
        "FirstName": column_values.get('text_mkry13cw', {}).get('value', ''),
        "LastName": column_values.get('text_mkry1xy1', {}).get('value', ''),
        "Website": column_values.get('text_mks821t', {}).get('value', ''),
        "Industry": industry,
        "Other_Industry__c": other_industry,
        "Sector__c": sector,
        "Other_Sector__c": other_sector,
        "Title": column_values.get('text_mksf27hv', {}).get('value', ''),
        "City": column_values.get('text_mkrym6fa', {}).get('value', ''),
        "State": column_values.get('text_mkryz0sr', {}).get('value', ''),
        "PostalCode": column_values.get('text_mkryrr5y', {}).get('value', ''),
        "Capacity_Building_Needs__c": what_are_your_needs,
        "WhatAreYourNeeds__c": other_what_are_your_needs,
        "Covered_Population__c": which_covered_populations,
        "WhichCoveredPopulations__c": other_which_covered_populations,
        "WhatisYourEstimatedBudget__c": what_is_your_estimated_budget,
        "Funding__c": funding_type,
        "MainChallenges__c": column_values.get('long_text_mksfhq35', {}).get('text', ''),
        "Where_did_you_hear_about_CTN__c": where_did_you_hear,

    }

    url = f"{INSTANCE_URL}/services/data/{API_VERSION}/sobjects/Lead"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=salesforce_payload)

    if response.status_code == 201:
        result = response.json()
        lead_id = result.get('id', '')
        print (f"✅ Lead created successfully: {lead_id}")
        return str(lead_id)

    else:
        return {
            "message": "❌ Failed to create lead",
            "status_code": response.status_code,
            "response": response.text
        }