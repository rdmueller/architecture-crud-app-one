#!/usr/bin/env python3
"""
Script to generate AsciiDoc documentation from architecture.json
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

def load_architecture_data(json_path: str) -> Dict[str, Any]:
    """Load architecture data from JSON file"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_adr_chapter(data: Dict[str, Any]) -> str:
    """Generate ADR chapter in AsciiDoc format"""
    content = ["= Architekturentscheidungen\n"]
    
    for adr_id, adr in sorted(data.get('adrs', {}).items()):
        content.append(f"== {adr_id}: {adr['title']}\n")
        content.append(f"*Status*: {adr['status']}\n")
        content.append(f"*Datum*: {adr['date']}\n")
        content.append(f"*Autoren*: {', '.join(adr['authors'])}\n")
        content.append("\n=== Kontext und Problemstellung\n")
        content.append(f"{adr['context']}\n")
        
        if adr.get('decisionCriteria'):
            content.append("\n=== Entscheidungskriterien\n")
            for criterion in adr['decisionCriteria']:
                content.append(f"* {criterion}\n")
        
        if adr.get('alternatives'):
            content.append("\n=== Betrachtete Alternativen\n")
            for alt in adr['alternatives']:
                content.append(f"\n==== {alt['name']}\n")
                content.append(f"{alt['description']}\n")
                if alt.get('prosCons'):
                    if alt['prosCons'].get('pros'):
                        content.append("\n*Vorteile:*\n")
                        for pro in alt['prosCons']['pros']:
                            content.append(f"* {pro}\n")
                    if alt['prosCons'].get('cons'):
                        content.append("\n*Nachteile:*\n")
                        for con in alt['prosCons']['cons']:
                            content.append(f"* {con}\n")
        
        content.append(f"\n=== Entscheidung\n{adr['decision']}\n")
        
        # Add relationships section
        if adr.get('relationships'):
            content.append("\n=== Beziehungen\n")
            rel = adr['relationships']
            
            if rel.get('qualities'):
                content.append("\n.Beeinflusste Qualitätsanforderungen\n")
                content.append('[cols="1,1,3", options="header"]\n|===\n')
                content.append('| ID | Einfluss | Begründung\n')
                for q in rel['qualities']:
                    content.append(f"| {q['id']} | {q['impact']} | {q['rationale']}\n")
                content.append("|===\n")
            
            if rel.get('risks'):
                content.append("\n.Erzeugte Risiken\n")
                content.append('[cols="1,3", options="header"]\n|===\n')
                content.append('| ID | Begründung\n')
                for r in rel['risks']:
                    content.append(f"| {r['id']} | {r['rationale']}\n")
                content.append("|===\n")
        
        content.append("\n")
    
    return "".join(content)

def generate_quality_chapter(data: Dict[str, Any]) -> str:
    """Generate Quality Requirements chapter in AsciiDoc format"""
    content = ["= Qualitätsanforderungen\n\n"]
    
    # Create a priority matrix
    content.append('[cols="1,3,1", options="header"]\n|===\n')
    content.append('| ID | Qualitätsanforderung | Priorität\n')
    
    for q_id, quality in sorted(data.get('qualities', {}).items()):
        content.append(f"| {q_id} | {quality['title']} | {quality['priority']}\n")
    
    content.append("|===\n\n")
    
    # Add details for each quality requirement
    for q_id, quality in sorted(data.get('qualities', {}).items()):
        content.append(f"== {q_id}: {quality['title']}\n\n")
        content.append(f"{quality['description']}\n\n")
        
        if quality.get('metrics'):
            content.append("=== Metriken\n\n")
            for metric in quality['metrics']:
                content.append(f"* *{metric['name']}*: {metric['description']}\n")
                content.append(f"  ** Kriterium: {metric['criteria']}\n")
                content.append(f"  ** Zielwert: {metric['targetValue']}\n\n")
    
    return "".join(content)

def generate_risks_and_debts_chapter(data: Dict[str, Any]) -> str:
    """Generate Risks and Technical Debt chapter in AsciiDoc format"""
    content = ["= Risiken und technische Schulden\n\n"]
    
    # Risks section
    content.append("== Risiken\n\n")
    for r_id, risk in sorted(data.get('risks', {}).items()):
        content.append(f"=== {r_id}: {risk['title']}\n\n")
        content.append(f"{risk['description']}\n\n")
        content.append(f"* *Auswirkung*: {risk['impact']}\n")
        content.append(f"* *Eintrittswahrscheinlichkeit*: {risk['likelihood']}\n")
        content.append(f"* *Status*: {risk['status']}\n")
        if risk.get('mitigationStrategy'):
            content.append(f"* *Mitigationsstrategie*: {risk['mitigationStrategy']}\n")
        content.append("\n")
    
    # Technical Debt section
    content.append("== Technische Schulden\n\n")
    for td_id, debt in sorted(data.get('technicalDebts', {}).items()):
        content.append(f"=== {td_id}: {debt['title']}\n\n")
        content.append(f"{debt['description']}\n\n")
        content.append(f"* *Auswirkung*: {debt['impact']}\n")
        content.append(f"* *Behebungsaufwand*: {debt['remediationEffort']}\n")
        content.append(f"* *Status*: {debt['status']}\n")
        if debt.get('remediationPlan'):
            content.append(f"* *Behebungsplan*: {debt['remediationPlan']}\n")
        content.append("\n")
    
    return "".join(content)

def main():
    # Paths
    project_root = Path(__file__).parent.parent
    json_path = project_root / "docs" / "arc42" / "architecture.json"
    output_dir = project_root / "docs" / "arc42"
    
    # Load data
    print(f"Loading architecture data from {json_path}")
    data = load_architecture_data(str(json_path))
    
    # Generate chapters
    chapters = {
        "09_architecture_decisions": generate_adr_chapter(data),
        "10_quality_requirements": generate_quality_chapter(data),
        "11_risks_and_technical_debt": generate_risks_and_debts_chapter(data)
    }
    
    # Write chapters
    for chapter_dir, content in chapters.items():
        chapter_path = output_dir / chapter_dir / f"{chapter_dir.split('_', 1)[1]}.adoc"
        chapter_path.parent.mkdir(exist_ok=True)
        
        print(f"Writing {chapter_path}")
        with open(chapter_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("AsciiDoc generation complete!")

if __name__ == "__main__":
    main()
