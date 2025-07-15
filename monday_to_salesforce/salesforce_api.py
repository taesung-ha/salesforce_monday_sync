# salesforce_api.py
import requests
from salesforce import get_salesforce_access_token
from config import SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD
import json

API_VERSION = "v59.0"

def create_salesforce_lead_from_monday(data: dict):
    ACCESS_TOKEN, INSTANCE_URL = get_salesforce_access_token(
        SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD
    )

    organization_name = data['event']['pulseName'] #Company
    column_values = data['event']['columnValues']

    # 필터: MondayForm으로부터 들어온 리드만 처리
    if column_values.get('short_textzb4g11iz', {}).get('value') != 'MondayForm':
        return {"messages": "Skipped: Not from MondayForm"}

    # Industry
    industry = ''
    other_industry = ''
    if column_values.get('color_mksfebkh', {}).get('label') == 'Other':
        industry = 'Other'
        other_industry = column_values.get('text_mksfswxm', {}).get('value', 'Other').strip()
    else:
        industry = column_values.get('color_mksfebkh', {}).get('label').strip()

    # Sector
    sector = ''
    other_sector = ''
    if column_values.get('color_mksf6mtf', {}).get('label') == 'Other':
        sector = 'Other'
        other_sector = column_values.get('text_mksfjsre', {}).get('value', 'Other').strip()
    else:
        sector = column_values.get('color_mksf6mtf', {}).get('label').strip()

    # WhatAreYourNeeds (dropdown_mksfyfqp) -> Capacity_Building_Needs__c
    what_are_your_needs = ''
    other_what_are_your_needs = ''
    a_labels = column_values.get('dropdown_mksfyfqp', {}).get('labels', [])
    a_labels = [label.strip() for label in a_labels]
    if 'Other' in a_labels:
        if len(a_labels) == 1:
            what_are_your_needs = 'Other'
            other_what_are_your_needs = column_values.get('long_text_mksfzsqt', {}).get('value', 'Other').strip()
        else:
            what_are_your_needs = ";".join(a_labels)
            other_what_are_your_needs = column_values.get('long_text_mksfzsqt', {}).get('value', 'Other').strip()
    else:
        what_are_your_needs = ";".join(a_labels)

    # WhichCoveredPopulations (dropdown_mksfe98g) -> Covered_Population__c
    which_covered_populations = ''
    other_which_covered_populations = ''
    b_labels = column_values.get('dropdown_mksfe98g', {}).get('labels', [])
    b_labels = [label.strip() for label in b_labels]
    if 'Other' in b_labels:
        if len(b_labels) == 1:
            which_covered_populations = 'Other'
            other_which_covered_populations = column_values.get('long_text_mksf3snn', {}).get('value', 'Other').strip()
        else:
            which_covered_populations = ";".join(b_labels)
            other_which_covered_populations = column_values.get('long_text_mksf3snn', {}).get('value', 'Other').strip()
    else:
        which_covered_populations = ";".join(b_labels)

    # WhatisYourEstimatedBudget (color_mksf6q5r)
    what_is_your_estimated_budget = column_values.get('color_mksf6q5r', {}).get('label', 'Other').strip()

    # Funding Type (dropdown_mksf2z7p)
    funding_type = ''
    other_funding_type = ''
    c_labels = column_values.get('dropdown_mksf2z7p', {}).get('labels', [])
    c_labels = [label.strip() for label in c_labels]
    if 'Other' in c_labels:
        if len(c_labels) == 1:
            funding_type = 'Other'
            other_funding_type = column_values.get('text_mksfsgjw', {}).get('value', 'Other').strip()
        else:
            funding_type = ";".join(c_labels)
            other_funding_type = column_values.get('text_mksfsgjw', {}).get('value', 'Other').strip()
    else:
        funding_type = ";".join(c_labels)

    # WhereDidYouHear (dropdown_mksf657r) <- 여기부터
    where_did_you_hear = ''
    other_where_did_you_hear = ''
    d_labels = column_values.get('dropdown_mksf657r', {}).get('labels', [])
    d_labels = [label.strip() for label in d_labels]
    if 'Other' in d_labels:
        if len(d_labels) == 1:
            where_did_you_hear = 'Other'
            other_where_did_you_hear = column_values.get('text_mksfjtqd', {}).get('value', 'Other').strip()
        else:
            where_did_you_hear = ";".join(d_labels)
            other_where_did_you_hear = column_values.get('text_mksfjtqd', {}).get('value', 'Other').strip()
    else:
        where_did_you_hear = ";".join(d_labels)

    # Salesforce로 보낼 payload 구성
    salesforce_payload = {
        "RecordTypeId": "0123p000000EILJAA4",
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
        "Other_Capacity_Building_Needs__c": other_what_are_your_needs,
        "Covered_Population__c": which_covered_populations,
        "OtherCoveredPopulations__c": other_which_covered_populations,
        "WhatisYourEstimatedBudget__c": what_is_your_estimated_budget,
        "Funding__c": funding_type,
        "Other_Funding__c": other_funding_type,
        "Where_did_you_hear_about_CTN__c": where_did_you_hear,
        "OtherWhereDidYouHearAboutCTN__c": other_where_did_you_hear,
        "MainChallenges__c": column_values.get('long_text_mksfhq35', {}).get('text', ''),
    }

    url = f"{INSTANCE_URL}/services/data/{API_VERSION}/sobjects/Lead"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=salesforce_payload)
    print(json.dumps(salesforce_payload, indent=2))
    
    try:
        response_data = response.json()
    except ValueError:
        response_data = {"raw_response": response.text}
    
    if response.status_code == 201:
        lead_id = response_data.get('id', '')
        print (f"✅ Lead created successfully: {lead_id}")
        return str(lead_id), response_data

    else:
        print("❌ Salesforce lead creation failed:")
        print("Payload:", json.dumps(salesforce_payload, indent=2))
        print("Response:", response.text)
        return {
            "message": "❌ Failed to create lead",
            "status_code": response.status_code,
            "response": response.text
        }, response_data