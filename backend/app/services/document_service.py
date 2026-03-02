"""
Business logic for document processing (Phase 2)
"""
import os
from typing import List
from app.models import Document, DocumentChunk, DocumentStatus
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import uuid4


def chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
    """Split text into chunks of roughly chunk_size characters."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end
    return chunks


async def process_document(document: Document, db: AsyncSession):
    """Read saved file, split into chunks, store in DocumentChunk table.
    Update status accordingly.
    """
    document.status = DocumentStatus.PROCESSING
    await db.commit()
    await db.refresh(document)

    try:
        # read file
        with open(document.file_path, "r", encoding="utf-8", errors="ignore") as f:
            contents = f.read()

        chunks = chunk_text(contents)
        # remove previous chunks if any
        await db.execute(
            "DELETE FROM document_chunks WHERE document_id = :id",
            {"id": str(document.id)}
        )

        for idx, chunk in enumerate(chunks):
            doc_chunk = DocumentChunk(
                document_id=document.id,
                chunk_index=idx,
                content=chunk,
                content_length=len(chunk),
            )
            db.add(doc_chunk)

        document.status = DocumentStatus.COMPLETED
        document.processed_at = None  # set timestamp later if needed
        await db.commit()
    except Exception:
        document.status = DocumentStatus.FAILED
        await db.commit()
        raise
