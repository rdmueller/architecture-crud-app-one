"""Risks page for Architecture CRUD application."""
import streamlit as st
import requests
import pandas as pd
from typing import Dict, Any, List

# API base URL
API_BASE_URL = "http://localhost:8082"


def fetch_risks() -> List[Dict[str, Any]]:
    """Fetch all risks from the API."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/risks")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching risks: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return []


def create_risk(risk_data: Dict[str, Any]) -> bool:
    """Create a new risk via API."""
    try:
        response = requests.post(f"{API_BASE_URL}/api/risks", json=risk_data)
        if response.status_code == 201:
            st.success(f"Risk {risk_data['id']} created successfully!")
            return True
        else:
            st.error(f"Error creating risk: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def update_risk(risk_id: str, risk_data: Dict[str, Any]) -> bool:
    """Update an existing risk via API."""
    try:
        response = requests.put(f"{API_BASE_URL}/api/risks/{risk_id}", json=risk_data)
        if response.status_code == 200:
            st.success(f"Risk {risk_id} updated successfully!")
            return True
        else:
            st.error(f"Error updating risk: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def delete_risk(risk_id: str) -> bool:
    """Delete a risk via API."""
    try:
        response = requests.delete(f"{API_BASE_URL}/api/risks/{risk_id}")
        if response.status_code == 204:
            st.success(f"Risk {risk_id} deleted successfully!")
            return True
        else:
            st.error(f"Error deleting risk: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def render_risks():
    """Render the Risks page."""
    st.header("Risks")
    
    # Create tabs for different operations
    tab1, tab2, tab3 = st.tabs(["List Risks", "Create Risk", "Edit Risk"])
    
    with tab1:
        # List risks
        st.subheader("All Risks")
        
        risks = fetch_risks()
        
        if risks:
            # Create DataFrame for display
            df_data = []
            for risk in risks:
                df_data.append({
                    "ID": risk["id"],
                    "Title": risk["title"],
                    "Impact": risk.get("impact", "Unknown"),
                    "Likelihood": risk.get("likelihood", "Unknown"),
                    "Status": risk.get("status", "Unknown")
                })
            
            df = pd.DataFrame(df_data)
            
            # Display dataframe
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Add actions for each risk
            st.subheader("Actions")
            col1, col2 = st.columns(2)
            
            with col1:
                selected_risk = st.selectbox("Select Risk", options=[r["id"] for r in risks])
            
            with col2:
                if st.button("Delete Selected Risk", type="secondary"):
                    if delete_risk(selected_risk):
                        st.rerun()
            
            # Show details of selected risk
            if selected_risk:
                st.subheader("Risk Details")
                selected_risk_data = next((r for r in risks if r["id"] == selected_risk), None)
                if selected_risk_data:
                    st.json(selected_risk_data)
        else:
            st.info("No risks found. Create your first risk!")
    
    with tab2:
        # Create Risk
        st.subheader("Create New Risk")
        
        with st.form("create_risk_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                risk_id = st.text_input("Risk ID", placeholder="RISK-001", 
                                        help="Format: RISK-XXX where XXX is a 3-digit number")
                title = st.text_input("Title", placeholder="Data breach risk")
                impact = st.selectbox("Impact", ["low", "medium", "high", "critical"])
                likelihood = st.selectbox("Likelihood", ["low", "medium", "high", "very high"])
            
            with col2:
                status = st.selectbox("Status", ["identified", "analyzing", "monitoring", "mitigated", "accepted", "closed"])
                owner = st.text_input("Owner", placeholder="John Doe")
                mitigation_strategy = st.text_area("Mitigation Strategy", 
                                                   placeholder="Describe how to mitigate this risk")
            
            description = st.text_area("Description", placeholder="Describe the risk in detail")
            
            submitted = st.form_submit_button("Create Risk")
            
            if submitted:
                # Validate and create risk
                if not risk_id or not title:
                    st.error("Risk ID and Title are required!")
                else:
                    risk_data = {
                        "id": risk_id,
                        "title": title,
                        "description": description,
                        "impact": impact,
                        "likelihood": likelihood,
                        "mitigationStrategy": mitigation_strategy,
                        "status": status,
                        "owner": owner
                    }
                    
                    if create_risk(risk_data):
                        st.rerun()
    
    with tab3:
        # Edit Risk
        st.subheader("Edit Existing Risk")
        
        risks = fetch_risks()
        
        if risks:
            selected_risk_id = st.selectbox("Select Risk to edit", 
                                            options=[r["id"] for r in risks],
                                            key="edit_risk_select")
            
            if selected_risk_id:
                selected_risk = next((r for r in risks if r["id"] == selected_risk_id), None)
                
                if selected_risk:
                    with st.form("edit_risk_form"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            title = st.text_input("Title", value=selected_risk["title"])
                            impact = st.selectbox("Impact", 
                                                  ["low", "medium", "high", "critical"],
                                                  index=["low", "medium", "high", "critical"].index(selected_risk.get("impact", "medium")))
                            likelihood = st.selectbox("Likelihood", 
                                                      ["low", "medium", "high", "very high"],
                                                      index=["low", "medium", "high", "very high"].index(selected_risk.get("likelihood", "medium")))
                        
                        with col2:
                            status = st.selectbox("Status", 
                                                  ["identified", "analyzing", "monitoring", "mitigated", "accepted", "closed"],
                                                  index=["identified", "analyzing", "monitoring", "mitigated", "accepted", "closed"].index(selected_risk.get("status", "identified")))
                            owner = st.text_input("Owner", value=selected_risk.get("owner", ""))
                            mitigation_strategy = st.text_area("Mitigation Strategy", 
                                                               value=selected_risk.get("mitigationStrategy", ""))
                        
                        description = st.text_area("Description", value=selected_risk.get("description", ""))
                        
                        submitted = st.form_submit_button("Update Risk")
                        
                        if submitted:
                            updated_data = {
                                "id": selected_risk_id,
                                "title": title,
                                "description": description,
                                "impact": impact,
                                "likelihood": likelihood,
                                "mitigationStrategy": mitigation_strategy,
                                "status": status,
                                "owner": owner
                            }
                            
                            if update_risk(selected_risk_id, updated_data):
                                st.rerun()
        else:
            st.info("No risks available to edit.")
