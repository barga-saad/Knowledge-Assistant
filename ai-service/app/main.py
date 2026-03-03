from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(
    title="AI Service",
    description="Service for document processing, embeddings, and chat response generation.",
    version="0.1.0"
)

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "AI Service is running"}
