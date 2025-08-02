# CRM Data Integration: Monday → Salesforce (Real-time Sync) + Salesforce → Monday (One-time Migration)
> A two-part end-to-end CRM synchronization project using Python, PostgreSQL, Docker, AWS Lambda, RDS, GitHub Actions, and both REST & GraphQL APIs. Built to automate real-time updates from Monday.com to Salesforce and perform one-time data migration from Salesforce to Monday.com.

---
## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Part I: Initial Migration (`salesforce_to_monday`)](#part-i-initial-migration-salesforce_to_monday)
  - [Batch Workflow](#batch-workflow)
  - [Codebase Summary](#codebase-summary)
  - [Sample Code (Updating Monday's column value)](#sample-code-updating-mondays-column-value)
- [Part II: Real-Time Synchronization (`monday_to_salesforce`)](#part-ii-real-time-synchronization-monday_to_salesforce)
  - [Event Pipeline](#event-pipeline)
  - [Domain Logic](#domain-logic)
  - [Codebase Summary](#codebase-summary-1)
  - [Observability](#observability)
  - [Sample Code (Updating Salesforce's column value)](#sample-code-updating-salesforces-column-value)
- [Payload Schemas](#payload-schemas)
  - [Monday → Salesforce](#monday--salesforce)
  - [Salesforce → Monday.com](#salesforce--mondaycom)
- [Outcome & Impact](#outcome--impact)
- [Project Structure](#project-structure)
- [Demo](#demo)
- [Future Improvements](#future-improvements)
- [Key Highlights](#key-highlights)
- [Future Improvements](#future-improvements)
- [Contact](#contact)

---

## Overview

Originally, Salesforce was the primary CRM system. However, as a small nonprofit, the organization faced challenges with Salesforce's complexity and cost. To empower non-technical team members and enable more visual, collaborative workflows—especially for Business Development—the operational layer was migrated to Monday.com. It provided a more intuitive UI, flexible board-based structure, and better support for managing BD pipelines across stages (e.g., Follow-up → Quote → MOU).

Salesforce continues to be used as the primary backend data store, with only a minimal number of user licenses retained for API-based syncing and legacy data access.

To enable this transition and maintain system consistency, this project implemented:

1. **Real-Time Synchronization (Monday → Salesforce)**: Triggered via webhooks, this module used AWS Lambda and API Gateway to reflect user-driven changes from Monday.com back into Salesforce.

2. **Batch Data Migration (Salesforce → Monday.com)**: Deployed via GitHub Actions, this component batch-transferred historical data using Salesforce REST APIs and Monday GraphQL mutations.
During this process, the project handled numerous field-level and structural mismatches between the two systems, carefully mapping and transforming data across platforms.

>💡 This real-time synchronization between Monday and Salesforce is difficult to implement even with a paid Monday Enterprise plan, and typically requires costly third-party integrations. By building the full system in-house through custom code, this project saved the organization an estimated **$7,000–$18,000** annually, while delivering reliable automation tailored to their exact business logic. It also eliminated the need for manual data entry across platforms, freeing up valuable time for the operations team and reducing human error. This represents **a major cost-saving achievement for a nonprofit organization**, where budget efficiency is especially critical.

---

## Tech Stack
| Layer       | Tools                              |
|------------|-------------------------------------|
| Language    | Python 3.11                        |
| CRMs        | Salesforce REST API, Monday.com GraphQL & REST API|
| Infra (Serverless)       | AWS Lambda + API Gateway + VPC + RDS (PostgreSQL) |
| Automation | GitHub Actions (batch jobs & CI/CD pipelines) |
| Containerization | Docker |
| Monitoring  | Telegram Bot API (error notification)                 |
| Event Triggers | Monday.com Webhooks (multiple types; `update_column_value`, `create_pulse`, `update_name`, `delete_pulse`)

---
## System Architecture

<img width="1821" height="1778" alt="Image" src="https://github.com/user-attachments/assets/e1f42793-eae8-410a-8a12-881d800eb9c5" />

---
## Part I: Initial Migration (`salesforce_to_monday`)
### Batch Workflow
1. GitHub Actions schedules a weekly run.

2. Python script authenticates via OAuth and fetches Salesforce data.

3. Custom schema mapping adapts records for Monday GraphQL.

4. Batched GraphQL mutations write to Monday.com boards.

5. Execution details logged in PostgreSQL for auditability.

### Codebase Summary

- The [`mapping_config`](https://github.com/taesung-ha/salesforce_monday_sync/tree/main/salesforce_to_monday/mapping_config) directory documents detailed field correspondence between Salesforce objects and Monday.com board columns.

- [`salesforce.py`](https://github.com/taesung-ha/salesforce_monday_sync/blob/main/salesforce_to_monday/salesforce.py) manages OAuth authentication and data retrieval via Salesforce REST API.

- [`monday.py`](https://github.com/taesung-ha/salesforce_monday_sync/blob/main/salesforce_to_monday/monday.py) handles board data extraction and update through Monday’s GraphQL interface. It compares fetched data and conditionally triggers create/update logic.

- [`main.py`](https://github.com/taesung-ha/salesforce_monday_sync/blob/main/salesforce_to_monday/main.py), [`sync.py`](https://github.com/taesung-ha/salesforce_monday_sync/blob/main/salesforce_to_monday/sync.py), [`sync_account`](https://github.com/taesung-ha/salesforce_monday_sync/blob/main/salesforce_to_monday/sync_account.py), [`sync_utils`](https://github.com/taesung-ha/salesforce_monday_sync/blob/main/salesforce_to_monday/sync_utils.py) orchestrates both modules, performing unified synchronization logic across all CRM entities.

- [`monday_board_connecting.py`](https://github.com/taesung-ha/salesforce_monday_sync/blob/main/salesforce_to_monday/monday_board_connecting.py) reconstructs inter-object relational links (e.g., Lead → Opportunity → Account) in Monday boards to mirror Salesforce's native relationships.

This robust pipeline accounts for object hierarchies, field naming discrepancies, and required data transformations, dramatically reducing historical data inconsistency and sync errors.

### Sample Code (Updating Monday's column value)
```python
#monday.py
import json
def create_or_update_monday_item(record, monday_items, monday_board_id, monday_token, field_mapping):
    import requests
    salesforce_id = record.get("Id")
    if not salesforce_id:
        return

    if monday_board_id == "9378000505":
        item_name = record.get('Company')
    else:
        item_name = record.get('Name') or f"{record.get('FirstName', '')} {record.get('LastName', '')}".strip()

    # Step 1: Process desired column values
    column_values = {} 
    for monday_col_id, sf_field in field_mapping.items():
        value = record.get(sf_field, "") 
        
        if salesforce_id in monday_items: 
            col_type = monday_items[salesforce_id]["column_values"].get(monday_col_id, {}).get("type", "text") 
        else:
            col_type = "text"
            
        if col_type == "dropdown":
            if isinstance(value, str):
                split_labels = [v.strip() for v in value.split(';')]
                split_labels = [DROPDOWN_VALUE_MAP.get(v.strip(), v.strip()) for v in split_labels]
                column_values[monday_col_id] = {"labels": split_labels}
            elif isinstance(value, list):
                mapped_list = [DROPDOWN_VALUE_MAP.get(v.strip(), v.strip()) for v in value]
                column_values[monday_col_id] = {"labels": mapped_list}
            else:
                column_values[monday_col_id] = {"labels": []}
        else:
            column_values[monday_col_id] = format_value_for_column(value, col_type)
        
    # Step 2: Create
    if salesforce_id not in monday_items:
        query = '''
        mutation ($boardId: ID!, $itemName: String!, $columnValues: JSON!) {
            create_item (board_id: $boardId, item_name: $itemName, column_values: $columnValues) {
                id
            }
        }
        '''
        variables = {
            "boardId": monday_board_id,
            "itemName": item_name,
            "columnValues": json.dumps(column_values)
        }

        r = requests.post(MONDAY_API_URL, headers={"Authorization": monday_token}, json={"query": query, "variables": variables})
        response = r.json()
        if "errors" in response:
            print(f"Failed to create item: {item_name}")
            print(response["errors"])
        else:
            print(f"Created: {item_name}", flush=True)
        return

    # Step 3: Update
    current = monday_items[salesforce_id]['column_values']
    change_log = []
    updated = {}
    
    for k, v in column_values.items(): 
        current_val = current.get(k, {}).get("value")
        
        if is_same_value(current_val, v):
            continue
        else:
            updated[k] = v
            change_log.append(f"    - {k}: {current_val} → {v}")

    if updated:
        query = '''
        mutation ($itemId: ID!, $boardId: ID!, $columnValues: JSON!) {
            change_multiple_column_values(item_id: $itemId, board_id: $boardId, column_values: $columnValues) {
                id
            }
        }
        '''
        variables = {
            "itemId": monday_items[salesforce_id]['item_id'],
            "boardId": monday_board_id,
            "columnValues": json.dumps(updated)
        }
        r = requests.post(MONDAY_API_URL, headers={"Authorization": monday_token}, json={"query": query, "variables": variables})
        response = r.json()
        if "errors" in response or "data" not in response:
            print(f"Update error for {item_name}")
            print(json.dumps(response.get("errors", {}), indent=2))
            
        else:
            updated_fields = ', '.join(updated.keys())
            print(f"Updated: {item_name}", flush=True)
            for line in change_log:
                print(line, flush=True)
                
    else:
        print(f"Skipped (no change): {item_name}", flush=True)
```

---  

## Part II: Real-Time Synchronization (`monday_to_salesforce`)
### Event Pipeline
1. Monday webhook fires on item update, rename, creation, or deletion.

2. Payload hits AWS API Gateway and is routed to Lambda.

3. Lambda parses `event` type and dispatches accordingly.

4. Business logic resolves data transformation and API invocation.

4. Salesforce objects (Lead/Account/Contact/Opportunity) are updated.

5. PostgreSQL logs event metadata and response status.

6. Telegram sends alerts for critical failures.

### Domain Logic
#### Lead Lifecycle (Qualified → Deal Progression):
- Trigger: Website form populates a new lead row on Monday.com.
- Manager Verification: Valid leads are tagged as "Qualified".
- Action:
  -  Create or Update Salesforce Lead
  - Instantiate associated Account, Contact, and Opportunity.
- Sync Back:
  - Status changes (e.g., "Follow-up", "Quote", "MOU") propagate to corresponding Salesforce Opportunity stage. 

> This unified pipeline ensures CRM integrity across departments without requiring dual entry.

### Codebase Summary
- **[`services/`](https://github.com/taesung-ha/salesforce_monday_sync/tree/main/monday_to_salesforce/services)**

   - [`salesforce_services.py`](https://github.com/taesung-ha/salesforce_monday_sync/blob/main/monday_to_salesforce/services/salesforce_service.py): Handles authentication and CRUD operations for Salesforce.

   - [`monday_services.py`](https://github.com/taesung-ha/salesforce_monday_sync/blob/main/monday_to_salesforce/services/monday_service.py): Handles Monday GraphQL operations and integrates new Salesforce IDs.

   - [`mapping_service.py`](https://github.com/taesung-ha/salesforce_monday_sync/blob/main/monday_to_salesforce/services/mapping_service.py): Maintains mapping tables of Monday item IDs and Salesforce IDs.

   - [`log_service.py`](https://github.com/taesung-ha/salesforce_monday_sync/blob/main/monday_to_salesforce/services/log_service.py): Stores webhook logs into PostgreSQL.

- **[`handlers/entity_handler.py`](https://github.com/taesung-ha/salesforce_monday_sync/blob/main/monday_to_salesforce/handlers/entity_handler.py)**

   - Contains Lambda logic per event type, calling appropriate service logic per CRUD scenario.

- **[`main.py`](https://github.com/taesung-ha/salesforce_monday_sync/blob/main/monday_to_salesforce/main.py)**

  - Main entry point for Lambda. Routes incoming Monday webhooks to the corresponding handler.

- **[`utils/transformer.py`](https://github.com/taesung-ha/salesforce_monday_sync/blob/main/monday_to_salesforce/utils/transformer.py)**

  - Helper functions reused across modules.

### Observability
- Logs written to `item_sf_mapping` and `webhook_logs` tables in PostgreSQL  
<img width="1512" height="1200" alt="Image" src="https://github.com/user-attachments/assets/38afdeba-b99f-4c1d-a2c7-e236695809fe" />  
<img width="2282" height="1246" alt="Image" src="https://github.com/user-attachments/assets/a0cb3ec4-5ffb-487c-88b0-3f7e4534fb17" />

- Error-level events trigger Telegram messages via bot API  
![Image](https://github.com/user-attachments/assets/0f0d597e-5361-47ef-8681-e587083f8da5)
- Includes context such as pulseId, object ID, error trace



### Sample Code (Updating Salesforce's Column Value)
```python
#entity_handler.py
from config.entity_config import ENTITY_CONFIG
from services.monday_service import get_monday_item_details, update_monday_column
from services.salesforce_service import update_salesforce_record, create_salesforce_record, delete_salesforce_record
from services.log_service import log_to_db, send_telegram_alert
from services.mapping_service import save_mapping, get_sf_id, delete_mapping
from utils.transformer import split_name, get_added_and_removed_ids
from datetime import datetime, timezone, timedelta

async def handle_update_column(event, entity_type):
    config = ENTITY_CONFIG[entity_type]
    board_id = event.get("boardId")
    item_id = event.get("pulseId")
    column_id = event.get("columnId")

    # fetch monday.com item details
    item_data = get_monday_item_details(item_id, board_id)
    column_values = item_data.get("event", {}).get("columnValues", {})
    sf_id = column_values.get(config["sf_id_column"], {}).get("value", "")

    if not sf_id:
        log_to_db("update_column_value", board_id, item_id, column_id, "skipped",
                  response_data={"msg": "No Salesforce ID"})
        
        print(f"Skipped: No Salesforce ID for item {item_id} on board {board_id}")
        return {"status": "Skipped: No Salesforce ID"}

    # Check column mapping
    if column_id in config["field_mapping"]:
        sf_field, value_key, transform_fn = config["field_mapping"][column_id]
        col_data = column_values.get(column_id, {})
    
        if isinstance(col_data, (int, float)):
            value = col_data
        else:
            raw_value = col_data.get(value_key, "")
            value = transform_fn(raw_value) if transform_fn else raw_value

        success = update_salesforce_record(config["object_name"], sf_id, {sf_field: value})
        log_to_db("update_column_value", board_id, item_id, column_id,
                    "success" if success else "failed",
                    response_data={"sf_id": sf_id, "field": sf_field, "value": value})
        print(f"Updated {sf_field} for {entity_type} {sf_id}, Updated value: {value}")
        return {"status": f"Updated {sf_field} for {entity_type} {sf_id}, Updated value: {value}"}
    
    log_to_db("update_column_value", board_id, item_id, column_id, "skipped",
              response_data={"msg": f"No mapping for column {column_id}"})
    
    print(f"Skipped: No mapping for column {column_id} in {entity_type}")
    return {"status": "Skipped: No mapping for this column"}

```

---


## Payload Schemas
### Monday → Salesforce
```json
{
  "event": {
    "app": "monday",
    "type": "update_column_value",
    "triggerTime": "2025-07-24T09:12:56.368Z",
    "subscriptionId": "*****",
    "isRetry": false,
    "userId": "*****",
    "originalTriggerUuid": null,
    "boardId": "*****",
    "groupId": "*****",
    "pulseId": "*****",
    "pulseName": "*****",
    "columnId": "*****",
    "columnType": "text",
    "columnTitle": "*****",
    "value": {
      "value": "Data Engineer"
    },
    "previousValue": {
      "value": "Applied Statistics Student"
    },
    "changedAt": "*****",
    "isTopGroup": true,
    "triggerUuid": "*****"
  }
}

```

### Salesforce → Monday.com
```json
{
  "attributes": {
    "type": "Lead",
    "url": "/services/data/v58.0/sobjects/Opportunity/REDACTED_OPPORTUNITY_ID"
  },
  "Id": "REDACTED_Lead_ID",
  "Name": "REDACTED_LEAD_NAME"
}
```
---
### Outcome & Impact

The CRM migration from Salesforce to Monday.com catalyzed a strategic transformation in business development (BD) operations. By shifting to Monday.com’s lightweight, intuitive UI, frontline staff with limited technical expertise could now manage BD workflows more autonomously and collaboratively. This transition significantly lowered the operational barrier imposed by Salesforce’s complex interface.

However, because Monday.com lacks the database robustness of Salesforce, a full migration of historical CRM data was impractical. Therefore, the system was designed to preserve Salesforce as the authoritative backend while relocating only active, workflow-relevant BD data to Monday.com. This necessitated a real-time synchronization system—ensuring operational agility without sacrificing data integrity.

Notably, even a Monday.com Enterprise plan does not natively support full bidirectional CRM synchronization with Salesforce. Most organizations resort to expensive third-party tools like Integromat, Tray.io, or Zapier, which offer limited customization and cost anywhere from $7,000–$18,000 annually, depending on volume and use cases. This project replaced that dependency entirely with an in-house, developer-built pipeline tailored to the organization's exact BD lifecycle.

The business impact was substantial:

- Replaced fragmented, error-prone manual data entry across systems with automated synchronization.

- Saved 4–6 hours of weekly manual syncing labor, reducing operational and cognitive burden by over 90%.

- Avoided $7,000–$18,000/year in software licensing and integration costs.

- Enabled non-technical teams to manage BD operations without reliance on developers or Salesforce administrators.

- Ensured deal lifecycle traceability, with Salesforce retaining canonical records while Monday offered a fluid operational interface.

- Implemented production-grade observability (logging, error alerts) for robust auditability and debugging.

- Achieved a scalable, budget-conscious CRM automation model, aligned with the lean and resource-constrained nature of nonprofit environments.

- By building this from the ground up using Python, AWS Lambda, GraphQL, and PostgreSQL, the system delivered not only cost efficiency but also long-term maintainability and strategic autonomy. For nonprofits, where every dollar and hour saved directly impacts mission delivery, this integration offered both tactical relief and operational transformation.

---
## Project Structure
```python
# For brevity, only the core components essential to the synchronization logic are listed below.

salesforce_monday_sync/
├── monday_to_salesforce/
│   ├── Dependencies
│   ├── config
│   │    └── config.py
│   │    └── entity_config.py
│   ├── handlers
│   │    └── entity_handler.py
│   ├── services/
│   │    └── log_service.py
│   │    └── mapping_service.py
│   │    └── monday_service.py
│   │    └── salesforce_service.py
│   ├── dat_migration.py
│   ├── main.py
│   └── requirements.txt
├── salesforce_to_monday/
│   ├── mapping_config
│   │   └── account.json
│   │   └── contact.json
│   │   └── lead.json
│   │   └── opportunity.json
│   ├── config.py
│   ├── main.py
│   ├── monday.py
│   ├── monday_board_connecting.py
│   ├── salesforce.py
│   ├── sync.py
│   ├── sync_account.py
│   ├── sync_utils.py
│   └── requirements.txt
└── README.md
```
---
## Demo
[Watch the 7-min demo](https://www.youtube.com/watch?v=xHnaaww_K10)
→ Demonstrates the real-time synchronization.

---
## Future Improvements
- Implement bidirectional sync logic (conflict resolution)
- Add Slack integration for success alerts
- Support custom field mapping via config file
- Implement async retry mechanism for failed API calls

---

## Key Highlights
- **Reduced sync latency** from `60s → <10s`  
- **Automated data consistency** for `1,000+ CRM records`  
- Enabled **non-technical teams** to leverage CRM automation with zero manual intervention  

---

## Future Improvements
- [ ] Add **OAuth 2.0 token refresh** for enhanced security  
- [ ] Expand to support **custom Salesforce objects**  
- [ ] Integrate with **AWS Step Functions** for advanced orchestration  

---

## Contact
**Author:** Tae Sung Ha  
**Email:** [taesungh@umich.edu](mailto:taesungh@umich.edu)  
**LinkedIn:** [[https://linkedin.com/in/taesungha](https://www.linkedin.com/in/tae-sung-ha-696a5b246/)](https://www.linkedin.com/in/tae-sung-ha-696a5b246/) 
