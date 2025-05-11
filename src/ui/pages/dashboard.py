"""Dashboard page for Architecture CRUD application."""
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from typing import Dict, Any, List

# API base URL - should be configurable
API_BASE_URL = "http://localhost:8082"


def fetch_architecture_data():
    """Fetch all architecture data from the API."""
    try:
        response = requests.get(f"{API_BASE_URL}/api/architecture")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching data: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return None


def render_dashboard():
    st.write("Debug mode enabled")
    """Render the dashboard page."""
    st.header("Architecture Overview")
    
    # Fetch architecture data
    data = fetch_architecture_data()
    if data:
        st.write(f"Debug - Raw data: {type(data)}")
    
    if data:
        # Extract entities
        adrs = data.get("adrs", {})
        qualities = data.get("qualities", {})
        risks = data.get("risks", {})
        technical_debts = data.get("technicalDebts", {})
        components = data.get("components", {})
        
        # Debug output
        st.write(f"Debug - Data received: ADRs: {len(adrs)}, Qualities: {len(qualities)}, Risks: {len(risks)}")
    else:
        # If no data available, show error
        st.error("Could not fetch architecture data from API. Please check if the API server is running.")
        adrs = qualities = risks = technical_debts = components = {}
    
    # Display metrics
    st.markdown("### Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("ADRs", len(adrs))
    with col2:
        st.metric("Qualities", len(qualities))
    with col3:
        st.metric("Risks", len(risks))
    with col4:
        st.metric("Technical Debts", len(technical_debts))
    with col5:
        st.metric("Components", len(components))
    
    # Display recent items
    st.markdown("### Recent Activity")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recent ADRs")
        if adrs:
            # Create DataFrame for recent ADRs
            adr_data = []
            for adr_id, adr in adrs.items():
                adr_data.append({
                    "ID": adr["id"],
                    "Title": adr["title"],
                    "Status": adr["status"],
                    "Date": adr["date"]
                })
            
            if adr_data:
                df = pd.DataFrame(adr_data)
                df = df.sort_values("Date", ascending=False).head(5)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No ADRs found")
        else:
            st.info("No ADRs available")
    
    with col2:
        st.subheader("Open Risks")
        if risks:
            # Create DataFrame for open risks
            risk_data = []
            for risk_id, risk in risks.items():
                if risk.get("status") in ["identified", "monitoring"]:
                    risk_data.append({
                        "ID": risk["id"],
                        "Title": risk["title"],
                        "Impact": risk.get("impact", "Unknown"),
                        "Likelihood": risk.get("likelihood", "Unknown"),
                        "Status": risk.get("status", "Unknown")
                    })
            
            if risk_data:
                df = pd.DataFrame(risk_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No open risks found")
        else:
            st.info("No risks available")
    
    # Visualizations
    st.markdown("### Visualizations")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("ADR Status Distribution")
        if adrs:
            status_counts = {}
            for adr in adrs.values():
                status = adr.get("status", "Unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            if status_counts:
                fig = px.pie(
                    values=list(status_counts.values()),
                    names=list(status_counts.keys()),
                    title="ADR Status Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No ADR data available for visualization")
        else:
            st.info("No ADRs available")
    
    with col2:
        st.subheader("Risk Heat Map")
        if risks:
            # Create risk matrix data
            impact_levels = ["low", "medium", "high", "critical"]
            likelihood_levels = ["low", "medium", "high", "very high"]
            
            risk_matrix = [[0 for _ in likelihood_levels] for _ in impact_levels]
            
            for risk in risks.values():
                impact = risk.get("impact", "low")
                likelihood = risk.get("likelihood", "low")
                
                if impact in impact_levels and likelihood in likelihood_levels:
                    i = impact_levels.index(impact)
                    j = likelihood_levels.index(likelihood)
                    risk_matrix[i][j] += 1
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=risk_matrix,
                x=likelihood_levels,
                y=impact_levels,
                colorscale="RdYlGn_r",
                text=risk_matrix,
                texttemplate="%{text}",
                textfont={"size": 20},
                colorbar=dict(title="Risk Count")
            ))
            
            fig.update_layout(
                title="Risk Matrix",
                xaxis_title="Likelihood",
                yaxis_title="Impact",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No risks available")
    
    # Technical debt overview
    st.markdown("### Technical Debt Overview")
    if technical_debts:
        debt_data = []
        for debt_id, debt in technical_debts.items():
            debt_data.append({
                "ID": debt["id"],
                "Title": debt["title"],
                "Impact": debt.get("impact", "Unknown"),
                "Effort": debt.get("effort", "Unknown"),
                "Status": debt.get("status", "Unknown")
            })
        
        if debt_data:
            df = pd.DataFrame(debt_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Technical debt by status
            status_counts = df["Status"].value_counts()
            fig = px.bar(
                x=status_counts.index,
                y=status_counts.values,
                title="Technical Debt by Status",
                labels={"x": "Status", "y": "Count"}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No technical debt data found")
    else:
        st.info("No technical debts available")
