"""Relationships management page for Architecture CRUD application."""
import streamlit as st
import requests
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
from typing import Dict, Any, List

# API base URL
API_BASE_URL = "http://localhost:8082"


def fetch_architecture_data() -> Dict[str, Any]:
    """Fetch full architecture data from API."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/architecture")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching architecture data: {response.status_code}")
            return {}
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return {}


def create_relationship_matrix(data: Dict[str, Any]) -> pd.DataFrame:
    """Create a relationship matrix from architecture data."""
    entities = []
    relationships = []
    
    # Collect all entities
    for entity_type, entities_dict in data.items():
        for entity_id, entity_data in entities_dict.items():
            entities.append({
                "id": entity_id,
                "type": entity_type,
                "title": entity_data.get("title", entity_id)
            })
    
    # Create matrix
    matrix_data = {}
    for source in entities:
        matrix_data[source["id"]] = {}
        for target in entities:
            matrix_data[source["id"]][target["id"]] = ""
    
    # Fill in relationships
    for entity_type, entities_dict in data.items():
        for entity_id, entity_data in entities_dict.items():
            if "relationships" in entity_data:
                for rel_type, rel_list in entity_data["relationships"].items():
                    for rel in rel_list:
                        target_id = rel.get("targetId")
                        if target_id and target_id in matrix_data.get(entity_id, {}):
                            rel_type_short = rel.get("type", rel_type)
                            matrix_data[entity_id][target_id] = rel_type_short
    
    # Convert to DataFrame
    df = pd.DataFrame(matrix_data)
    return df


def create_relationship_graph(data: Dict[str, Any]) -> go.Figure:
    """Create a network graph visualization of relationships."""
    G = nx.DiGraph()
    
    # Add nodes
    node_colors = {
        "adrs": "#FF6B6B",
        "qualities": "#4ECDC4", 
        "risks": "#FFE66D",
        "technicalDebts": "#95E1D3",
        "components": "#A6E3E9"
    }
    
    for entity_type, entities_dict in data.items():
        for entity_id, entity_data in entities_dict.items():
            G.add_node(entity_id, 
                      title=entity_data.get("title", entity_id),
                      type=entity_type,
                      color=node_colors.get(entity_type, "#CCCCCC"))
    
    # Add edges
    for entity_type, entities_dict in data.items():
        for entity_id, entity_data in entities_dict.items():
            if "relationships" in entity_data:
                for rel_type, rel_list in entity_data["relationships"].items():
                    for rel in rel_list:
                        target_id = rel.get("targetId")
                        if target_id and target_id in G.nodes:
                            G.add_edge(entity_id, target_id, 
                                     type=rel.get("type", rel_type),
                                     strength=rel.get("strength", "medium"))
    
    # Create Plotly figure
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Edge trace
    edge_trace = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(go.Scatter(
            x=[x0, x1, None],
            y=[y0, y1, None],
            mode='lines',
            line=dict(width=1, color='#888'),
            hoverinfo='none'
        ))
    
    # Node trace
    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            size=20,
            color=[G.nodes[node]['color'] for node in G.nodes()],
            line_width=2),
        text=[G.nodes[node]['title'] for node in G.nodes()],
        textposition="top center"
    )
    
    # Create figure with correct title format
    fig = go.Figure(data=edge_trace + [node_trace],
                    layout=go.Layout(
                        title=dict(text='Architecture Relationships Graph', font=dict(size=16)),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        annotations=[dict(
                            text="",
                            showarrow=False,
                            xref="paper", yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    
    return fig


def render_relationships():
    """Render the relationships management page."""
    st.header("Architecture Relationships")
    
    # Fetch architecture data
    data = fetch_architecture_data()
    
    if not data:
        st.info("No architecture data available. Please create some entities first.")
        return
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Relationship Matrix", "Network Graph", "Manage Relationships"])
    
    with tab1:
        # Relationship Matrix
        st.subheader("Relationship Matrix")
        
        matrix_df = create_relationship_matrix(data)
        
        if not matrix_df.empty:
            st.dataframe(matrix_df, use_container_width=True)
            
            # Export options
            st.subheader("Export Matrix")
            csv = matrix_df.to_csv(index=True)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="relationship_matrix.csv",
                mime="text/csv"
            )
        else:
            st.info("No relationships defined yet.")
    
    with tab2:
        # Network Graph
        st.subheader("Relationship Network Graph")
        
        fig = create_relationship_graph(data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Legend
        st.markdown("### Legend")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Entity Types:**")
            st.markdown("🔴 ADRs")
            st.markdown("🟢 Quality Requirements")
            st.markdown("🟡 Risks")
        
        with col2:
            st.markdown("&nbsp;")
            st.markdown("🟣 Technical Debts")
            st.markdown("🔵 Components")
    
    with tab3:
        # Manage Relationships
        st.subheader("Manage Relationships")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Select source entity
            entity_types = list(data.keys())
            source_type = st.selectbox("Source Entity Type", entity_types, key="source_type")
            
            if source_type and source_type in data:
                source_entities = [
                    f"{eid}: {edata.get('title', eid)}" 
                    for eid, edata in data[source_type].items()
                ]
                
                selected_source = st.selectbox("Source Entity", source_entities, key="source_entity")
                
                if selected_source:
                    source_id = selected_source.split(":")[0]
                    source_data = data[source_type].get(source_id, {})
                    
                    # Show current relationships
                    st.markdown("**Current Relationships:**")
                    if "relationships" in source_data:
                        for rel_type, rel_list in source_data["relationships"].items():
                            if rel_list:
                                st.markdown(f"*{rel_type}:*")
                                for rel in rel_list:
                                    st.write(f"- {rel.get('targetId')} ({rel.get('type', 'N/A')})")
                    else:
                        st.info("No relationships defined for this entity.")
        
        with col2:
            # Add new relationship
            st.markdown("**Add New Relationship**")
            
            target_type = st.selectbox("Target Entity Type", entity_types, key="target_type")
            
            if target_type and target_type in data:
                target_entities = [
                    f"{eid}: {edata.get('title', eid)}" 
                    for eid, edata in data[target_type].items()
                ]
                
                selected_target = st.selectbox("Target Entity", target_entities, key="target_entity")
                
                if selected_target:
                    target_id = selected_target.split(":")[0]
                    
                    rel_type = st.text_input("Relationship Type", 
                                             placeholder="e.g., implements, affects, mitigates")
                    
                    strength = st.selectbox("Relationship Strength", 
                                            ["weak", "medium", "strong"])
                    
                    if st.button("Add Relationship"):
                        # TODO: Implement API call to add relationship
                        st.info("This feature will be implemented in the next iteration.")
                        
                        # Example of what the API call would look like:
                        # relationship_data = {
                        #     "sourceType": source_type,
                        #     "sourceId": source_id,
                        #     "targetType": target_type,
                        #     "targetId": target_id,
                        #     "type": rel_type,
                        #     "strength": strength
                        # }
                        # response = requests.post(f"{API_BASE_URL}/api/relationships", 
                        #                        json=relationship_data)
