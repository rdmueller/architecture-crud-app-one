"""Export routes for architecture documentation."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from typing import Dict, Any
import zipfile
import io
import json
from datetime import datetime

from src.api.dependencies import get_repository
from src.data.repository import ArchitectureRepository
from src.generator.generator import AsciiDocGenerator

router = APIRouter(prefix="/export", tags=["export"])

# Initialize generator
generator = AsciiDocGenerator()


@router.get("/asciidoc")
async def export_asciidoc(repository: ArchitectureRepository = Depends(get_repository)) -> Response:
    """Export architecture data as AsciiDoc."""
    try:
        data = repository.load()
        asciidoc_content = generator.generate(data)
        
        return Response(
            content=asciidoc_content,
            media_type="text/plain",
            headers={
                "Content-Disposition": f'attachment; filename="architecture_{datetime.now().strftime("%Y%m%d")}.adoc"'
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/json")
async def export_json(repository: ArchitectureRepository = Depends(get_repository)) -> Response:
    """Export architecture data as JSON."""
    try:
        data = repository.load()
        json_content = json.dumps(data, indent=2)
        
        return Response(
            content=json_content,
            media_type="application/json",
            headers={
                "Content-Disposition": f'attachment; filename="architecture_{datetime.now().strftime("%Y%m%d")}.json"'
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/zip")
async def export_zip(repository: ArchitectureRepository = Depends(get_repository)) -> Response:
    """Export architecture data as ZIP archive."""
    try:
        data = repository.load()
        
        # Create ZIP in memory
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add JSON file
            json_content = json.dumps(data, indent=2)
            zip_file.writestr('architecture.json', json_content)
            
            # Add AsciiDoc file
            asciidoc_content = generator.generate(data)
            zip_file.writestr('architecture.adoc', asciidoc_content)
            
            # Add individual chapters
            if "adrs" in data:
                adrs_content = generator.generate_adrs(data["adrs"])
                zip_file.writestr('chapters/adrs.adoc', adrs_content)
            
            if "qualities" in data:
                qualities_content = generator.generate_qualities(data["qualities"])
                zip_file.writestr('chapters/qualities.adoc', qualities_content)
            
            if "risks" in data:
                risks_content = generator.generate_risks(data["risks"])
                zip_file.writestr('chapters/risks.adoc', risks_content)
            
            if "technicalDebts" in data:
                debts_content = generator.generate_technical_debts(data["technicalDebts"])
                zip_file.writestr('chapters/technical_debts.adoc', debts_content)
            
            if "components" in data:
                components_content = generator.generate_components(data["components"])
                zip_file.writestr('chapters/components.adoc', components_content)
            
            # Add relationships matrix
            relationships_content = generator.generate_relationships_matrix(data)
            zip_file.writestr('chapters/relationships.adoc', relationships_content)
            
            # Add README
            readme_content = f"""Architecture Documentation Export
================================

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Contents:
- architecture.json: Raw architecture data in JSON format
- architecture.adoc: Complete architecture documentation in AsciiDoc format
- chapters/: Individual chapters as separate AsciiDoc files

Usage:
1. Open architecture.adoc with any AsciiDoc viewer/editor
2. Convert to PDF/HTML using asciidoctor:
   asciidoctor architecture.adoc
   asciidoctor-pdf architecture.adoc

The individual chapters can be included in your own documentation structure.
"""
            zip_file.writestr('README.txt', readme_content)
        
        zip_buffer.seek(0)
        
        return Response(
            content=zip_buffer.getvalue(),
            media_type="application/zip",
            headers={
                "Content-Disposition": f'attachment; filename="architecture_export_{datetime.now().strftime("%Y%m%d")}.zip"'
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")
