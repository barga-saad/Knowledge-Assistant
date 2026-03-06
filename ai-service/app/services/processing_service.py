from app.services.embedding_service import generate_embedding
import PyPDF2
import io

async def process_document(file_stream: io.BytesIO, file_name: str):
    """
    Reads a document from a file stream, splits it into chunks, and generates embeddings for each chunk.
    """
    text = await read_document(file_stream, file_name)
    chunks = chunk_text(text)
    
    processed_chunks = []
    for chunk_content in chunks:
        embedding = await generate_embedding(chunk_content)
        processed_chunks.append({"content": chunk_content, "embedding": embedding})
        
    return processed_chunks

async def read_document(file_stream: io.BytesIO, file_name: str) -> str:
    """
    Reads the content of a file (PDF or TXT) and returns it as a string.
    """
    if file_name.lower().endswith('.pdf'):
        return await read_pdf(file_stream)
    else:
        return await read_txt(file_stream)

async def read_pdf(file_stream: io.BytesIO) -> str:
    """
    Reads the text content of a PDF file.
    """
    reader = PyPDF2.PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

async def read_txt(file_stream: io.BytesIO) -> str:
    """
    Reads the content of a text file.
    """
    return file_stream.read().decode("utf-8")

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """
    Splits the text into chunks of a specified size with a given overlap.
    """
    if not text:
        return []
        
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
