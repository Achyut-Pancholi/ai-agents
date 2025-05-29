import re

# Extract sender email using regex
def extract_sender_email(content: str) -> str:
    match = re.search(r"From:\s*(\S+@\S+)", content, re.IGNORECASE)
    return match.group(1) if match else "unknown@example.com"

# Extract sender name (usually at the end of email)
def extract_sender_name(content: str) -> str:
    lines = content.strip().splitlines()
    for i in reversed(range(len(lines))):
        if lines[i].strip() and not lines[i].strip().startswith("Regards") and lines[i-1].strip().lower() == "regards,":
            return lines[i].strip()
    return "Unknown"

# Guess urgency based on keywords
def detect_urgency(content: str) -> str:
    content = content.lower()
    if "urgent" in content or "asap" in content or "immediately" in content:
        return "High"
    elif "soon" in content or "at your earliest" in content:
        return "Medium"
    else:
        return "Normal"

# Extract conversation ID if available (example placeholder)
def extract_conversation_id(content: str) -> str:
    match = re.search(r"Conversation-ID:\s*(\S+)", content, re.IGNORECASE)
    return match.group(1) if match else None

# Main parsing function
def parse_email(content: str) -> dict:
    return {
        "sender_email": extract_sender_email(content),
        "sender_name": extract_sender_name(content),
        "urgency": detect_urgency(content),
        "conversation_id": extract_conversation_id(content),
        "raw_content": content.strip()
    }
