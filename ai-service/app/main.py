from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from app.api.endpoints import router

app = FastAPI(
    title="AI Service",
    description="Service for document processing, embeddings, and chat response generation.",
    version="0.1.0"
)

app.mount("/static", StaticFiles(directory="ui/static"), name="static")

app.include_router(router, prefix="/api")

@app.get("/")
async def read_root():
    return FileResponse('ui/index.html')
