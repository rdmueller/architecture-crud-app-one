"""Test to verify the correct validation rules for each entity type."""
import requests


API_BASE = "http://localhost:8082"


def test_id_formats():
    """Test correct ID formats for each entity type."""
    
    test_cases = [
        # (entity_type, correct_id, incorrect_id)
        ("adrs", "ADR-001", "A-001"),
        ("qualities", "QR-001", "Q-001"),
        ("risks", "RISK-001", "R-001"),
        ("technical-debts", "TD-001", "T-001"),
        ("components", "C-001", "COMP-001"),
    ]
    
    for entity_type, correct_id, incorrect_id in test_cases:
        print(f"\nTesting {entity_type}...")
        
        # Create minimal entity with correct ID
        entity = {
            "id": correct_id,
            "title": "Test Entity",
            "description": "Test Description",
            # Add required fields for specific types
            "status": "proposed" if entity_type == "adrs" else None,
            "date": "2025-01-01" if entity_type == "adrs" else None,
            "authors": ["Test"] if entity_type == "adrs" else None,
            "context": "Test" if entity_type == "adrs" else None,
            "decision": "Test" if entity_type == "adrs" else None,
            "alternatives": {} if entity_type == "adrs" else None,
            "relationships": {"qualities": [], "risks": [], "technicalDebts": [], "components": [], "relatedAdrs": []} if entity_type == "adrs" else None,
            "priority": "high" if entity_type in ["qualities", "technical-debts"] else None,
            "qualityCategory": "performance" if entity_type == "qualities" else None,
            "metrics": [] if entity_type == "qualities" else None,
            "impact": "high" if entity_type in ["risks", "technical-debts"] else None,
            "probability": "low" if entity_type == "risks" else None,
            "mitigation": "Test" if entity_type == "risks" else None,
            "status": "identified" if entity_type == "risks" else None,
            "category": "technical" if entity_type == "risks" else None,
            "effort": "high" if entity_type == "technical-debts" else None,
            "resolution": "Test" if entity_type == "technical-debts" else None,
            "status": "planned" if entity_type == "technical-debts" else None,
            "responsibility": "Test" if entity_type == "components" else None,
            "type": "service" if entity_type == "components" else None,
            "interfaces": [] if entity_type == "components" else None,
            "attributes": {} if entity_type == "components" else None,
        }
        
        # Remove None values
        entity = {k: v for k, v in entity.items() if v is not None}
        
        # Test with correct ID
        response = requests.post(f"{API_BASE}/api/{entity_type}", json=entity)
        print(f"Correct ID ({correct_id}): {response.status_code}")
        if response.status_code != 201:
            print(f"Error: {response.json()}")
        
        # Test with incorrect ID format
        entity["id"] = incorrect_id
        response = requests.post(f"{API_BASE}/api/{entity_type}", json=entity)
        print(f"Incorrect ID ({incorrect_id}): {response.status_code}")
        if response.status_code == 422:
            print("Correct - validation error as expected")


if __name__ == "__main__":
    test_id_formats()
