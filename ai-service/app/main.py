"""
AI Service main application
Wraps Ollama and provides LLM endpoints
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

app = FastAPI(
    title="Knowledge Assistant AI Service",
    description="Local LLM service using Ollama",
    version="1.0.0",
)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/embed")
async def embed_text(text: str):
    """
    Generate embeddings for text using Ollama.
    
    This will be called when:
    - Uploading documents (embed chunks)
    - Searching (embed query)
    """
    # TODO: Call Ollama embedding endpoint
    pass


@app.post("/generate")
async def generate_response(prompt: str, context: str = None):
    """
    Generate text response using local LLM.
    
    Args:
        prompt: User question
        context: Retrieved document chunks (for RAG)
    
    Returns:
        Generated response from Llama2
    """
    # TODO: Call Ollama generation endpoint
    pass
