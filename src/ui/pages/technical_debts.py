"""Technical Debts page for Architecture CRUD application."""
import streamlit as st
import requests
import pandas as pd
from typing import Dict, Any, List

# API base URL
API_BASE_URL = "http://localhost:8082"


def fetch_technical_debts() -> List[Dict[str, Any]]:
    """Fetch all technical debts from the API."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/technical-debts")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching technical debts: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return []


def create_technical_debt(debt_data: Dict[str, Any]) -> bool:
    """Create a new technical debt via API."""
    try:
        response = requests.post(f"{API_BASE_URL}/api/technical-debts", json=debt_data)
        if response.status_code == 201:
            st.success(f"Technical debt {debt_data['id']} created successfully!")
            return True
        else:
            st.error(f"Error creating technical debt: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def update_technical_debt(debt_id: str, debt_data: Dict[str, Any]) -> bool:
    """Update an existing technical debt via API."""
    try:
        response = requests.put(f"{API_BASE_URL}/api/technical-debts/{debt_id}", json=debt_data)
        if response.status_code == 200:
            st.success(f"Technical debt {debt_id} updated successfully!")
            return True
        else:
            st.error(f"Error updating technical debt: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def delete_technical_debt(debt_id: str) -> bool:
    """Delete a technical debt via API."""
    try:
        response = requests.delete(f"{API_BASE_URL}/api/technical-debts/{debt_id}")
        if response.status_code == 204:
            st.success(f"Technical debt {debt_id} deleted successfully!")
            return True
        else:
            st.error(f"Error deleting technical debt: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def render_technical_debts():
    """Render the Technical Debts page."""
    st.header("Technical Debts")
    
    # Create tabs for different operations
    tab1, tab2, tab3 = st.tabs(["List Technical Debts", "Create Technical Debt", "Edit Technical Debt"])
    
    with tab1:
        # List technical debts
        st.subheader("All Technical Debts")
        
        debts = fetch_technical_debts()
        
        if debts:
            # Create DataFrame for display
            df_data = []
            for debt in debts:
                df_data.append({
                    "ID": debt["id"],
                    "Title": debt["title"],
                    "Impact": debt.get("impact", "Unknown"),
                    "Effort": debt.get("effort", "Unknown"),
                    "Status": debt.get("status", "Unknown")
                })
            
            df = pd.DataFrame(df_data)
            
            # Display dataframe
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Add actions for each technical debt
            st.subheader("Actions")
            col1, col2 = st.columns(2)
            
            with col1:
                selected_debt = st.selectbox("Select Technical Debt", options=[d["id"] for d in debts])
            
            with col2:
                if st.button("Delete Selected Technical Debt", type="secondary"):
                    if delete_technical_debt(selected_debt):
                        st.rerun()
            
            # Show details of selected technical debt
            if selected_debt:
                st.subheader("Technical Debt Details")
                selected_debt_data = next((d for d in debts if d["id"] == selected_debt), None)
                if selected_debt_data:
                    st.json(selected_debt_data)
        else:
            st.info("No technical debts found. Create your first technical debt!")
    
    with tab2:
        # Create Technical Debt
        st.subheader("Create New Technical Debt")
        
        with st.form("create_debt_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                debt_id = st.text_input("Technical Debt ID", placeholder="TD-001", 
                                        help="Format: TD-XXX where XXX is a 3-digit number")
                title = st.text_input("Title", placeholder="Legacy code refactoring")
                impact = st.selectbox("Impact", ["low", "medium", "high"])
                effort = st.selectbox("Effort", ["low", "medium", "high"])
            
            with col2:
                status = st.selectbox("Status", ["identified", "acknowledged", "planned", "in progress", "resolved"])
                repayment_plan = st.text_area("Repayment Plan", 
                                              placeholder="Describe how to address this technical debt")
            
            description = st.text_area("Description", placeholder="Describe the technical debt in detail")
            
            submitted = st.form_submit_button("Create Technical Debt")
            
            if submitted:
                # Validate and create technical debt
                if not debt_id or not title:
                    st.error("Technical Debt ID and Title are required!")
                else:
                    debt_data = {
                        "id": debt_id,
                        "title": title,
                        "description": description,
                        "impact": impact,
                        "effort": effort,
                        "repaymentPlan": repayment_plan,
                        "status": status
                    }
                    
                    if create_technical_debt(debt_data):
                        st.rerun()
    
    with tab3:
        # Edit Technical Debt
        st.subheader("Edit Existing Technical Debt")
        
        debts = fetch_technical_debts()
        
        if debts:
            selected_debt_id = st.selectbox("Select Technical Debt to edit", 
                                            options=[d["id"] for d in debts],
                                            key="edit_debt_select")
            
            if selected_debt_id:
                selected_debt = next((d for d in debts if d["id"] == selected_debt_id), None)
                
                if selected_debt:
                    with st.form("edit_debt_form"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            title = st.text_input("Title", value=selected_debt["title"])
                            impact = st.selectbox("Impact", 
                                                  ["low", "medium", "high"],
                                                  index=["low", "medium", "high"].index(selected_debt.get("impact", "medium")))
                            effort = st.selectbox("Effort", 
                                                  ["low", "medium", "high"],
                                                  index=["low", "medium", "high"].index(selected_debt.get("effort", "medium")))
                        
                        with col2:
                            status = st.selectbox("Status", 
                                                  ["identified", "acknowledged", "planned", "in progress", "resolved"],
                                                  index=["identified", "acknowledged", "planned", "in progress", "resolved"].index(selected_debt.get("status", "identified")))
                            repayment_plan = st.text_area("Repayment Plan", 
                                                          value=selected_debt.get("repaymentPlan", ""))
                        
                        description = st.text_area("Description", value=selected_debt.get("description", ""))
                        
                        submitted = st.form_submit_button("Update Technical Debt")
                        
                        if submitted:
                            updated_data = {
                                "id": selected_debt_id,
                                "title": title,
                                "description": description,
                                "impact": impact,
                                "effort": effort,
                                "repaymentPlan": repayment_plan,
                                "status": status
                            }
                            
                            if update_technical_debt(selected_debt_id, updated_data):
                                st.rerun()
        else:
            st.info("No technical debts available to edit.")
