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
def detect_tone(content: str) -> str:
    content = content.lower()
    if any(word in content for word in ["not acceptable", "furious", "angry", "threaten", "lawsuit", "legal"]):
        return "Threatening"
    elif any(word in content for word in ["disappointed", "very unhappy", "frustrated", "bad experience"]):
        return "Escalation"
    elif any(word in content for word in ["please", "kindly", "would you mind"]):
        return "Polite"
    else:
        return "Neutral"

def decide_action(tone: str, urgency: str) -> str:
    if tone in ["Threatening", "Escalation"] or urgency == "High":
        return "Escalate"
    else:
        return "RoutineLog"

def parse_email(content: str) -> dict:
    sender_email = extract_sender_email(content)
    sender_name = extract_sender_name(content)
    urgency = detect_urgency(content)
    tone = detect_tone(content)
    action = decide_action(tone, urgency)

    return {
        "sender_email": sender_email,
        "sender_name": sender_name,
        "urgency": urgency,
        "tone": tone,
        "recommended_action": action,
        "raw_content": content.strip()
    }