from typing import Optional
from pydantic import BaseModel, Field


class RagMetadata(BaseModel):
    org_id: Optional[str] = None


class RagDocumentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    category: Optional[str] = None
    metadata: Optional[RagMetadata] = None
