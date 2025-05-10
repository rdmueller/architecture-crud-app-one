"""API client for communication with FastAPI backend."""
import os
import requests
from typing import Dict, List, Optional, Any
import streamlit as st

# API base URL - configurable via environment variable
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8082")


class APIError(Exception):
    """Custom exception for API errors."""
    pass


def get_api_url(endpoint: str) -> str:
    """Get full API URL for endpoint."""
    return f"{API_BASE_URL}/api/{endpoint}"


def handle_response(response: requests.Response) -> Any:
    """Handle API response and raise appropriate errors."""
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise APIError("Resource not found")
    elif response.status_code == 422:
        raise APIError("Validation error")
    else:
        raise APIError(f"API Error: {response.status_code}")


# ADR Functions
def get_adrs() -> Dict[str, Any]:
    """Get all ADRs from API."""
    try:
        response = requests.get(get_api_url("adrs"))
        return handle_response(response)
    except Exception as e:
        st.error(f"Error fetching ADRs: {e}")
        return {}


def get_adr(adr_id: str) -> Optional[Dict[str, Any]]:
    """Get single ADR by ID."""
    try:
        response = requests.get(get_api_url(f"adrs/{adr_id}"))
        return handle_response(response)
    except Exception as e:
        st.error(f"Error fetching ADR {adr_id}: {e}")
        return None


def create_adr(adr_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create new ADR."""
    try:
        response = requests.post(get_api_url("adrs"), json=adr_data)
        return handle_response(response)
    except Exception as e:
        st.error(f"Error creating ADR: {e}")
        return None


def update_adr(adr_id: str, adr_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update existing ADR."""
    try:
        response = requests.put(get_api_url(f"adrs/{adr_id}"), json=adr_data)
        return handle_response(response)
    except Exception as e:
        st.error(f"Error updating ADR {adr_id}: {e}")
        return None


def delete_adr(adr_id: str) -> bool:
    """Delete ADR."""
    try:
        response = requests.delete(get_api_url(f"adrs/{adr_id}"))
        if response.status_code == 200:
            return True
        else:
            raise APIError(f"Failed to delete ADR: {response.status_code}")
    except Exception as e:
        st.error(f"Error deleting ADR {adr_id}: {e}")
        return False


# Quality Functions
def get_qualities() -> Dict[str, Any]:
    """Get all quality requirements."""
    try:
        response = requests.get(get_api_url("qualities"))
        return handle_response(response)
    except Exception as e:
        st.error(f"Error fetching qualities: {e}")
        return {}


def create_quality(quality_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create new quality requirement."""
    try:
        response = requests.post(get_api_url("qualities"), json=quality_data)
        return handle_response(response)
    except Exception as e:
        st.error(f"Error creating quality: {e}")
        return None


# Risk Functions
def get_risks() -> Dict[str, Any]:
    """Get all risks."""
    try:
        response = requests.get(get_api_url("risks"))
        return handle_response(response)
    except Exception as e:
        st.error(f"Error fetching risks: {e}")
        return {}


def create_risk(risk_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create new risk."""
    try:
        response = requests.post(get_api_url("risks"), json=risk_data)
        return handle_response(response)
    except Exception as e:
        st.error(f"Error creating risk: {e}")
        return None


# Technical Debt Functions
def get_technical_debts() -> Dict[str, Any]:
    """Get all technical debts."""
    try:
        response = requests.get(get_api_url("technical-debts"))
        return handle_response(response)
    except Exception as e:
        st.error(f"Error fetching technical debts: {e}")
        return {}


def create_technical_debt(debt_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create new technical debt."""
    try:
        response = requests.post(get_api_url("technical-debts"), json=debt_data)
        return handle_response(response)
    except Exception as e:
        st.error(f"Error creating technical debt: {e}")
        return None


# Component Functions
def get_components() -> Dict[str, Any]:
    """Get all components."""
    try:
        response = requests.get(get_api_url("components"))
        return handle_response(response)
    except Exception as e:
        st.error(f"Error fetching components: {e}")
        return {}


def create_component(component_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create new component."""
    try:
        response = requests.post(get_api_url("components"), json=component_data)
        return handle_response(response)
    except Exception as e:
        st.error(f"Error creating component: {e}")
        return None


# Architecture Functions
def get_architecture() -> Optional[Dict[str, Any]]:
    """Get entire architecture data."""
    try:
        response = requests.get(get_api_url("architecture"))
        return handle_response(response)
    except Exception as e:
        st.error(f"Error fetching architecture: {e}")
        return None
