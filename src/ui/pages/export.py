"""Export page for Architecture CRUD application."""
import streamlit as st
import requests
import json
import zipfile
import io
from typing import Dict, Any
from datetime import datetime

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


def export_asciidoc(data: Dict[str, Any]) -> str:
    """Export architecture data as AsciiDoc."""
    # TODO: This should call the backend API endpoint for AsciiDoc generation
    # For now, creating a basic template
    
    asciidoc = []
    asciidoc.append("= Architecture Documentation")
    asciidoc.append(f":toc:")
    asciidoc.append(f":date: {datetime.now().strftime('%Y-%m-%d')}")
    asciidoc.append("")
    
    # ADRs Section
    asciidoc.append("== Architecture Decision Records")
    asciidoc.append("")
    
    if "adrs" in data:
        for adr_id, adr in data["adrs"].items():
            asciidoc.append(f"=== {adr_id}: {adr.get('title', 'Untitled')}")
            asciidoc.append("")
            asciidoc.append(f"*Status:* {adr.get('status', 'Unknown')}")
            asciidoc.append(f"*Date:* {adr.get('date', 'Unknown')}")
            asciidoc.append(f"*Authors:* {', '.join(adr.get('authors', []))}")
            asciidoc.append("")
            
            if "context" in adr:
                asciidoc.append("==== Context")
                asciidoc.append(adr["context"])
                asciidoc.append("")
            
            if "decision" in adr:
                asciidoc.append("==== Decision")
                asciidoc.append(adr["decision"])
                asciidoc.append("")
            
            if "alternatives" in adr and adr["alternatives"]:
                asciidoc.append("==== Alternatives")
                for alt_name, alt_data in adr["alternatives"].items():
                    asciidoc.append(f"*{alt_name}*")
                    if "advantages" in alt_data:
                        asciidoc.append("Advantages:")
                        for adv in alt_data["advantages"]:
                            asciidoc.append(f"- {adv}")
                    if "disadvantages" in alt_data:
                        asciidoc.append("Disadvantages:")
                        for dis in alt_data["disadvantages"]:
                            asciidoc.append(f"- {dis}")
                    asciidoc.append("")
            
            asciidoc.append("")
    
    # Quality Requirements Section
    asciidoc.append("== Quality Requirements")
    asciidoc.append("")
    
    if "qualities" in data:
        for q_id, quality in data["qualities"].items():
            asciidoc.append(f"=== {q_id}: {quality.get('title', 'Untitled')}")
            asciidoc.append("")
            asciidoc.append(f"*Priority:* {quality.get('priority', 'Unknown')}")
            asciidoc.append("")
            
            if "description" in quality:
                asciidoc.append(quality["description"])
                asciidoc.append("")
            
            if "metrics" in quality and quality["metrics"]:
                asciidoc.append("==== Metrics")
                for metric in quality["metrics"]:
                    metric_line = f"- {metric.get('metricName', 'Unknown')}: "
                    metric_line += f"{metric.get('targetValue', 'N/A')} "
                    metric_line += f"{metric.get('unit', '')}"
                    asciidoc.append(metric_line)
                asciidoc.append("")
    
    # Risks Section
    asciidoc.append("== Risks")
    asciidoc.append("")
    
    if "risks" in data:
        for r_id, risk in data["risks"].items():
            asciidoc.append(f"=== {r_id}: {risk.get('title', 'Untitled')}")
            asciidoc.append("")
            asciidoc.append(f"*Impact:* {risk.get('impact', 'Unknown')}")
            asciidoc.append(f"*Likelihood:* {risk.get('likelihood', 'Unknown')}")
            asciidoc.append(f"*Status:* {risk.get('status', 'Unknown')}")
            asciidoc.append("")
            
            if "description" in risk:
                asciidoc.append(risk["description"])
                asciidoc.append("")
            
            if "mitigationStrategy" in risk:
                asciidoc.append("==== Mitigation Strategy")
                asciidoc.append(risk["mitigationStrategy"])
                asciidoc.append("")
    
    # Technical Debts Section
    asciidoc.append("== Technical Debts")
    asciidoc.append("")
    
    if "technicalDebts" in data:
        for td_id, debt in data["technicalDebts"].items():
            asciidoc.append(f"=== {td_id}: {debt.get('title', 'Untitled')}")
            asciidoc.append("")
            asciidoc.append(f"*Impact:* {debt.get('impact', 'Unknown')}")
            asciidoc.append(f"*Effort:* {debt.get('effort', 'Unknown')}")
            asciidoc.append(f"*Status:* {debt.get('status', 'Unknown')}")
            asciidoc.append("")
            
            if "description" in debt:
                asciidoc.append(debt["description"])
                asciidoc.append("")
            
            if "remediationPlan" in debt:
                asciidoc.append("==== Remediation Plan")
                asciidoc.append(debt["remediationPlan"])
                asciidoc.append("")
    
    # Components Section
    asciidoc.append("== Components")
    asciidoc.append("")
    
    if "components" in data:
        for c_id, component in data["components"].items():
            asciidoc.append(f"=== {c_id}: {component.get('title', 'Untitled')}")
            asciidoc.append("")
            
            if "responsibility" in component:
                asciidoc.append(f"*Responsibility:* {component['responsibility']}")
                asciidoc.append("")
            
            if "interfaces" in component and component["interfaces"]:
                asciidoc.append("==== Interfaces")
                for interface in component["interfaces"]:
                    asciidoc.append(f"- {interface}")
                asciidoc.append("")
            
            if "attributes" in component and component["attributes"]:
                asciidoc.append("==== Attributes")
                for attr, value in component["attributes"].items():
                    asciidoc.append(f"- {attr}: {value}")
                asciidoc.append("")
    
    return "\n".join(asciidoc)


