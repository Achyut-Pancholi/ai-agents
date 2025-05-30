# app.py

# ==== Imports ====
from agents.classifier_agent import classify_input
from agents.email_parser_agent import parse_email
from agents.json_agent import parse_json_file
from agents.pdf_agent import parse_pdf_invoice
from memory.shared_memory import store_entry, get_all_entries
from actions.action_router import route_action

# ==== Input File Paths ====
email_file_path = "data/sample_input/sample_email.txt"
json_file_path = "data/sample_input/sample_payload.json"
pdf_file_path = "data/sample_input/sample_invoice.pdf"

# ==== PROCESS EMAIL ====
print("\n📬 Processing Email Input...")
classified_email = classify_input(email_file_path)

if classified_email["format"] == "Email":
    email_content = classified_email["content_preview"]
    parsed_email = parse_email(email_content)

    # Step 1: Trigger Action based on tone/urgency
    action_response = route_action(
        action=parsed_email["recommended_action"],
        source_type=classified_email["file_path"],
        extracted_data=parsed_email
    )

    # Step 2: Store everything in memory
    store_entry(
        source_type=classified_email["file_path"],
        format_type=classified_email["format"],
        intent=classified_email["intent"],
        extracted_data={**parsed_email, "action_triggered": action_response}
    )

    print("✅ Email processed, action triggered, and stored in memory.")
else:
    print("⚠️ Not an email. Skipping email parser.")

# ==== PROCESS JSON ====
print("\n🧾 Processing JSON Input...")
try:
    parsed_json = parse_json_file(json_file_path)

    # Optional: simulate anomaly detection logic here
    action = "RiskAlert" if parsed_json.get("has_anomaly") else "RoutineLog"

    action_response = route_action(
        action=action,
        source_type=json_file_path,
        extracted_data=parsed_json
    )

    store_entry(
        source_type=json_file_path,
        format_type="JSON",
        intent="InvoiceData",  # You can change based on classifier
        extracted_data={**parsed_json, "action_triggered": action_response}
    )

    print("✅ JSON file processed and stored in memory.")
except Exception as e:
    print(f"❌ Error processing JSON: {e}")

# ==== PROCESS PDF ====
print("\n📄 Processing PDF Input...")
try:
    parsed_pdf = parse_pdf_invoice(pdf_file_path)

    # Simulate condition: if total > 10,000 or compliance keywords present
    action = parsed_pdf.get("action_needed", "RoutineLog")

    action_response = route_action(
        action=action,
        source_type=pdf_file_path,
        extracted_data=parsed_pdf
    )

    store_entry(
        source_type=pdf_file_path,
        format_type="PDF",
        intent="Invoice",
        extracted_data={**parsed_pdf, "action_triggered": action_response}
    )

    print("✅ PDF file processed and stored in memory.")
except Exception as e:
    print(f"❌ Error processing PDF: {e}")

# ==== VIEW SHARED MEMORY ====
print("\n🧠 Shared Memory Contents:")
entries = get_all_entries()
for i, entry in enumerate(entries, start=1):
    print(f"\nEntry #{i}:")
    print(entry)
