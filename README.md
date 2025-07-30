# 🌀 CRM Data Integration: Monday → Salesforce (Real-time Sync) + Salesforce → Monday (One-time Migration)
> A two-part CRM synchronization project using Python, PostgreSQL, AWS Lambda, RDS, GitHub Actions, and both REST & GraphQL APIs. Built to automate real-time updates from Monday.com to Salesforce and perform one-time data migration from Salesforce to Monday.com.

---
## 📚 Table of Contents

- Overview

- Tech Stack

- System Diagram

- Part I: Real-time Sync (Monday → Salesforce)

  - Flow
  - Business Logic
  - Error Handling & Logging

- Part II: One-time Migration (Salesforce → Monday)

  - Flow

- Sample Payloads

- Results & Impact

  - 💰 Cost-saving Breakdown

- Testing & Deployment

- Project Structure

- Demo

- Future Improvements

- About the Author

---

## 🧐 Overview

Originally, Salesforce was the primary CRM system. However, as a small nonprofit, the organization faced challenges with Salesforce's complexity and cost. To empower non-technical team members and enable more visual, collaborative workflows—especially for Business Development—the operational layer was migrated to Monday.com. It provided a more intuitive UI, flexible board-based structure, and better support for managing BD pipelines across stages (e.g., Follow-up → Quote → MOU).

Salesforce continues to be used as the primary backend data store, with only a minimal number of user licenses retained for API-based syncing and legacy data access.

To enable this transition and maintain system consistency, this project implemented:

Real-time Sync from Monday → Salesforce (Webhook-triggered via AWS Lambda), to reflect changes made by operations teams back into Salesforce.

One-time Migration from Salesforce → Monday (scheduled batch via GitHub Actions + GraphQL), to backfill initial data.

During this process, the project handled numerous field-level and structural mismatches between the two systems, carefully mapping and transforming data across platforms.

>💡 This real-time synchronization between Monday and Salesforce is difficult to implement even with a paid Monday Enterprise plan, and typically requires costly third-party integrations. By building the full system in-house through custom code, this project saved the organization an estimated **$7,000–$18,000** annually, while delivering reliable automation tailored to their exact business logic. It also eliminated the need for manual data entry across platforms, freeing up valuable time for the operations team and reducing human error. This represents **a major cost-saving achievement for a nonprofit organization**, where budget efficiency is especially critical.

---

## 🧰 Tech Stack
| Layer       | Tools                              |
|------------|-------------------------------------|
| Language    | Python 3.11                        |
| CRMs        | Salesforce REST API, Monday.com GraphQL & REST API|
| Infra       | AWS Lambda + VPC + RDS (PostgreSQL) |
| Monitoring  | Telegram Bot API                   |
| Deployment  | GitHub Actions Workflow (CI/CD)                     |
| Event System | Monday.com Webhooks (multiple types; `update_column_value`, `create_pulse`, `update_name`, `delete_pulse`)

---
## 🪡 System Architecture

<img width="1821" height="1778" alt="Image" src="https://github.com/user-attachments/assets/38265745-45fb-430d-bdf5-e47d868823d0" />

---
## 📦 Part I: Initial Migration (Salesforce → Monday.com)
### Batch Workflow
1. GitHub Actions schedules a weekly run.

2. Python script authenticates via OAuth and fetches Salesforce data.

3. Custom schema mapping adapts records for Monday GraphQL.

4. Batched GraphQL mutations write to Monday.com boards.

5. Execution details logged in PostgreSQL for auditability.

---


## 📦 Part II: Real-Time Synchronization (Monday.com → Salesforce)
### Event Pipeline
1. Monday webhook fires on item update, rename, creation, or deletion.

2. Payload hits AWS API Gateway and is routed to Lambda.

3. Lambda parses event type and dispatches accordingly.

4. Business logic resolves data transformation and API invocation.

4. Salesforce objects (Lead/Account/Contact/Opportunity) are updated.

5. PostgreSQL logs event metadata and response status.

6. Telegram sends alerts for critical failures.

---

## 🤖 Payload Schemas
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
## 📊 Outcome & Impact
- 🔁 Full replacement of manual syncing between CRM systems

- 🧠 Reduced 90% of weekly cognitive and operational overhead

- 🏷 Avoided subscription costs for Monday Enterprise plan & external connectors

- 🔎 Ensured lifecycle traceability of leads and deals

- 🧾 Production-grade logging enabled debugging & analytics

---
## 💰 Cost Efficiency Analysis
- Estimated savings: $7,000–$18,000 annually (licensing + integrations)

- Labor savings: Eliminated 4–6 hours/week of manual data entry

- Strategic value: Empowered non-technical users to drive BD pipeline without developer dependency

- Organizational fit: A lean, scalable automation solution designed for nonprofits operating with budget constraints

---
## 🧪 Testing & Deployment
- ✅ Unit tests written in tests/test_mapper.py

- 🔧 Local testing via ngrok + Postman

- 🚀 Deployed via GitHub Actions → AWS Lambda

- 🔐 Credentials stored in Lambda environment variables (IAM-protected)

---
## 🧭 Project Structure
```pgsql
crm-sync/
├── lambda/
│   ├── handler.py
│   ├── mapping.py
│   └── utils/
│       └── telegram.py
├── migration/
│   └── sf_to_monday.py
├── logs/
│   └── log_sample.csv
├── tests/
│   └── test_mapper.py
├── diagrams/
│   └── architecture.png
├── requirements.txt
└── README.md
```
---
## 📹 Demo
▶️ Watch the 3-min demo <br>
→ Demonstrates real-time sync, database logging, and error alerts in action.

---
## 📌 Future Improvements
- Implement bidirectional sync logic (conflict resolution)
- Add Slack integration for success alerts
- Support custom field mapping via config file
- Implement async retry mechanism for failed API calls



### ✅ Installation
```bash
# Clone the repository
git clone https://github.com/taesungha/salesforce-monday-sync.git
cd salesforce-monday-sync

# Install dependencies
pip install -r requirements.txt
```

## 🔍 Key Highlights
- ✔ **Reduced sync latency** from `60s → <10s`  
- ✔ **Automated data consistency** for `1,000+ CRM records`  
- ✔ Enabled **non-technical teams** to leverage CRM automation with zero manual intervention  

---

## 📈 Future Improvements
- [ ] Add **OAuth 2.0 token refresh** for enhanced security  
- [ ] Expand to support **custom Salesforce objects**  
- [ ] Integrate with **AWS Step Functions** for advanced orchestration  

---

## 📬 Contact
**Author:** Taesung Ha  
📧 **Email:** [taesungh@umich.edu](mailto:taesungh@umich.edu)  
🌐 **LinkedIn:** [[https://linkedin.com/in/taesungha](https://www.linkedin.com/in/tae-sung-ha-696a5b246/)](https://www.linkedin.com/in/tae-sung-ha-696a5b246/) 
