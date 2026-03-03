from fastapi import APIRouter, HTTPException
from app.models.api_models import ProcessRequest, ProcessResponse, EmbedRequest, EmbedResponse, GenerateRequest, GenerateResponse
from app.services.processing_service import process_document
from app.services.embedding_service import generate_embedding
from app.services.llm_service import generate_response

router = APIRouter()

@router.post("/process", response_model=ProcessResponse)
async def process_document_endpoint(request: ProcessRequest):
    try:
        chunks = await process_document(request.file_path)
        return ProcessResponse(chunks=chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/embed", response_model=EmbedResponse)
async def embed_endpoint(request: EmbedRequest):
    try:
        embedding = await generate_embedding(request.text)
        return EmbedResponse(embedding=embedding)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate", response_model=GenerateResponse)
async def generate_endpoint(request: GenerateRequest):
    try:
        response = await generate_response(request.query, request.context)
        return GenerateResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
