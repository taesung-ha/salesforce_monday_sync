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

>💡 This real-time synchronization between Monday and Salesforce is difficult to implement even with a paid Monday Enterprise plan, and typically requires costly third-party integrations. By building the full system in-house through custom code, this project saved the organization an estimated **$7,000–$18,000** annually, while delivering reliable automation tailored to their exact business logic. It also eliminated the need for manual data entry across platforms, freeing up valuable time for the operations team and reducing human error. This represents a major cost-saving achievement for a nonprofit organization, where budget efficiency is especially critical.

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
```mermaid
graph TD
    subgraph Part I: Real-time (Monday → Salesforce)
    A[Monday Webhook (item update/create/delete)] --> B[API Gateway]
    B --> C[AWS Lambda]
    C --> D[Salesforce API (Lead/Account/Contact/Opportunity)]
    C --> E[PostgreSQL (logs)]
    C --> F[Telegram Notification (on error)]
    end

    subgraph Part II: One-time (Salesforce → Monday)
    G[GitHub Actions Trigger] --> H[Salesforce API (GET)]
    H --> I[Python Sync Script]
    I --> J[Monday API (GraphQL mutations)]
    I --> E
    end
```
---
## 🏗️ Architecture
Monday.com ←→ AWS API Gateway ←→ AWS Lambda ←→ Salesforce <br>
↓ <br>
PostgreSQL <br>
↓ <br>
AWS S3 (Backup)

---

## 🛠 Tech Stack
- **Languages:** Python, SQL  
- **Cloud:** AWS Lambda, API Gateway, EventBridge, S3  
- **Databases:** PostgreSQL  
- **APIs:** Salesforce REST API, Monday GraphQL API  
- **DevOps:** Docker, GitHub Actions (CI/CD)  

---

## ⚡ How It Works
1. **Webhook Trigger:**  
   - Monday.com or Salesforce sends an event → API Gateway receives the payload.
2. **Lambda Processing:**  
   - Validates and transforms data  
   - Applies mapping logic (using PostgreSQL tables)  
   - Updates corresponding system via API  
3. **Logging & Backup:**  
   - Stores sync logs in PostgreSQL  
   - Pushes backup to AWS S3  
4. **Alerting:**  
   - Errors or anomalies trigger Telegram notifications for real-time monitoring  

---

## 🚀 Getting Started

### ✅ Prerequisites
- Python 3.9+
- AWS account with Lambda & API Gateway enabled
- Docker installed
- Salesforce & Monday.com API credentials

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
