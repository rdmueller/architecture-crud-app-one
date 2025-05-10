"""Tests for the repository layer."""
import pytest
import json
import tempfile
import os
from datetime import date
from pathlib import Path

from src.data.repository import ArchitectureRepository
from src.api.models.architecture import Architecture, Metadata
from src.api.models.adr import ADR


class TestArchitectureRepository:
    """Test suite for ArchitectureRepository."""
    
    def setup_method(self):
        """Set up test environment."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.repo = ArchitectureRepository(self.temp_file.name)
    
    def teardown_method(self):
        """Clean up test environment."""
        # Remove temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_save_and_load_architecture(self):
        """Test saving and loading architecture data."""
        # Create test architecture
        architecture = Architecture(
            metadata=Metadata(
                title="Test Architecture",
                system="test-system",
                version="1.0.0",
                date=date(2024, 5, 10),
                authors=["Test Author"]
            ),
            adrs={
                "ADR-001": ADR(
                    id="ADR-001",
                    title="Test Decision",
                    status="accepted",
                    date=date(2024, 5, 10),
                    authors=["Test Author"],
                    context="Test context",
                    decision="Test decision",
                    relationships={
                        "qualities": [],
                        "risks": [],
                        "technicalDebts": [],
                        "components": [],
                        "relatedAdrs": []
                    }
                )
            }
        )
        
        # Save architecture
        self.repo.save(architecture)
        
        # Load architecture
        loaded = self.repo.load()
        
        assert loaded.metadata.title == "Test Architecture"
        assert loaded.metadata.system == "test-system"
        assert len(loaded.adrs) == 1
        assert "ADR-001" in loaded.adrs
        assert loaded.adrs["ADR-001"].title == "Test Decision"
    
    def test_load_empty_file(self):
        """Test loading from an empty file."""
        # Create empty file
        empty_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        empty_file.close()
        
        repo = ArchitectureRepository(empty_file.name)
        
        # Should load default empty architecture
        architecture = repo.load()
        
        assert architecture.metadata.title == "Architecture"
        assert architecture.metadata.system == "system"
        assert architecture.metadata.version == "1.0.0"
        assert architecture.adrs == {}
        assert architecture.qualities == {}
        
        # Clean up
        os.unlink(empty_file.name)
    
    def test_load_nonexistent_file(self):
        """Test loading from a non-existent file."""
        repo = ArchitectureRepository("nonexistent.json")
        
        # Should load default empty architecture
        architecture = repo.load()
        
        assert architecture.metadata.title == "Architecture"
        assert architecture.metadata.system == "system"
        assert architecture.metadata.version == "1.0.0"
    
    def test_add_adr(self):
        """Test adding an ADR to existing architecture."""
        # Load empty architecture
        architecture = self.repo.load()
        
        # Create new ADR
        adr = ADR(
            id="ADR-002",
            title="New Decision",
            status="proposed",
            date=date(2024, 5, 11),
            authors=["New Author"],
            context="New context",
            decision="New decision",
            relationships={
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        )
        
        # Add ADR
        self.repo.add_adr(adr)
        
        # Reload and verify
        loaded = self.repo.load()
        assert "ADR-002" in loaded.adrs
        assert loaded.adrs["ADR-002"].title == "New Decision"
    
    def test_update_adr(self):
        """Test updating an existing ADR."""
        # Create initial architecture with ADR
        architecture = Architecture(
            metadata=Metadata(
                title="Test Architecture",
                system="test-system",
                version="1.0.0",
                date=date(2024, 5, 10)
            ),
            adrs={
                "ADR-001": ADR(
                    id="ADR-001",
                    title="Original Title",
                    status="proposed",
                    date=date(2024, 5, 10),
                    authors=["Original Author"],
                    context="Original context",
                    decision="Original decision",
                    relationships={
                        "qualities": [],
                        "risks": [],
                        "technicalDebts": [],
                        "components": [],
                        "relatedAdrs": []
                    }
                )
            }
        )
        self.repo.save(architecture)
        
        # Update ADR
        updated_adr = ADR(
            id="ADR-001",
            title="Updated Title",
            status="accepted",
            date=date(2024, 5, 11),
            authors=["Updated Author"],
            context="Updated context",
            decision="Updated decision",
            relationships={
                "qualities": [],
                "risks": [],
                "technicalDebts": [],
                "components": [],
                "relatedAdrs": []
            }
        )
        
        self.repo.update_adr("ADR-001", updated_adr)
        
        # Reload and verify
        loaded = self.repo.load()
        assert loaded.adrs["ADR-001"].title == "Updated Title"
        assert loaded.adrs["ADR-001"].status == "accepted"
    
    def test_delete_adr(self):
        """Test deleting an ADR."""
        # Create initial architecture with ADR
        architecture = Architecture(
            metadata=Metadata(
                title="Test Architecture",
                system="test-system",
                version="1.0.0",
                date=date(2024, 5, 10)
            ),
            adrs={
                "ADR-001": ADR(
                    id="ADR-001",
                    title="To Be Deleted",
                    status="proposed",
                    date=date(2024, 5, 10),
                    authors=["Author"],
                    context="Context",
                    decision="Decision",
                    relationships={
                        "qualities": [],
                        "risks": [],
                        "technicalDebts": [],
                        "components": [],
                        "relatedAdrs": []
                    }
                )
            }
        )
        self.repo.save(architecture)
        
        # Delete ADR
        self.repo.delete_adr("ADR-001")
        
        # Reload and verify
        loaded = self.repo.load()
        assert "ADR-001" not in loaded.adrs
        assert len(loaded.adrs) == 0
    
    def test_get_adr(self):
        """Test getting a specific ADR."""
        # Create initial architecture with ADR
        architecture = Architecture(
            metadata=Metadata(
                title="Test Architecture",
                system="test-system",
                version="1.0.0",
                date=date(2024, 5, 10)
            ),
            adrs={
                "ADR-001": ADR(
                    id="ADR-001",
                    title="Test ADR",
                    status="accepted",
                    date=date(2024, 5, 10),
                    authors=["Author"],
                    context="Context",
                    decision="Decision",
                    relationships={
                        "qualities": [],
                        "risks": [],
                        "technicalDebts": [],
                        "components": [],
                        "relatedAdrs": []
                    }
                )
            }
        )
        self.repo.save(architecture)
        
        # Get ADR
        adr = self.repo.get_adr("ADR-001")
        assert adr is not None
        assert adr.title == "Test ADR"
        
        # Try to get non-existent ADR
        non_existent = self.repo.get_adr("ADR-999")
        assert non_existent is None
