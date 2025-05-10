"""ADRs page for Architecture CRUD application."""
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date
from typing import Dict, Any, List

# API base URL - should be configurable
API_BASE_URL = "http://localhost:8082"


def fetch_adrs() -> List[Dict[str, Any]]:
    """Fetch all ADRs from the API."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/adrs")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching ADRs: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return []


def create_adr(adr_data: Dict[str, Any]) -> bool:
    """Create a new ADR via API."""
    try:
        response = requests.post(f"{API_BASE_URL}/api/adrs", json=adr_data)
        if response.status_code == 201:
            st.success(f"ADR {adr_data['id']} created successfully!")
            return True
        else:
            st.error(f"Error creating ADR: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def update_adr(adr_id: str, adr_data: Dict[str, Any]) -> bool:
    """Update an existing ADR via API."""
    try:
        response = requests.put(f"{API_BASE_URL}/api/adrs/{adr_id}", json=adr_data)
        if response.status_code == 200:
            st.success(f"ADR {adr_id} updated successfully!")
            return True
        else:
            st.error(f"Error updating ADR: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def delete_adr(adr_id: str) -> bool:
    """Delete an ADR via API."""
    try:
        response = requests.delete(f"{API_BASE_URL}/api/adrs/{adr_id}")
        if response.status_code == 204:
            st.success(f"ADR {adr_id} deleted successfully!")
            return True
        else:
            st.error(f"Error deleting ADR: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def render_adrs():
    """Render the ADRs page."""
    st.header("Architecture Decision Records (ADRs)")
    
    # Create tabs for different operations
    tab1, tab2, tab3 = st.tabs(["List ADRs", "Create ADR", "Edit ADR"])
    
    with tab1:
        # List ADRs
        st.subheader("All ADRs")
        
        adrs = fetch_adrs()
        
        if adrs:
            # Create DataFrame for display
            df_data = []
            for adr in adrs:
                df_data.append({
                    "ID": adr["id"],
                    "Title": adr["title"],
                    "Status": adr["status"],
                    "Date": adr["date"],
                    "Authors": ", ".join(adr.get("authors", []))
                })
            
            df = pd.DataFrame(df_data)
            
            # Display dataframe with actions
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Add actions for each ADR
            st.subheader("Actions")
            col1, col2 = st.columns(2)
            
            with col1:
                selected_adr = st.selectbox("Select ADR", options=[adr["id"] for adr in adrs], key="delete_adr_select")
            
            with col2:
                if st.button("Delete Selected ADR", type="secondary", key="delete_adr_button"):
                    if delete_adr(selected_adr):
                        st.rerun()
            
            # Show details of selected ADR
            if selected_adr:
                st.subheader("ADR Details")
                selected_adr_data = next((adr for adr in adrs if adr["id"] == selected_adr), None)
                if selected_adr_data:
                    st.json(selected_adr_data)
        else:
            st.info("No ADRs found. Create your first ADR!")
    
    with tab2:
        # Create ADR
        st.subheader("Create New ADR")
        
        with st.form("create_adr_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                adr_id = st.text_input("ADR ID", placeholder="ADR-001", key="adr_id",
                                       help="Format: ADR-XXX where XXX is a 3-digit number")
                title = st.text_input("Title", placeholder="Choose technology X for component Y", key="title")
                status = st.selectbox("Status", ["proposed", "accepted", "rejected", "deprecated", "superseded"], key="status")
                adr_date = st.date_input("Date", value=date.today(), key="date")
            
            with col2:
                authors = st.text_input("Authors", placeholder="John Doe, Jane Smith", key="authors",
                                        help="Comma-separated list of authors")
                context = st.text_area("Context", placeholder="Describe the context and problem statement", key="context")
                decision = st.text_area("Decision", placeholder="Describe the decision that was made", key="decision")
            
            # Alternatives section
            st.subheader("Alternatives")
            num_alternatives = st.number_input("Number of alternatives", min_value=0, max_value=10, value=0, key="num_alternatives")
            
            alternatives = {}
            for i in range(num_alternatives):
                st.markdown(f"### Alternative {i+1}")
                alt_key = st.text_input(f"Alternative {i+1} Name", key=f"alt_name_{i}")
                if alt_key:
                    col1, col2 = st.columns(2)
                    with col1:
                        advantages = st.text_area(f"Advantages", key=f"alt_advantages_{i}", placeholder="List advantages, one per line")
                    with col2:
                        disadvantages = st.text_area(f"Disadvantages", key=f"alt_disadvantages_{i}", placeholder="List disadvantages, one per line")
                    alternatives[alt_key] = {
                        "advantages": advantages.split("\n") if advantages else [], 
                        "disadvantages": disadvantages.split("\n") if disadvantages else []
                    }
            
            submitted = st.form_submit_button("Create ADR", type="primary", use_container_width=True)
            
            if submitted:
                # Validate and create ADR
                if not adr_id or not title:
                    st.error("ADR ID and Title are required!")
                else:
                    # Handle authors split
                    author_list = []
                    if authors:
                        author_list = [author.strip() for author in authors.split(",") if author.strip()]
                    
                    adr_data = {
                        "id": adr_id,
                        "title": title,
                        "status": status,
                        "date": adr_date.isoformat(),
                        "authors": author_list,
                        "context": context,
                        "decision": decision,
                        "alternatives": alternatives,
                        "relationships": {
                            "qualities": [],
                            "risks": [],
                            "technicalDebts": [],
                            "components": [],
                            "relatedAdrs": []
                        }
                    }
                    
                    if create_adr(adr_data):
                        st.rerun()
    
    with tab3:
        # Edit ADR
        st.subheader("Edit Existing ADR")
        
        adrs = fetch_adrs()
        
        if adrs:
            selected_adr_id = st.selectbox("Select ADR to edit", 
                                           options=[adr["id"] for adr in adrs],
                                           key="edit_adr_select")
            
            if selected_adr_id:
                selected_adr = next((adr for adr in adrs if adr["id"] == selected_adr_id), None)
                
                if selected_adr:
                    with st.form("edit_adr_form"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            title = st.text_input("Title", value=selected_adr["title"])
                            status = st.selectbox("Status", 
                                                  ["proposed", "accepted", "rejected", "deprecated", "superseded"],
                                                  index=["proposed", "accepted", "rejected", "deprecated", "superseded"].index(selected_adr["status"]))
                            adr_date = st.date_input("Date", value=datetime.fromisoformat(selected_adr["date"]).date())
                        
                        with col2:
                            authors = st.text_input("Authors", 
                                                    value=", ".join(selected_adr.get("authors", [])))
                            context = st.text_area("Context", value=selected_adr.get("context", ""))
                            decision = st.text_area("Decision", value=selected_adr.get("decision", ""))
                        
                        submitted = st.form_submit_button("Update ADR")
                        
                        if submitted:
                            updated_data = {
                                "id": selected_adr_id,
                                "title": title,
                                "status": status,
                                "date": adr_date.isoformat(),
                                "authors": [author.strip() for author in authors.split(",") if author.strip()],
                                "context": context,
                                "decision": decision,
                                "alternatives": selected_adr.get("alternatives", {}),
                                "relationships": selected_adr.get("relationships", {
                                    "qualities": [],
                                    "risks": [],
                                    "technicalDebts": [],
                                    "components": [],
                                    "relatedAdrs": []
                                })
                            }
                            
                            if update_adr(selected_adr_id, updated_data):
                                st.rerun()
        else:
            st.info("No ADRs available to edit.")
