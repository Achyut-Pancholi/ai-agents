import fitz  # PyMuPDF

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

    # Basic keyword matching (customize this for your invoice structure)
    lines = text.splitlines()
    invoice_data = {
        "invoice_number": None,
        "customer_name": None,
        "total_amount": None,
        "raw_text": text[:500]  # Preview
    }

    for line in lines:
        if "invoice no" in line.lower():
            invoice_data["invoice_number"] = line.split(":")[-1].strip()
        elif "bill to" in line.lower():
            invoice_data["customer_name"] = line.split(":")[-1].strip()
        elif "total" in line.lower():
            invoice_data["total_amount"] = line.split(":")[-1].strip()

    return invoice_data
