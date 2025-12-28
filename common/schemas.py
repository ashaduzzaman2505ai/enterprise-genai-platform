from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class DocumentSchema(BaseModel):
    """Schema representing a document to be chunked or indexed.

    Fields are intentionally simple and permissive to allow different
    ingestion sources to attach arbitrary metadata.
    """

    content: str = Field(..., description="Text content of the document")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    id: Optional[str] = Field(None, description="Optional document identifier")
