"""FastAPI dependencies."""
import os
from functools import lru_cache

from src.data.repository import ArchitectureRepository


@lru_cache()
def get_repository() -> ArchitectureRepository:
    """Get repository instance."""
    print("get_repository called")
    """Get repository instance."""
    # Get data file path from environment or use default
    data_file = os.environ.get("ARCHITECTURE_DATA_FILE", "data/architecture.json")
    # Convert to absolute path if not already
    if not os.path.isabs(data_file):
        data_file = os.path.abspath(data_file)
    print(f"Using data file: {data_file}")
    return ArchitectureRepository(data_file)
