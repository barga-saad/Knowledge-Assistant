import pytest
from unittest.mock import patch, AsyncMock
from app.services.processing_service import process_document, read_document, chunk_text

@pytest.mark.asyncio
@patch("app.services.processing_service.read_document", new_callable=AsyncMock)
async def test_process_document(mock_read_document):
    """ 
    Tests that the process_document function correctly calls the read_document and generate_embedding functions.
    """
    mock_read_document.return_value = "This is a test document."
    
    with patch("app.services.embedding_service.generate_embedding", new_callable=AsyncMock) as mock_generate_embedding:
        mock_generate_embedding.return_value = [0.1, 0.2, 0.3]
        
        processed_chunks = await process_document("test.txt")
        
        assert len(processed_chunks) > 0
        assert "content" in processed_chunks[0]
        assert "embedding" in processed_chunks[0]

@pytest.mark.asyncio
async def test_read_document_txt():
    """
    Tests that the read_document function correctly reads a TXT file.
    """
    with open("test.txt", "w") as f:
        f.write("This is a test document.")
        
    text = await read_document("test.txt")
    assert text == "This is a test document."

@pytest.mark.asyncio
async def test_read_document_pdf():
    """
    Tests that the read_document function correctly reads a PDF file.
    """
    # Create a dummy PDF file
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter

    c = canvas.Canvas("test.pdf", pagesize=letter)
    c.drawString(100, 750, "This is a test PDF document.")
    c.save()

    text = await read_document("test.pdf")
    assert "This is a test PDF document." in text

def test_chunk_text():
    """
    Tests that the chunk_text function correctly chunks the text.
    """
    text = "This is a test document. " * 100
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    
    assert len(chunks) > 0
    assert len(chunks[0]) == 100
