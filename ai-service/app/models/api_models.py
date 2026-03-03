from pydantic import BaseModel
from typing import List

class ProcessRequest(BaseModel):
    file_path: str

class Chunk(BaseModel):
    content: str
    embedding: List[float]

class ProcessResponse(BaseModel):
    chunks: List[Chunk]

class EmbedRequest(BaseModel):
    text: str

class EmbedResponse(BaseModel):
    embedding: List[float]

class GenerateRequest(BaseModel):
    query: str
    context: List[str]

class GenerateResponse(BaseModel):
    response: str
