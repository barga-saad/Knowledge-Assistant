from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.api_models import ProcessResponse, GenerateRequest, GenerateResponse
from app.services.processing_service import process_document
from app.services.llm_service import generate_response

router = APIRouter()

@router.post("/process", response_model=ProcessResponse)
async def process_document_endpoint(file: UploadFile = File(...)):
    try:
        chunks = await process_document(file.file, file.filename)
        return ProcessResponse(chunks=chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate", response_model=GenerateResponse)
async def generate_endpoint(request: GenerateRequest):
    try:
        response = await generate_response(request.query, request.context)
        return GenerateResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
