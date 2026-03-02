"""
Document management endpoints
Upload, list, delete documents
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import os
from uuid import uuid4

from app.core.config import settings
from app.models import Document, DocumentStatus
from app.services.document_service import process_document

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


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    title: str = Form(...),
    description: str = Form(None),
    is_public: bool = Form(False),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = Depends(),
):
    """
    Upload a new document (PDF or TXT).

    Saves file, creates database record with status PENDING.
    """
    # validate extension
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower().lstrip('.')
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type .{ext} not allowed",
        )

    contents = await file.read()
    size = len(contents)
    if size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large (max {settings.MAX_FILE_SIZE} bytes)",
        )

    # ensure directory exists
    os.makedirs(settings.DOCUMENTS_DIR, exist_ok=True)
    unique_name = f"{uuid4()}_{filename}"
    dest_path = os.path.join(settings.DOCUMENTS_DIR, unique_name)
    with open(dest_path, "wb") as f:
        f.write(contents)

    # create db record (owner not implemented yet)
    new_doc = Document(
        owner_id=uuid4(),
        title=title,
        description=description,
        file_path=dest_path,
        file_name=filename,
        file_size=size,
        file_type=ext,
        status=DocumentStatus.PENDING,
        is_public=is_public,
    )
    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)

    # schedule processing in background
    background_tasks.add_task(process_document, new_doc, db)

    return new_doc


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
