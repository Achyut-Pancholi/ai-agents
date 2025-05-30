import fitz  # PyMuPDF

# Map variations of field labels
FIELD_KEYWORDS = {
    "invoice_number": ["invoice no", "invoice number", "inv no"],
    "customer_name": ["bill to", "customer", "client"],
    "total_amount": ["total amount", "total", "grand total"]
}

COMPLIANCE_KEYWORDS = ["gdpr", "hipaa", "fda", "regulation", "policy", "privacy", "compliance"]

def extract_text_from_pdf(file_path: str) -> str:
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error reading PDF: {e}")

def parse_pdf_invoice(file_path: str) -> dict:
    text = extract_text_from_pdf(file_path)
    lines = text.splitlines()

    invoice_data = {
        "invoice_number": None,
        "customer_name": None,
        "total_amount": None,
        "compliance_flags": [],
        "amount_flagged": False,
        "raw_text": text[:800]
    }
    if invoice_data["amount_flagged"]:
        invoice_data["action_needed"] = "FinanceAlert"
    elif invoice_data["compliance_flags"]:
        invoice_data["action_needed"] = "ComplianceFlag"
    else:
        invoice_data["action_needed"] = "RoutineLog"

    for line in lines:
        lower = line.lower()

        for field_key, keyword_list in FIELD_KEYWORDS.items():
            for keyword in keyword_list:
                if keyword in lower and ":" in line:
                    value = line.split(":")[-1].strip()
                    if field_key == "total_amount":
                        try:
                            clean_value = value.replace(",", "").replace("₹", "").replace("$", "")
                            total = float(clean_value)
                            invoice_data["total_amount"] = total
                            if total > 10000:
                                invoice_data["amount_flagged"] = True
                        except:
                            pass
                    else:
                        invoice_data[field_key] = value
                    break  # Stop checking other keywords once matched

    # Check for compliance keywords in full text
    matches = [term.upper() for term in COMPLIANCE_KEYWORDS if term in text.lower()]
    invoice_data["compliance_flags"] = matches

    return invoice_data