def create_zip_export(data: Dict[str, Any]) -> bytes:
    """Create a ZIP file with all export formats."""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add JSON file
        json_data = json.dumps(data, indent=2)
        zip_file.writestr('architecture.json', json_data)
        
        # Add AsciiDoc file
        asciidoc_content = export_asciidoc(data)
        zip_file.writestr('architecture.adoc', asciidoc_content)
        
        # Add README
        readme_content = f"""Architecture Documentation Export
================================

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Contents:
- architecture.json: Raw architecture data in JSON format
- architecture.adoc: Architecture documentation in AsciiDoc format

Usage:
1. Open architecture.adoc with any AsciiDoc viewer/editor
2. Convert to PDF/HTML using asciidoctor:
   asciidoctor architecture.adoc
   asciidoctor-pdf architecture.adoc
"""
        zip_file.writestr('README.txt', readme_content)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def render_export():
    """Render the export page."""
    st.header("Export Architecture Documentation")
    
    # Fetch architecture data
    data = fetch_architecture_data()
    
    if not data:
        st.info("No architecture data available to export.")
        return
    
    # Export options
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Export Formats")
        
        # JSON Export
        st.markdown("### JSON Export")
        st.markdown("Export the complete architecture data in JSON format.")
        json_str = json.dumps(data, indent=2)
        st.download_button(
            label="Download JSON",
            data=json_str,
            file_name=f"architecture_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
        
        # AsciiDoc Export
        st.markdown("### AsciiDoc Export")
        st.markdown("Export documentation in AsciiDoc format.")
        asciidoc_content = export_asciidoc(data)
        st.download_button(
            label="Download AsciiDoc",
            data=asciidoc_content,
            file_name=f"architecture_{datetime.now().strftime('%Y%m%d')}.adoc",
            mime="text/plain"
        )
    
    with col2:
        st.subheader("Combined Export")
        
        # ZIP Export
        st.markdown("### ZIP Archive")
        st.markdown("Download all formats in a single ZIP file.")
        zip_data = create_zip_export(data)
        st.download_button(
            label="Download ZIP Archive",
            data=zip_data,
            file_name=f"architecture_export_{datetime.now().strftime('%Y%m%d')}.zip",
            mime="application/zip"
        )
        
        # Preview section
        st.markdown("### Preview")
        with st.expander("Preview AsciiDoc Export"):
            st.text(asciidoc_content[:1000] + "..." if len(asciidoc_content) > 1000 else asciidoc_content)
    
    # Export statistics
    st.markdown("### Export Statistics")
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    with stats_col1:
        st.metric("Total ADRs", len(data.get("adrs", {})))
        st.metric("Total Qualities", len(data.get("qualities", {})))
    
    with stats_col2:
        st.metric("Total Risks", len(data.get("risks", {})))
        st.metric("Total Technical Debts", len(data.get("technicalDebts", {})))
    
    with stats_col3:
        st.metric("Total Components", len(data.get("components", {})))
        
        # Calculate total relationships
        total_relationships = 0
        for entity_type, entities in data.items():
            for entity_id, entity_data in entities.items():
                if "relationships" in entity_data:
                    for rel_type, rel_list in entity_data["relationships"].items():
                        total_relationships += len(rel_list)
        
        st.metric("Total Relationships", total_relationships)
