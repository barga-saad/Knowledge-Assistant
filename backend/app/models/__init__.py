"""
SQLAlchemy ORM models
Defines database table structures
"""

from sqlalchemy import (
    Column, String, Boolean, Integer, BigInteger, Text,
    ForeignKey, TIMESTAMP, Enum, DateTime, JSON, func
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func as sqla_func
from pgvector.sqlalchemy import Vector

from app.core.database import Base
from datetime import datetime, timezone
import uuid
import enum


# ========================
# Enums
# ========================

class UserRole(str, enum.Enum):
    """User roles"""
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"


class DocumentStatus(str, enum.Enum):
    """Document processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ActionType(str, enum.Enum):
    """Audit log action types"""
    LOGIN = "login"
    LOGOUT = "logout"
    UPLOAD_DOCUMENT = "upload_document"
    DELETE_DOCUMENT = "delete_document"
    SEARCH = "search"
    EXPORT = "export"


# ========================
# User Model
# ========================

class User(Base):
    """User entity - synced with Keycloak"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    keycloak_id = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    documents = relationship("Document", back_populates="owner", cascade="all, delete-orphan")
    search_queries = relationship("SearchQuery", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user")
    conversations = relationship("ConversationSession", back_populates="user", cascade="all, delete-orphan")
    permissions = relationship("Permission", back_populates="user", cascade="all, delete-orphan")


# ========================
# Document Model
# ========================

class Document(Base):
    """Document entity - uploaded files"""
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    file_path = Column(String(512), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    file_type = Column(String(50), nullable=False)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.PENDING, index=True)
    content_hash = Column(String(255), index=True)
    metadata = Column(JSONB)
    is_public = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    processed_at = Column(TIMESTAMP(timezone=True))
    
    # Relationships
    owner = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    permissions = relationship("Permission", back_populates="document", cascade="all, delete-orphan")


# ========================
# Document Chunks Model
# ========================

class DocumentChunk(Base):
    """Document chunks with embeddings for semantic search"""
    __tablename__ = "document_chunks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    content_length = Column(Integer)
    # Vector embedding - 1536 dimensions (standard for embeddings)
    embedding = Column(Vector(1536))
    metadata = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    document = relationship("Document", back_populates="chunks")


# ========================
# Search Queries Model
# ========================

class SearchQuery(Base):
    """Search history and analytics"""
    __tablename__ = "search_queries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    query_text = Column(Text, nullable=False)
    results_count = Column(Integer, default=0)
    response_time_ms = Column(Integer)
    is_satisfied = Column(Boolean)
    feedback_text = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    
    # Relationships
    user = relationship("User", back_populates="search_queries")


# ========================
# Audit Log Model
# ========================

class AuditLog(Base):
    """Audit trail for compliance and debugging"""
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), index=True)
    action = Column(Enum(ActionType), nullable=False, index=True)
    resource_type = Column(String(50))
    resource_id = Column(UUID(as_uuid=True))
    details = Column(JSONB)
    ip_address = Column(String(45))
    user_agent = Column(String(512))
    status_code = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")


# ========================
# Conversation Session Model
# ========================

class ConversationSession(Base):
    """Multi-turn conversation sessions"""
    __tablename__ = "conversation_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255))
    is_archived = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("ConversationMessage", back_populates="session", cascade="all, delete-orphan")


# ========================
# Conversation Message Model
# ========================

class ConversationMessage(Base):
    """Individual messages in conversations"""
    __tablename__ = "conversation_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("conversation_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer)
    referenced_documents = Column(JSONB)  # List of document IDs
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    session = relationship("ConversationSession", back_populates="messages")


# ========================
# Permission Model
# ========================

class Permission(Base):
    """Fine-grained access control"""
    __tablename__ = "permissions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    permission_type = Column(String(50), nullable=False)  # "view", "edit", "delete", etc.
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user = relationship("User", back_populates="permissions")
    document = relationship("Document", back_populates="permissions")
