import time

# Simulate a REST API call
def post_to_endpoint(endpoint: str, payload: dict):
    print(f"\n🚀 Simulated POST to {endpoint}")
    print("📦 Payload:")
    print(payload)

    # Simulate response
    response = {
        "status": "success",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "endpoint": endpoint
    }
    return response

# Main router function to decide action
def route_action(action: str, source_type: str, extracted_data: dict):
    payload = {
        "source": source_type,
        "data": extracted_data
    }

    if action == "Escalate":
        return post_to_endpoint("/crm/escalate", payload)
    elif action == "RoutineLog":
        return post_to_endpoint("/crm/log", payload)
    elif action == "RiskAlert":
        return post_to_endpoint("/risk_alert", payload)
    elif action == "ComplianceFlag":
        return post_to_endpoint("/compliance_flag", payload)
    elif action == "FinanceAlert":
        return post_to_endpoint("/finance_alert", payload)
    else:
        print(f"⚠️ Unknown action: {action}")
        return {"status": "failed", "reason": "Unknown action"}
