import os
import json
import mimetypes

# Simple rule-based intent classifier
# --- agents/classifier_agent.py ---

def detect_intent(content: str) -> str:
    content = content.lower()

    # Define intent keyword mappings
    intent_keywords = {
        "RFQ": ["quotation", "quote request", "rfq", "pricing"],
        "Invoice": ["invoice", "payment due", "billing", "billed amount"],
        "Complaint": ["not working", "complaint", "unhappy", "frustrated", "issue", "angry", "problem"],
        "Regulation": ["gdpr", "hipaa", "compliance", "data privacy", "regulation", "policy"],
        "Fraud Risk": ["unauthorized", "suspicious", "fraud", "breach", "hack", "leak"]
    }

    for intent, keywords in intent_keywords.items():
        for keyword in keywords:
            if keyword in content:
                return intent

    return "General"


# Detect format based on file extension or content type
def detect_format(file_path: str) -> str:
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == '.pdf':
        return "PDF"
    elif ext == '.json':
        return "JSON"
    elif ext == '.txt':
        return "Email"
    else:
        mime, _ = mimetypes.guess_type(file_path)
        return mime or "Unknown"

# Main classification function
def classify_input(file_path: str) -> dict:
    format_type = detect_format(file_path)
    intent_type = "Unknown"
    content = ""

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            intent_type = detect_intent(content)
    except:
        intent_type = "Invoice" if format_type == "PDF" else "Unknown"

    return {
        "file_path": file_path,
        "format": format_type,
        "intent": intent_type,
        "content_preview": content[:200]  # Optional: for debug/logging
    }
