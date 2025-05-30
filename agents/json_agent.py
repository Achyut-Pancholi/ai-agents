import json
import os

REQUIRED_FIELDS = {
    "invoice_id": str,
    "customer_name": str,
    "items": list,
    "total_amount": (int, float)
}

def parse_json_file(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")

    anomalies = []

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in data:
            anomalies.append(f"Missing required field: {field}")
        else:
            if not isinstance(data[field], expected_type):
                anomalies.append(f"Field '{field}' has wrong type. Expected {expected_type}, got {type(data[field])}")

    result = {
        "invoice_id": data.get("invoice_id"),
        "customer_name": data.get("customer_name"),
        "items": data.get("items", []),
        "total_amount": data.get("total_amount"),
        "anomalies": anomalies,
        "is_valid": len(anomalies) == 0,
        "raw_json": data
    }
    result["has_anomaly"] = len(anomalies) > 0
    result["recommended_action"] = "RiskAlert" if result["has_anomaly"] else "RoutineLog"

    return result
