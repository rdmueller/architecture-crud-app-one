"""FastAPI dependencies."""
import os
from functools import lru_cache

from src.data.repository import ArchitectureRepository


@lru_cache()
def get_repository() -> ArchitectureRepository:
    """Get repository instance."""
    # Get data file path from environment or use default
    data_file = os.environ.get("ARCHITECTURE_DATA_FILE", "data/architecture.json")
    return ArchitectureRepository(data_file)
