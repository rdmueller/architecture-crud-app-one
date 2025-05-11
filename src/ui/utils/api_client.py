"""API client for communication with FastAPI backend."""
import requests
from typing import Dict, List, Optional, Any
import streamlit as st

# API base URL - should be configurable
API_BASE_URL = "http://localhost:8082"


class APIError(Exception):
    """Custom exception for API errors."""
    pass


def get_api_url(endpoint: str) -> str:
    """Get full API URL for endpoint."""
    return f"{API_BASE_URL}/api/{endpoint}"


def handle_response(response: requests.Response) -> Any:
    """Handle API response and raise appropriate errors."""
    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    elif response.status_code == 404:
        raise APIError("Resource not found")
    elif response.status_code == 422:
        raise APIError("Validation error")
    else:
        raise APIError(f"API Error: {response.status_code}")


# ADR Functions
def get_adrs() -> List[Dict[str, Any]]:
    """Get all ADRs from API."""
    try:
        response = requests.get(get_api_url("adrs"))
        data = handle_response(response)
        print(f"API client received architecture data: {len(data.get('adrs', {}))}, {len(data.get('qualities', {}))}, {len(data.get('risks', {}))}, {len(data.get('technicalDebts', {}))}, {len(data.get('components', {}))}") 
        return data
    except Exception as e:
        st.error(f"Error fetching ADRs: {e}")
        return []


def get_adr(adr_id: str) -> Optional[Dict[str, Any]]:
    """Get single ADR by ID."""
    try:
        response = requests.get(get_api_url(f"adrs/{adr_id}"))
        data = handle_response(response)
        print(f"API client received architecture data: {len(data.get('adrs', {}))}, {len(data.get('qualities', {}))}, {len(data.get('risks', {}))}, {len(data.get('technicalDebts', {}))}, {len(data.get('components', {}))}") 
        return data
    except Exception as e:
        st.error(f"Error fetching ADR {adr_id}: {e}")
        return None


