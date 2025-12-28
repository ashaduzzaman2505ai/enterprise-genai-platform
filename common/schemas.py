from pydantic import BaseModel
from typing import Dict, Any

class DocumentSchema(BaseModel):
    content: str
    metadata: Dict[str, Any]
