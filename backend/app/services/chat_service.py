import logging
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models.document_models import DocumentChunk
from app.core.config import settings
from pgvector.sqlalchemy import l2_distance

logger = logging.getLogger(__name__)

async def get_chat_response(db: AsyncSession, query: str, user_id: str):
    """
    Handles the chat logic: gets a query embedding, finds relevant chunks, and generates a response.
    """
    try:
        # 1. Get embedding for the user's query from the AI service
        ai_service_url = f"{settings.AI_SERVICE_URL}/embed"
        async with httpx.AsyncClient() as client:
            response = await client.post(ai_service_url, json={"text": query})
            response.raise_for_status()
            query_embedding = response.json()['embedding']

        # 2. Find relevant document chunks using similarity search
        # Only search documents owned by the user
        stmt = (
            select(DocumentChunk)
            .options(joinedload(DocumentChunk.document))
            .join(DocumentChunk.document)
            .where(Document.owner_id == user_id)
            .order_by(l2_distance(DocumentChunk.embedding, query_embedding))
            .limit(5)
        )
        result = await db.execute(stmt)
        relevant_chunks = result.scalars().all()

        context = [chunk.content for chunk in relevant_chunks]

        # 3. Generate a response using the AI service
        ai_service_url = f"{settings.AI_SERVICE_URL}/generate"
        async with httpx.AsyncClient() as client:
            response = await client.post(ai_service_url, json={"query": query, "context": context})
            response.raise_for_status()
            chat_response = response.json()['response']

        return chat_response

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error occurred during chat: {e.response.text}")
        return "Sorry, there was an error with the AI service."
    except Exception as e:
        logger.error(f"An unexpected error occurred during chat: {e}")
        return "An unexpected error occurred."
