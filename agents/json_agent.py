import json
import os

# Validate required keys in the JSON
REQUIRED_KEYS = ["invoice_id", "customer_name", "items", "total_amount"]

def parse_json_file(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")

    missing_keys = [key for key in REQUIRED_KEYS if key not in data]
    if missing_keys:
        raise ValueError(f"Missing required fields: {missing_keys}")

    return {
        "invoice_id": data["invoice_id"],
        "customer_name": data["customer_name"],
        "items": data["items"],
        "total_amount": data["total_amount"],
        "raw_json": data
    }
