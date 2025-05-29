import time

# Shared memory dictionary
_shared_memory = {
    "entries": []
}

# Add new data to shared memory
def store_entry(source_type: str, format_type: str, intent: str, extracted_data: dict):
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source_type": source_type,
        "format": format_type,
        "intent": intent,
        "data": extracted_data
    }
    _shared_memory["entries"].append(entry)

# Retrieve all memory entries
def get_all_entries():
    return _shared_memory["entries"]

# Get the most recent entry
def get_latest_entry():
    return _shared_memory["entries"][-1] if _shared_memory["entries"] else None

# Clear memory (for testing or fresh start)
def clear_memory():
    _shared_memory["entries"].clear()

import json

def export_memory_to_file(file_path="data/sample_output/output_logs.json"):
    with open(file_path, "w") as f:
        json.dump(_shared_memory["entries"], f, indent=4)
    return file_path
