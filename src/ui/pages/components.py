"""Components page for Architecture CRUD application."""
import streamlit as st
import requests
import pandas as pd
from typing import Dict, Any, List

# API base URL
API_BASE_URL = "http://localhost:8082"


def fetch_components() -> List[Dict[str, Any]]:
    """Fetch all components from the API."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/components")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching components: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return []


def create_component(component_data: Dict[str, Any]) -> bool:
    """Create a new component via API."""
    try:
        response = requests.post(f"{API_BASE_URL}/api/components", json=component_data)
        if response.status_code == 201:
            st.success(f"Component {component_data['id']} created successfully!")
            return True
        else:
            st.error(f"Error creating component: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def update_component(component_id: str, component_data: Dict[str, Any]) -> bool:
    """Update an existing component via API."""
    try:
        response = requests.put(f"{API_BASE_URL}/api/components/{component_id}", json=component_data)
        if response.status_code == 200:
            st.success(f"Component {component_id} updated successfully!")
            return True
        else:
            st.error(f"Error updating component: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def delete_component(component_id: str) -> bool:
    """Delete a component via API."""
    try:
        response = requests.delete(f"{API_BASE_URL}/api/components/{component_id}")
        if response.status_code == 204:
            st.success(f"Component {component_id} deleted successfully!")
            return True
        else:
            st.error(f"Error deleting component: {response.text}")
            return False
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return False


def render_components():
    """Render the Components page."""
    st.header("Components")
    
    # Create tabs for different operations
    tab1, tab2, tab3 = st.tabs(["List Components", "Create Component", "Edit Component"])
    
    with tab1:
        # List components
        st.subheader("All Components")
        
        components = fetch_components()
        
        if components:
            # Create DataFrame for display
            df_data = []
            for component in components:
                df_data.append({
                    "ID": component["id"],
                    "Title": component["title"],
                    "Responsibility": component.get("responsibility", "Not specified"),
                    "Interfaces": len(component.get("interfaces", [])),
                })
            
            df = pd.DataFrame(df_data)
            
            # Display dataframe
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Add actions for each component
            st.subheader("Actions")
            col1, col2 = st.columns(2)
            
            with col1:
                selected_component = st.selectbox("Select Component", options=[c["id"] for c in components])
            
            with col2:
                if st.button("Delete Selected Component", type="secondary"):
                    if delete_component(selected_component):
                        st.rerun()
            
            # Show details of selected component
            if selected_component:
                st.subheader("Component Details")
                selected_component_data = next((c for c in components if c["id"] == selected_component), None)
                if selected_component_data:
                    st.json(selected_component_data)
        else:
            st.info("No components found. Create your first component!")
    
    with tab2:
        # Create Component
        st.subheader("Create New Component")
        
        with st.form("create_component_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                component_id = st.text_input("Component ID", placeholder="COMP-001", 
                                             help="Format: COMP-XXX where XXX is a 3-digit number")
                title = st.text_input("Title", placeholder="User Service")
            
            with col2:
                responsibility = st.text_area("Responsibility", 
                                              placeholder="Describe what this component is responsible for")
            
            # Interfaces section
            st.subheader("Interfaces")
            num_interfaces = st.number_input("Number of interfaces", min_value=0, max_value=10, value=0)
            
            interfaces = []
            for i in range(num_interfaces):
                st.markdown(f"### Interface {i+1}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    interface_name = st.text_input(f"Interface {i+1} Name", key=f"interface_name_{i}")
                with col2:
                    interface_type = st.selectbox(f"Type", ["provided", "required"], key=f"interface_type_{i}")
                with col3:
                    protocol = st.text_input(f"Protocol", placeholder="REST, gRPC, etc.", key=f"interface_protocol_{i}")
                
                description = st.text_area(f"Description", key=f"interface_desc_{i}")
                
                if interface_name:
                    interfaces.append({
                        "name": interface_name,
                        "type": interface_type,
                        "protocol": protocol,
                        "description": description
                    })
            
            # Attributes section
            st.subheader("Attributes")
            num_attributes = st.number_input("Number of attributes", min_value=0, max_value=10, value=0)
            
            attributes = []
            for i in range(num_attributes):
                col1, col2 = st.columns(2)
                with col1:
                    attr_name = st.text_input(f"Attribute {i+1} Name", key=f"attr_name_{i}")
                with col2:
                    attr_value = st.text_input(f"Value", key=f"attr_value_{i}")
                
                if attr_name:
                    attributes.append({
                        "name": attr_name,
                        "value": attr_value
                    })
            
            submitted = st.form_submit_button("Create Component")
            
            if submitted:
                # Validate and create component
                if not component_id or not title:
                    st.error("Component ID and Title are required!")
                else:
                    component_data = {
                        "id": component_id,
                        "title": title,
                        "responsibility": responsibility,
                        "interfaces": interfaces,
                        "attributes": attributes
                    }
                    
                    if create_component(component_data):
                        st.rerun()
    
    with tab3:
        # Edit Component
        st.subheader("Edit Existing Component")
        
        components = fetch_components()
        
        if components:
            selected_component_id = st.selectbox("Select Component to edit", 
                                                 options=[c["id"] for c in components],
                                                 key="edit_component_select")
            
            if selected_component_id:
                selected_component = next((c for c in components if c["id"] == selected_component_id), None)
                
                if selected_component:
                    with st.form("edit_component_form"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            title = st.text_input("Title", value=selected_component["title"])
                        
                        with col2:
                            responsibility = st.text_area("Responsibility", 
                                                          value=selected_component.get("responsibility", ""))
                        
                        submitted = st.form_submit_button("Update Component")
                        
                        if submitted:
                            updated_data = {
                                "id": selected_component_id,
                                "title": title,
                                "responsibility": responsibility,
                                "interfaces": selected_component.get("interfaces", []),
                                "attributes": selected_component.get("attributes", [])
                            }
                            
                            if update_component(selected_component_id, updated_data):
                                st.rerun()
        else:
            st.info("No components available to edit.")
