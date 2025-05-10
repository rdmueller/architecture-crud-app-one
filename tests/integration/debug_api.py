"""Debug API validation errors."""
import requests


def create_valid_quality():
    """Create a valid quality object."""
    return {
        "id": "Q-001",
        "title": "Performance",
        "description": "The system must respond quickly to user requests.",
        "priority": "high",
        "qualityCategory": "performance",
        "metrics": [
            {
                "name": "Response Time",
                "target": "< 200ms",
                "current": "150ms"
            }
        ]
    }


# Test quality creation
print("Testing quality creation...")
quality = create_valid_quality()
response = requests.post("http://localhost:8082/api/qualities", json=quality)
print(f"Status: {response.status_code}")
if response.status_code != 201:
    print(f"Error: {response.json()}")
else:
    print("Success!")
