#!/usr/bin/env python
"""Debug API endpoints and data loading."""
import requests
import json
import os
import sys

def debug_api_endpoints():
    """Debug API endpoints."""
    base_url = "http://localhost:8082"
    
    print("Debugging API endpoints...")
    
    # Check health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Failed to connect to health endpoint: {e}")
        print("Is the API server running?")
        return
    
    # Check architecture endpoint
    try:
        response = requests.get(f"{base_url}/api/architecture")
        print(f"\nArchitecture endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Architecture data:")
            print(f"- Metadata: {data.get('metadata', {}).get('title', 'N/A')}")
            print(f"- ADRs: {len(data.get('adrs', {}))}")
            print(f"- Qualities: {len(data.get('qualities', {}))}")
            print(f"- Risks: {len(data.get('risks', {}))}")
            print(f"- Technical Debts: {len(data.get('technicalDebts', {}))}")
            print(f"- Components: {len(data.get('components', {}))}")
            
            # Save response to file for inspection
            with open("api_architecture_response.json", "w") as f:
                json.dump(data, f, indent=2)
            print(f"Saved response to api_architecture_response.json")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Failed to connect to architecture endpoint: {e}")
    
    # Check ADRs endpoint
    try:
        response = requests.get(f"{base_url}/api/adrs")
        print(f"\nADRs endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} ADRs")
            if data:
                print("First ADR:")
                print(f"- ID: {data[0].get('id', 'N/A')}")
                print(f"- Title: {data[0].get('title', 'N/A')}")
            
            # Save response to file for inspection
            with open("api_adrs_response.json", "w") as f:
                json.dump(data, f, indent=2)
            print(f"Saved response to api_adrs_response.json")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Failed to connect to ADRs endpoint: {e}")

def main():
    """Main function."""
    print("Architecture CRUD API Debugger")
    print("=============================")
    
    debug_api_endpoints()

if __name__ == "__main__":
    main()
