"""Debug relationship validation errors."""
import requests
import json
from datetime import datetime


# Create valid entities
adr = {
    "id": "ADR-001",
    "title": "Test ADR",
    "status": "accepted",
    "date": datetime.now().strftime("%Y-%m-%d"),
    "authors": ["Test Author"],
    "context": "Test context",
    "decision": "Test decision",
    "alternatives": {},
    "relationships": {
        "qualities": [],
        "risks": [],
        "technicalDebts": [],
        "components": [],
        "relatedAdrs": []
    }
}

quality = {
    "id": "QR-001",
    "title": "Performance",
    "description": "Test quality",
    "priority": "high",
    "qualityCategory": "performance",
    "metrics": []
}

# Create quality first
print("Creating quality...")
response = requests.post("http://localhost:8082/api/qualities", json=quality)
print(f"Quality creation: {response.status_code}")
if response.status_code != 201:
    print(f"Error: {response.json()}")

# Create ADR with relationship
print("\nCreating ADR with relationship...")
adr["relationships"]["qualities"] = [
    {
        "id": quality["id"],
        "type": "addresses",
        "strength": "strong"
    }
]

response = requests.post("http://localhost:8082/api/adrs", json=adr)
print(f"ADR creation: {response.status_code}")
if response.status_code != 201:
    print(f"Error: {response.json()}")
    # Print the exact structure sent
    print(f"\nSent data: {json.dumps(adr, indent=2)}")
