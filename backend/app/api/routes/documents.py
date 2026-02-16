"""
Document management endpoints
Upload, list, delete documents
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas import DocumentResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
):
    """
    List all documents for the authenticated user.
    
    Args:
        skip: Number of documents to skip (for pagination)
        limit: Maximum documents to return
    
    Returns:
        List of documents
    """
    # TODO: Implement with authentication
    return []


@router.post("/upload")
async def upload_document(
    db: AsyncSession = Depends(get_db),
):
    """
    Upload a new document (PDF or TXT).
    
    The document will be:
    1. Stored in file storage
    2. Parsed for content
    3. Chunks created and embedded
    4. Made searchable via vector DB
    """
    # TODO: Implement file upload
    pass


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get details of a specific document.
    """
    # TODO: Implement
    pass


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a document and all its chunks.
    """
    # TODO: Implement
    pass
