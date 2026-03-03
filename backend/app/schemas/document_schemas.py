from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    description: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(DocumentBase):
    pass

class DocumentInDBBase(DocumentBase):
    id: UUID4
    owner_id: UUID4
    file_path: str
    file_name: str
    file_size: int
    file_type: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Document(DocumentInDBBase):
    pass

class DocumentChunkBase(BaseModel):
    content: str
    metadata: Optional[dict] = None

class DocumentChunkCreate(DocumentChunkBase):
    document_id: UUID4
    chunk_index: int

class DocumentChunk(DocumentChunkBase):
    id: UUID4
    document_id: UUID4

    class Config:
        from_attributes = True
