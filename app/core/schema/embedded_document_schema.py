from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class EmbeddedDocumentMetadata(BaseModel):
    org_id: Optional[str] = None


class EmbeddedDocumentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    category: Optional[str] = None
    chunk_number: Optional[int] = None
    metadata: Optional[EmbeddedDocumentMetadata] = None
    embeddings: Optional[List[float]]


class EmbeddedDocumentResponse(BaseModel):
    id: str
    title: str
    content: str
    category: Optional[str] = None
    metadata: Optional[EmbeddedDocumentMetadata] = None


class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=3, ge=1, le=50)
    category: Optional[str] = None
    metadata: Optional[EmbeddedDocumentMetadata] = None


class SearchResult(BaseModel):
    id: str
    title: str
    content: str
    category: Optional[str] = None
    score: float
    chunk_number: Optional[int] = None
    metadata: Optional[EmbeddedDocumentMetadata] = None
