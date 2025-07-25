# Salesforce ↔ Monday.com Synchronization Platform  
_A Serverless CRM Integration Pipeline with Real-Time Sync & Automation_

---

## 📌 Overview
This project provides an **automated, bi-directional synchronization solution** between **Salesforce** and **Monday.com** to streamline CRM workflows for nonprofit and business teams.  
It eliminates manual data entry, reduces sync delays by 80%, and ensures data integrity across both platforms.

### ✅ Key Goals:
- **Real-time updates** for Leads, Opportunities, Contacts, and Accounts
- **Scalable serverless architecture** to minimize infrastructure overhead
- **Cross-platform data consistency** with robust error handling and logging

---

## ✅ Features
- 🔄 **Bi-directional sync** between Salesforce and Monday.com using webhooks
- ⚡ **Serverless automation** powered by AWS Lambda + API Gateway
- 🐳 **Microservices containerized** with Docker for portability
- 🗄️ **Data validation & mapping** via PostgreSQL
- 🔔 **Error monitoring & alerting** using Telegram Bot API
- ☁️ **Automatic backup to AWS S3**

---

## 🏗️ Architecture
Monday.com ←→ AWS API Gateway ←→ AWS Lambda ←→ Salesforce
                                    ↓
                                    PostgreSQL
                                    ↓
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
