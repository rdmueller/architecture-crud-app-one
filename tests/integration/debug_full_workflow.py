"""Debug full workflow validation errors."""
import requests
import json
from datetime import datetime


# Create all entities
quality = {
    "id": "QR-001",
    "title": "Performance",
    "description": "System performance",
    "priority": "high",
    "qualityCategory": "performance",
    "metrics": []
}

risk = {
    "id": "RISK-001",
    "title": "Database Risk",
    "description": "Database issues",
    "impact": "high",
    "probability": "low",
    "mitigation": "Use caching",
    "status": "identified",
    "category": "technical"
}

# Create entities
print("Creating quality...")
response = requests.post("http://localhost:8082/api/qualities", json=quality)
print(f"Quality: {response.status_code}")

print("Creating risk...")
response = requests.post("http://localhost:8082/api/risks", json=risk)
print(f"Risk: {response.status_code}")

# Create ADR with relationships
adr = {
    "id": "ADR-001",
    "title": "Architecture Decision",
    "status": "accepted",
    "date": datetime.now().strftime("%Y-%m-%d"),
    "authors": ["Test Author"],
    "context": "Architecture context",
    "decision": "Architecture decision",
    "alternatives": {},
    "relationships": {
        "qualities": [{"id": quality["id"], "type": "implements", "strength": "strong"}],
        "risks": [{"id": risk["id"], "type": "mitigates", "strength": "medium"}],
        "technicalDebts": [],
        "components": [],
        "relatedAdrs": []
    }
}

print("\nCreating ADR with relationships...")
response = requests.post("http://localhost:8082/api/adrs", json=adr)
print(f"ADR: {response.status_code}")
if response.status_code != 201:
    print(f"Error: {response.json()}")
    
    # Test each relationship type separately
    print("\nTesting relationship types separately...")
    
    # Test risk relationship only
    adr_risk_only = adr.copy()
    adr_risk_only["relationships"] = {
        "qualities": [],
        "risks": [{"id": risk["id"], "type": "mitigates", "strength": "medium"}],
        "technicalDebts": [],
        "components": [],
        "relatedAdrs": []
    }
    
    response = requests.post("http://localhost:8082/api/adrs", json=adr_risk_only)
    print(f"ADR with risk only: {response.status_code}")
    if response.status_code != 201:
        print(f"Error: {response.json()}")
