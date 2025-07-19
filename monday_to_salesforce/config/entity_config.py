#entity_config.py
from utils.transformer import identity, join_labels

ENTITY_CONFIG = {
    "Lead": {
        "board_id": 9378000505,
        "sf_id_column": "text_mkryhch5",  # Salesforce Lead ID 저장 컬럼
        "object_name": "Lead",
        "record_type": "0123p000000EILJAA4",  # Lead Record Type ID
        "field_mapping": {
            "text_mkry13cw": ("FirstName", "value", identity),
            "text_mkry1xy1": ("LastName", "value", identity),
            "email_mksx3vtp": ("Email", "value", identity),
            "short_textzb4g11iz": ("LeadSource", "value", identity),
            "text_mks821t": ("Website", "value", identity),
            "color_mksfebkh": ("Industry", "label", identity),
            "text_mksfswxm": ("Other_Industry__c", "value", identity),
            "color_mksf6mtf": ("Sector__c", "label", identity),
            "text_mksfjsre": ("Other_Sector__c", "value", identity),
            "text_mksf27hv": ("Title", "value", identity),
            "text_mkrym6fa": ("City", "value", identity),
            "text_mkryrr5y": ("PostalCode", "value", identity),
            "dropdown_mkstb9d4": ("State", "labels", join_labels),
            "text_mkryamt0": ("StateCode", "value", identity),
            "text_mkrym3j7": ("Country", "value", identity),
            "dropdown_mksfyfqp": ("Capacity_Building_Needs__c", "labels", join_labels),
            "long_text_mksfzsqt": ("Other_Capacity_Building_Needs__c", "value", identity),
            "dropdown_mksfe98g": ("Covered_Population__c", "labels", join_labels),
            "long_text_mksf3snn": ("OtherCoveredPopulations__c", "value", identity),
            "dropdown_mksf657r": ("Where_did_you_hear_about_CTN__c", "labels", join_labels),
            "text_mksfjtqd": ("OtherWhereDidYouHearAboutCTN__c", "value", identity),
            "color_mksf6q5r": ("WhatisYourEstimatedBudget__c", "label", identity),
            "dropdown_mksf2z7p": ("Funding__c", "labels", join_labels),
            "text_mksfsgjw": ("Other_Funding__c", "value", identity),
            "long_text_mksfhq35": ("Main_Challenges__c", "value", identity),
        }
    },

}