[output_logs (2).json](https://github.com/user-attachments/files/20516414/output_logs.2.json)[sample_payload.json](https://github.com/user-attachments/files/20516279/sample_payload.json)
# 🤖 Multi-Format Autonomous AI System – Flowbit AI Internship Final Assessment

This project was developed as part of the final round for the **AI Agent Development Internship** at **Flowbit Private Limited**.

The system simulates a real-world autonomous AI pipeline that accepts multiple data formats, classifies them intelligently, extracts structured fields, and dynamically triggers chained actions (like escalations, alerts, and CRM updates) based on context and content.

---

## 🧠 System Components

### 1. 📂 Classifier Agent (Level-Up)
- Detects `Format`: Email / PDF / JSON
- Detects `Intent`: RFQ, Complaint, Invoice, Regulation, Fraud Risk
- Uses few-shot examples and schema-matching
- Routes to the correct agent and logs routing metadata in memory

### 2. 📧 Email Agent
- Extracts:
  - Sender
  - Request intent
  - Urgency
  - Tone (angry, polite, threatening, etc.)
- Triggers:
  - Escalate → POST `/crm/escalate`
  - Routine → Log to memory

### 3. 🔧 JSON Agent
- Parses simulated webhook data (using Faker)
- Validates required fields
- Flags anomalies (type errors, missing fields)
- If anomalies found → POST `/risk_alert`

### 4. 📄 PDF Agent
- Parses line-item invoice PDFs or policy documents using PyPDF2/Tika
- Extracts:
  - Invoice totals
  - Regulatory keywords (e.g., “GDPR”, “FDA”)
- Flags:
  - If total > 10,000 → escalate
  - If policy contains sensitive terms → alert

### 5. 🗃️ Shared Memory Module
Stores:
- Input metadata (type, source, timestamp)
- Extracted fields per agent
- Triggered actions and follow-up decisions
- Trace logs for audits

### 6. 🔁 Action Router
- Receives outputs from agents
- Makes contextual decisions
- Simulates actions via:
  - `POST /crm/escalate`
  - `POST /risk_alert`
  - `POST /log`

---

## 🔁 Sample End-to-End Flow

1. User uploads an email → Classifier tags it as `Email + Complaint`
2. Email Agent processes:
   - Sender: procurement@client.com
   - Tone: angry
   - Urgency: high
3. Action Router decides → Escalate via `/crm/escalate`
4. Memory logs all steps

---

## 🧪 Sample Inputs

- `sample_email.txt`
- `sample_invoice.pdf`
- `sample_payload.json` 

---

## 📂 Folder Structure

```
/agents
    classifier_agent.py
    email_parser_agent.py
    json_agent.py
    pdf_agent.py

/actions
    action_router.py

/data
    sample_input/
        sample_email.txt
        sample_invoice.pdf
        sample_payload.json
    sample_output/
        output_logs.json
    uploads/

/mcp
    main_controller.py

/memory
    shared_memory.py

/templates
    index.html
    memory_view.html

/utils
    file_utils.py
    intent_classifier.py

/app.py
/fastapi_app.py
/requirements.txt
/Dockerfile
/.gitignore
/README.md

```

---

🌐 Web UI Details
This project includes a simple web frontend built with Jinja2 and served via FastAPI, allowing users to upload files and review agent activity.

📄 Web Pages
index.html: File upload UI with links to Swagger, memory logs, and output download

memory_view.html: Visualizes shared memory entries (timestamp, format, intent, extracted fields)

🧭 How to Use the Web UI
🔧 Run Locally:

git clone https://github.com/Achyut-Pancholi/ai-agents.git

pip install -r requirements.txt
🚀 Launch Server:

python -m uvicorn fastapi_app:app --reload

🌐 Access Web Page:
Open your browser and go to http://localhost:8000

You'll see the upload page. You can:

Upload .pdf, .json, or .txt (email) files

View extracted memory at /view-memory

Download the log file at /export/

See API docs at /docs



## 🎥 Demo Video


---

## 🧱 Tech Stack

- Python 3.10+
- FastAPI
- Redis
- PyPDF2 / Tika
- Faker (for test data)
- LangChain / OpenAI (optional for tone/intent)
- Docker (optional)
- HTML
---

## 🖼️ Diagram of Agent Flow

Agent Flow Diagram.jpg


---

## 📸 Screenshots


- Input files :- 
  sample_email.txt : ![image](https://github.com/user-attachments/assets/812fab77-787d-4862-81d0-0420c50b994c)
  sample_invoice.pdf : [sample_invoice.pdf](https://github.com/user-attachments/files/20516276/sample_invoice.pdf)
  sample_payload.json : [Uploading sample_payload.json…]{
  "invoice_id": "INV-1001",
  "customer_name": "Alice Smith",
  "items": [
    { "name": "HP Laptop", "quantity": 2, "price": 60000 },
    { "name": "Mouse", "quantity": 2, "price": 500 }
  ],
  "total_amount": 121000
}
()

- website screen shots
![Screenshot 2025-05-30 122351](https://github.com/user-attachments/assets/be023ed5-d3e7-44bd-8012-d4ef86e280f5)
![Screenshot 2025-05-30 122416](https://github.com/user-attachments/assets/6be31ba7-8884-4ec4-861d-d85e1ac32e65)
![Screenshot 2025-05-30 122446](https://github.com/user-attachments/assets/6a22eb79-c7c2-4b30-b8fd-9ef45f769fa1)


- Output Log 
---[Uploading output_l[
    {
        "timestamp": "2025-05-30 12:24:20",
        "source_type": "data/uploads\\e5df7275-53bc-4fa0-81c1-fdd6b0241215_sample_email.txt",
        "format": "Email",
        "intent": "RFQ",
        "data": {
            "sender_email": "john@example.com",
            "sender_name": "John Doe",
            "urgency": "Normal",
            "tone": "Polite",
            "recommended_action": "RoutineLog",
            "raw_content": "From: john@example.com\nSubject: Request for Quotation\n\nHi Team,\n\nPlease share a quotation for 20 HP laptops with extended warranty.\n\nRegards,\nJohn Doe"
        }
    },
    {
        "timestamp": "2025-05-30 12:24:25",
        "source_type": "data/uploads\\9c32bb06-e23d-444b-bd20-c471ae4514f5_sample_invoice.pdf",
        "format": "PDF",
        "intent": "Invoice",
        "data": {
            "invoice_number": "INV-2025-001",
            "customer_name": "Achyut Kumar",
            "total_amount": 11500.0,
            "compliance_flags": [
                "GDPR"
            ],
            "amount_flagged": true,
            "raw_text": "Invoice Number : INV-2025-001 \nBill To: Achyut Kumar \nTotal Amount: \u20b911,500 \nMentions: \u201cGDPR\u201d",
            "action_needed": "RoutineLog"
        }
    },
    {
        "timestamp": "2025-05-30 12:24:29",
        "source_type": "data/uploads\\74b0818b-8ddc-43b9-a2e5-1b33b05d2e48_sample_payload.json",
        "format": "JSON",
        "intent": "Invoice",
        "data": {
            "invoice_id": "INV-1001",
            "customer_name": "Alice Smith",
            "items": [
                {
                    "name": "HP Laptop",
                    "quantity": 2,
                    "price": 60000
                },
                {
                    "name": "Mouse",
                    "quantity": 2,
                    "price": 500
                }
            ],
            "total_amount": 121000,
            "anomalies": [],
            "is_valid": true,
            "raw_json": {
                "invoice_id": "INV-1001",
                "customer_name": "Alice Smith",
                "items": [
                    {
                        "name": "HP Laptop",
                        "quantity": 2,
                        "price": 60000
                    },
                    {
                        "name": "Mouse",
                        "quantity": 2,
                        "price": 500
                    }
                ],
                "total_amount": 121000
            },
            "has_anomaly": false,
            "recommended_action": "RoutineLog"
        }
    }
]ogs .json…]()




## 🙌 Acknowledgements

Thanks to **Flowbit AI** for this exciting challenge. It sharpened my understanding of real-world agent orchestration and contextual AI workflows.

---

## 📫 Contact

**Achyut Pancholi**  
📧 achyutpancholi21@gmail.com  
🌐 [LinkedIn](https://www.linkedin.com/in/achyut-pancholi)
