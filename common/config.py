from dataclasses import dataclass
from pathlib import Path
import os
from typing import Union

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv is optional in some deployments
    pass


@dataclass
class Settings:
    """Application settings.

    Minimal wrapper around environment values. `DATA_DIR` is a `Path`
    for convenient filesystem operations.
    """

    PROJECT_NAME: str = "Enterprise GenAI Platform"
    DATA_DIR: Path = Path(os.getenv("DATA_DIR", "data"))
    ENV: str = os.getenv("ENV", "dev")

    # Neo4j AuraDB settings
    NEO4J_URI: str = os.getenv("NEO4J_URI", "")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "")

    def ensure_data_dir(self) -> Path:
        """Create `DATA_DIR` if it doesn't exist and return the Path."""
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        return self.DATA_DIR


settings = Settings()
