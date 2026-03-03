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
from app.models.document_models import Document
from app.schemas.document_schemas import Document as DocumentSchema
from app.services.document_service import process_document

from app.core.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=DocumentSchema)
async def upload_document(
    title: str = Form(...),
    description: str = Form(None),
    is_public: bool = Form(False),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    # current_user: User = Depends(get_current_active_user) # Add authentication later
):
    """
    Upload a new document (PDF or TXT).

    Saves file, creates database record with status PENDING, and triggers background processing.
    """
    # Validate file extension
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower().lstrip('.')
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type .{ext} not allowed. Allowed types are: {', '.join(settings.ALLOWED_EXTENSIONS)}",
        )

    # Read file content and check size
    contents = await file.read()
    size = len(contents)
    if size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE // 1024 // 1024}MB",
        )

    # Create a unique filename and save the file
    os.makedirs(settings.DOCUMENTS_DIR, exist_ok=True)
    unique_name = f"{uuid4()}_{filename}"
    dest_path = os.path.join(settings.DOCUMENTS_DIR, unique_name)
    with open(dest_path, "wb") as f:
        f.write(contents)

    # Create a new document record in the database
    new_doc = Document(
        # owner_id=current_user.id, # Add user association later
        owner_id=uuid4(), # Placeholder for now
        title=title,
        description=description,
        file_path=dest_path,
        file_name=filename,
        file_size=size,
        file_type=ext,
        status='pending',
        is_public=is_public,
    )
    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)

    # Schedule background task for document processing
    background_tasks.add_task(process_document, new_doc.id)

    return new_doc

# ... other document-related endpoints (list, get, delete) will be added here ...
