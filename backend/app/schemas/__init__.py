"""
Pydantic models for request/response schemas
Provides data validation and documentation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# ========================
# Auth Schemas
# ========================

class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Request to refresh access token"""
    refresh_token: str


# ========================
# User Schemas
# ========================

class UserBase(BaseModel):
    """Base user data"""
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    """User creation request"""
    pass


class UserResponse(UserBase):
    """User response (public data only)"""
    id: UUID
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ========================
# Document Schemas
# ========================

class DocumentBase(BaseModel):
    """Base document data"""
    title: str
    description: Optional[str] = None
    is_public: bool = False


class DocumentCreate(DocumentBase):
    """Document creation request"""
    pass


class DocumentResponse(DocumentBase):
    """Document response"""
    id: UUID
    owner_id: UUID
    file_name: str
    file_size: int
    file_type: str
    status: str
    created_at: datetime
    processed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ========================
# Search & Query Schemas
# ========================

class SearchQuery(BaseModel):
    """Search request"""
    query: str = Field(..., min_length=1, max_length=500)
    max_results: int = Field(10, ge=1, le=50)
    threshold: float = Field(0.5, ge=0.0, le=1.0)  # Similarity threshold


class SearchResult(BaseModel):
    """Single search result"""
    document_id: UUID
    document_title: str
    chunk_index: int
    content: str
    similarity_score: float


class SearchResponse(BaseModel):
    """Search response"""
    results: List[SearchResult]
    total_count: int
    query_time_ms: int


# ========================
# Conversation Schemas
# ========================

class MessageCreate(BaseModel):
    """Chat message request"""
    content: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[UUID] = None


class MessageResponse(BaseModel):
    """Chat message response"""
    id: UUID
    session_id: UUID
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationCreate(BaseModel):
    """Conversation session creation"""
    title: Optional[str] = None


class ConversationResponse(BaseModel):
    """Conversation session response"""
    id: UUID
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True
