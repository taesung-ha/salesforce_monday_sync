#entity_config.py
from utils.transformer import identity, join_labels

ENTITY_CONFIG = {
    "Lead": {
        "board_id": 9378000505,
        "sf_id_column": "text_mkryhch5",  # Salesforce Lead ID 저장 컬럼
        "object_name": "Lead",
        "record_type": "0123p000000EILJAA4",  # Lead Record Type ID
        "field_mapping": {
            "color_mksj2adq": ("Status", "label", identity),
            "text_mkry13cw": ("FirstName", "value", identity),
            "text_mkry1xy1": ("LastName", "value", identity),
            "email_mksx3vtp": ("Email", "value", identity),
            "short_textzb4g11iz": ("LeadSource", "value", identity),
            "text_mks821t": ("Website", "value", identity),
            "dropdown_mkt48t9a": ("Multi_Industry__c", "labels", join_labels),
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
        },
        "link_mappings": {
            "board_relation_mksdqfg0": ("Opportunity", "Linked_Opportunity__c"),
            "board_relation_mks9cjfs": ("Account", "Linked_Account__c"),
            "board_relation_mks95q": ("Contact", "Linked_Contact__c")
        }
    },
    
    "Account": {
        "board_id": 9378000326,
        "sf_id_column": "text_mkrykpx4",  # Salesforce Account
        "object_name": "Account",
        "field_mapping": {
            "text_mkrykpx4": ("Id", "value", identity),
            "dropdown_mksjv0b6": ("Type", "labels", join_labels),
            "text_mkrycwt2": ("BillingStreet", "value", identity),
            "text_mkry84sc": ("BillingCity", "value", identity),
            "text_mkryw8sk": ("BillingState", "value", identity),
            "text_mkry7mvg": ("BillingPostalCode", "value", identity),
            "text_mkry5991": ("BillingCountry", "value", identity),
            "text_mkrypgwa": ("BillingStateCode", "value", identity),
            "text_mkryh3k": ("Phone", "value", identity),
            "text_mkrynkny": ("Website", "value", identity),
            "color_mkstk7e5": ("Industry", "label", identity),
            "long_text_mksjv61h": ("Description", "value", identity),
            "dropdown_mkt01cp2": ("Capacity_Building_Needs__c", "labels", join_labels)
        },
        
    },
    "Contact": {
        "board_id": 9429890440,
        "sf_id_column": "text_mks6ner3",
        "object_name": "Contact",
        "field_mapping": {
            "text_mks61cq2": ("FirstName", "value", identity),
            "text_mks67we5": ("LastName", "value", identity),
            "text_mks6s3rq": ("Title", "value", identity),
            "text_mks6h9j": ("Phone", "value", identity),
            "long_text_mksjsbdg": ("Description", "value", identity),
            "text_mks6hgvs": ("Veteran_Status__c", "value", identity),
            "text_mks6g6mp": ("Disability_Status__c", "value", identity),
            "dropdown_mksj5djx": ("npe01__Organization_Type__c", "labels", join_labels),
            "text_mks69r6r": ("Birthdate", "value", identity),
            "text_mks63b0a": ("MailingCity", "value", identity),
            "text_mks6p9v": ("MailingStreet", "value", identity),
            "dropdown_mkt0xrxe": ("MailingState", "labels", join_labels),
            "text_mks6rkt1": ("MailingPostalCode", "value", identity),
            "dropdown_mksjtsrc": ("npe01__Type_of_Account__c", "labels", join_labels),
            "text_mks6nck4": ("npe01__WorkPhone__c", "value", identity),
            "text_mks6bhk": ("npe01__Work_Address__c", "value", identity),
            "text_mks67a8w": ("MobilePhone", "value", identity),
            "text_mks6d5v1": ("LinkedIn__c", "value", identity),
            "text_mks6c82k": ("Email", "value", identity),
        },
        "link_mappings": {
            "board_relation_mks98dnn": ("Account", "AccountId"),
            "board_relation_mkt3d4a9": ("Account", "npsp__Primary_Affiliation__c")
        }
    },
    "Opportunity": {
        "board_id": 9378000036,
        "sf_id_column": "text_mkry20c9",
        "object_name": "Opportunity",
        "field_mapping": {
            "color_mksj6ap4": ("StageName", "label", identity),
            "dropdown_mksjwx1c": ("Type", "labels", join_labels),
            "long_text_mksjyg4z": ("Description", "value", identity),
            "numeric_mksjdntv": ("Amount", "value", identity),
            "date_mkt1abcz": ("CloseDate", "date", identity),
        },
        "link_mappings": {
            "board_relation_mks9nfzc": ("Account", "AccountId"),
            "board_relation_mksdqfg0": ("Contact", "ContactId"),
            "board_relation_mkt3dbmb": ("Contact", "npsp__Primary_Contact__c"),
            
        }
        
    }
}