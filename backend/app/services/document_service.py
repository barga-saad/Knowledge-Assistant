import logging
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document_models import Document, DocumentChunk
from app.core.database import SessionLocal
from app.core.config import settings
import asyncio

logger = logging.getLogger(__name__)

async def process_document(document_id: str):
    """
    Background task to process a document: extract text, create chunks, and generate embeddings.
    """
    logger.info(f"Starting processing for document {document_id}")

    async with SessionLocal() as db:
        try:
            document = await db.get(Document, document_id)
            if not document:
                logger.error(f"Document {document_id} not found for processing.")
                return

            document.status = 'processing'
            await db.commit()
            logger.info(f"Document {document_id} status updated to processing.")

            ai_service_url = f"{settings.AI_SERVICE_URL}/process"
            async with httpx.AsyncClient() as client:
                response = await client.post(ai_service_url, json={"file_path": document.file_path})
                response.raise_for_status() 
                data = response.json()

            for chunk_data in data['chunks']:
                chunk = DocumentChunk(
                    content=chunk_data['content'],
                    embedding=chunk_data['embedding'],
                    document_id=document_id
                )
                db.add(chunk)

            document.status = 'completed'
            await db.commit()
            logger.info(f"Successfully processed document {document_id}")

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred while processing document {document_id}: {e.response.text}")
            await db.rollback()
            document.status = 'failed'
            await db.commit()
        except Exception as e:
            logger.error(f"Error processing document {document_id}: {e}")
            await db.rollback()
            document.status = 'failed'
            await db.commit()
