import os
import json
import mimetypes

# Simple rule-based intent classifier
def detect_intent(content: str) -> str:
    content = content.lower()
    if "quotation" in content or "quote" in content:
        return "RFQ"
    elif "invoice" in content:
        return "Invoice"
    elif "complaint" in content:
        return "Complaint"
    else:
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
