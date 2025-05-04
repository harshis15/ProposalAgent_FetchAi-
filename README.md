
# 🤖 Autonomous RFQ Analyzer Agents (Multi-Agent System)

This repository contains a fully autonomous multi-agent system built using the [uAgents framework](https://github.com/fetchai/uAgents). The system simulates the end-to-end flow of receiving, analyzing, emailing, and transacting RFQ (Request for Quotation) documents using intelligent agents.

---

## 🧠 System Overview

### 🔄 Workflow Summary

1. `test_agent` or `useragent` submits an RFQ.
2. `asi1_risk_summarizer` analyzes it using the ASI1 AI API.
3. The summary is returned to the user and also sent to `proposal_generator`.
4. The `proposal_generator` emails the summary to the user.
5. Upon successful email delivery, `transact_ai_agent` logs a simulated transaction.

---

## 📂 Agents Included

### 1. `useragent` – 💬 RFQ Client Interface
- Sends RFQ queries.
- Receives AI-generated summaries.
- Initiates communication with server agent.

### 2. `asi1_risk_summarizer` – 🧠 AI RFQ Analyzer
- Analyzes RFQs using the ASI1 API.
- Extracts key details and flags.
- Sends summary to user and email agent.

### 3. `proposal_generator` – ✉️ Email Sender
- Emails the summarized quote to the user.
- Notifies the `useragent` of status.
- Triggers the transaction agent.

### 4. `transact_ai_agent` – 💳 Transaction Simulator
- Logs and confirms transactions after quote delivery.
- Generates a timestamped transaction ID.

### 5. `test_agent` – 🧪 Pipeline Trigger
- Simulates a user sending a sample RFQ for demonstration purposes.

---

## 🧩 Message Models

| Model               | Purpose                                               |
|--------------------|-------------------------------------------------------|
| `ASI1Query`         | Carries RFQ text to the AI analyzer                   |
| `ASI1Response`      | Contains the AI-generated summary                     |
| `QuoteEmailRequest` | Email content for delivery                            |
| `TransactionRequest`| Request to trigger transaction simulation             |
| `TransactionStatus` | Acknowledgment from the transaction agent             |

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/rfq-analyzer-agents.git
cd rfq-analyzer-agents
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Run Agents in Separate Terminals
```bash
python serveragent.py
python emailagent.py
python transactaiagent.py
python useragent.py 
python testagent.py
```

---

## 📧 Sample Email Output
```
Subject: Your Quote Summary from RFQ Analyzer

Hello,

Please find below the summarized RFQ and estimated quote:

<summary>

Estimated Price: $1500 USD
Quote ID: Q-4321

Thank you,
ASI1 Quote Bot
```

---

## 🙏 Acknowledgments

- [uAgents Framework](https://github.com/fetchai/uAgents)
- [ASI1 AI API](https://asi1.ai)
- [AgentVerse Platform](https://agentverse.ai)

---
