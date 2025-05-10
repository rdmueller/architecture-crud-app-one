"""Quality Requirements page for Architecture CRUD application."""
import streamlit as st
import requests
import pandas as pd
from typing import Dict, Any, List

# API base URL
API_BASE_URL = "http://localhost:8082"


def fetch_qualities() -> List[Dict[str, Any]]:
    """Fetch all quality requirements from the API."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/qualities")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching qualities: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return []


def create_quality(quality_data: Dict[str, Any]) -> bool:
    """Create a new quality requirement via API."""
    try:
        response = requests.post(f"{API_BASE_URL}/api/qualities", json=quality_data)
        if response.status_code == 201:
            st.success(f"Quality {quality_data['id']} created successfully!")
            return True
        else:
            st.error(f"Error creating quality: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def update_quality(quality_id: str, quality_data: Dict[str, Any]) -> bool:
    """Update an existing quality requirement via API."""
    try:
        response = requests.put(f"{API_BASE_URL}/api/qualities/{quality_id}", json=quality_data)
        if response.status_code == 200:
            st.success(f"Quality {quality_id} updated successfully!")
            return True
        else:
            st.error(f"Error updating quality: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def delete_quality(quality_id: str) -> bool:
    """Delete a quality requirement via API."""
    try:
        response = requests.delete(f"{API_BASE_URL}/api/qualities/{quality_id}")
        if response.status_code == 204:
            st.success(f"Quality {quality_id} deleted successfully!")
            return True
        else:
            st.error(f"Error deleting quality: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def render_qualities():
    """Render the Quality Requirements page."""
    st.header("Quality Requirements")
    
    # Create tabs for different operations
    tab1, tab2, tab3 = st.tabs(["List Qualities", "Create Quality", "Edit Quality"])
    
    with tab1:
        # List qualities
        st.subheader("All Quality Requirements")
        
        qualities = fetch_qualities()
        
        if qualities:
            # Create DataFrame for display
            df_data = []
            for quality in qualities:
                df_data.append({
                    "ID": quality["id"],
                    "Title": quality["title"],
                    "Priority": quality.get("priority", "Unknown"),
                    "Metrics": len(quality.get("metrics", [])),
                })
            
            df = pd.DataFrame(df_data)
            
            # Display dataframe
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Add actions for each quality
            st.subheader("Actions")
            col1, col2 = st.columns(2)
            
            with col1:
                selected_quality = st.selectbox("Select Quality", options=[q["id"] for q in qualities])
            
            with col2:
                if st.button("Delete Selected Quality", type="secondary"):
                    if delete_quality(selected_quality):
                        st.rerun()
            
            # Show details of selected quality
            if selected_quality:
                st.subheader("Quality Details")
                selected_quality_data = next((q for q in qualities if q["id"] == selected_quality), None)
                if selected_quality_data:
                    st.json(selected_quality_data)
        else:
            st.info("No quality requirements found. Create your first quality requirement!")
    
    with tab2:
        # Create Quality
        st.subheader("Create New Quality Requirement")
        
        with st.form("create_quality_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                quality_id = st.text_input("Quality ID", placeholder="QA-001", 
                                           help="Format: QA-XXX where XXX is a 3-digit number")
                title = st.text_input("Title", placeholder="System Performance")
                priority = st.selectbox("Priority", ["must", "should", "could", "wont"])
            
            with col2:
                description = st.text_area("Description", 
                                           placeholder="Describe the quality requirement")
            
            # Metrics section
            st.subheader("Metrics")
            num_metrics = st.number_input("Number of metrics", min_value=0, max_value=10, value=0)
            
            metrics = []
            for i in range(num_metrics):
                st.markdown(f"### Metric {i+1}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    metric_name = st.text_input(f"Metric {i+1} Name", key=f"metric_name_{i}")
                with col2:
                    target_value = st.text_input(f"Target Value", key=f"metric_target_{i}")
                with col3:
                    unit = st.text_input(f"Unit", key=f"metric_unit_{i}")
                
                if metric_name:
                    metrics.append({
                        "metricName": metric_name,
                        "targetValue": target_value,
                        "unit": unit
                    })
            
            submitted = st.form_submit_button("Create Quality")
            
            if submitted:
                # Validate and create quality
                if not quality_id or not title:
                    st.error("Quality ID and Title are required!")
                else:
                    quality_data = {
                        "id": quality_id,
                        "title": title,
                        "description": description,
                        "metrics": metrics,
                        "priority": priority
                    }
                    
                    if create_quality(quality_data):
                        st.rerun()
    
    with tab3:
        # Edit Quality
        st.subheader("Edit Existing Quality Requirement")
        
        qualities = fetch_qualities()
        
        if qualities:
            selected_quality_id = st.selectbox("Select Quality to edit", 
                                               options=[q["id"] for q in qualities],
                                               key="edit_quality_select")
            
            if selected_quality_id:
                selected_quality = next((q for q in qualities if q["id"] == selected_quality_id), None)
                
                if selected_quality:
                    with st.form("edit_quality_form"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            title = st.text_input("Title", value=selected_quality["title"])
                            priority = st.selectbox("Priority", 
                                                    ["must", "should", "could", "wont"],
                                                    index=["must", "should", "could", "wont"].index(selected_quality.get("priority", "should")))
                        
                        with col2:
                            description = st.text_area("Description", 
                                                       value=selected_quality.get("description", ""))
                        
                        submitted = st.form_submit_button("Update Quality")
                        
                        if submitted:
                            updated_data = {
                                "id": selected_quality_id,
                                "title": title,
                                "description": description,
                                "metrics": selected_quality.get("metrics", []),
                                "priority": priority
                            }
                            
                            if update_quality(selected_quality_id, updated_data):
                                st.rerun()
        else:
            st.info("No quality requirements available to edit.")