def create_adr(adr_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create new ADR."""
    try:
        response = requests.post(get_api_url("adrs"), json=adr_data)
        data = handle_response(response)
        print(f"API client received architecture data: {len(data.get('adrs', {}))}, {len(data.get('qualities', {}))}, {len(data.get('risks', {}))}, {len(data.get('technicalDebts', {}))}, {len(data.get('components', {}))}") 
        return data
    except Exception as e:
        st.error(f"Error creating ADR: {e}")
        return None


def update_adr(adr_id: str, adr_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update existing ADR."""
    try:
        response = requests.put(get_api_url(f"adrs/{adr_id}"), json=adr_data)
        data = handle_response(response)
        print(f"API client received architecture data: {len(data.get('adrs', {}))}, {len(data.get('qualities', {}))}, {len(data.get('risks', {}))}, {len(data.get('technicalDebts', {}))}, {len(data.get('components', {}))}") 
        return data
    except Exception as e:
        st.error(f"Error updating ADR {adr_id}: {e}")
        return None


def delete_adr(adr_id: str) -> bool:
    """Delete ADR."""
    try:
        response = requests.delete(get_api_url(f"adrs/{adr_id}"))
        if response.status_code == 204:
            return True
        else:
            raise APIError(f"Failed to delete ADR: {response.status_code}")
    except Exception as e:
        st.error(f"Error deleting ADR {adr_id}: {e}")
        return False


# Quality Functions
def get_qualities() -> List[Dict[str, Any]]:
    """Get all quality requirements."""
    try:
        response = requests.get(get_api_url("qualities"))
        data = handle_response(response)
        print(f"API client received architecture data: {len(data.get('adrs', {}))}, {len(data.get('qualities', {}))}, {len(data.get('risks', {}))}, {len(data.get('technicalDebts', {}))}, {len(data.get('components', {}))}") 
        return data
    except Exception as e:
        st.error(f"Error fetching qualities: {e}")
        return []


def create_quality(quality_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create new quality requirement."""
    try:
        response = requests.post(get_api_url("qualities"), json=quality_data)
        data = handle_response(response)
        print(f"API client received architecture data: {len(data.get('adrs', {}))}, {len(data.get('qualities', {}))}, {len(data.get('risks', {}))}, {len(data.get('technicalDebts', {}))}, {len(data.get('components', {}))}") 
        return data
    except Exception as e:
        st.error(f"Error creating quality: {e}")
        return None


# Risk Functions
def get_risks() -> List[Dict[str, Any]]:
    """Get all risks."""
    try:
        response = requests.get(get_api_url("risks"))
        data = handle_response(response)
        print(f"API client received architecture data: {len(data.get('adrs', {}))}, {len(data.get('qualities', {}))}, {len(data.get('risks', {}))}, {len(data.get('technicalDebts', {}))}, {len(data.get('components', {}))}") 
        return data
    except Exception as e:
        st.error(f"Error fetching risks: {e}")
        return []


def create_risk(risk_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create new risk."""
    try:
        response = requests.post(get_api_url("risks"), json=risk_data)
        data = handle_response(response)
        print(f"API client received architecture data: {len(data.get('adrs', {}))}, {len(data.get('qualities', {}))}, {len(data.get('risks', {}))}, {len(data.get('technicalDebts', {}))}, {len(data.get('components', {}))}") 
        return data
    except Exception as e:
        st.error(f"Error creating risk: {e}")
        return None


# Technical Debt Functions
def get_technical_debts() -> List[Dict[str, Any]]:
    """Get all technical debts."""
    try:
        response = requests.get(get_api_url("technical-debts"))
        data = handle_response(response)
        print(f"API client received architecture data: {len(data.get('adrs', {}))}, {len(data.get('qualities', {}))}, {len(data.get('risks', {}))}, {len(data.get('technicalDebts', {}))}, {len(data.get('components', {}))}") 
        return data
    except Exception as e:
        st.error(f"Error fetching technical debts: {e}")
        return []


def create_technical_debt(debt_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create new technical debt."""
    try:
        response = requests.post(get_api_url("technical-debts"), json=debt_data)
        data = handle_response(response)
        print(f"API client received architecture data: {len(data.get('adrs', {}))}, {len(data.get('qualities', {}))}, {len(data.get('risks', {}))}, {len(data.get('technicalDebts', {}))}, {len(data.get('components', {}))}") 
        return data
    except Exception as e:
        st.error(f"Error creating technical debt: {e}")
        return None


# Component Functions
def get_components() -> List[Dict[str, Any]]:
    """Get all components."""
    try:
        response = requests.get(get_api_url("components"))
        data = handle_response(response)
        print(f"API client received architecture data: {len(data.get('adrs', {}))}, {len(data.get('qualities', {}))}, {len(data.get('risks', {}))}, {len(data.get('technicalDebts', {}))}, {len(data.get('components', {}))}") 
        return data
    except Exception as e:
        st.error(f"Error fetching components: {e}")
        return []


def create_component(component_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create new component."""
    try:
        response = requests.post(get_api_url("components"), json=component_data)
        data = handle_response(response)
        print(f"API client received architecture data: {len(data.get('adrs', {}))}, {len(data.get('qualities', {}))}, {len(data.get('risks', {}))}, {len(data.get('technicalDebts', {}))}, {len(data.get('components', {}))}") 
        return data
    except Exception as e:
        st.error(f"Error creating component: {e}")
        return None


# Architecture Functions
def get_architecture() -> Dict[str, Any]:
    """Get entire architecture data."""
    try:
        response = requests.get(get_api_url("architecture"))
        data = handle_response(response)
        print(f"API client received architecture data: {len(data.get('adrs', {}))}, {len(data.get('qualities', {}))}, {len(data.get('risks', {}))}, {len(data.get('technicalDebts', {}))}, {len(data.get('components', {}))}") 
        return data
    except Exception as e:
        st.error(f"Error fetching architecture: {e}")
        return None
