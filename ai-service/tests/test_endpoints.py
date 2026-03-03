from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

@patch("app.services.processing_service.process_document")
def test_process_document_endpoint(mock_process_document):
    """
    Tests the /process endpoint.
    """
    mock_process_document.return_value = [{"content": "chunk1", "embedding": [0.1, 0.2]}]
    
    response = client.post("/process", json={"file_path": "test.txt"})
    
    assert response.status_code == 200
    assert response.json() == [{"content": "chunk1", "embedding": [0.1, 0.2]}]

@patch("app.services.llm_service.generate_response")
def test_generate_endpoint(mock_generate_response):
    """
    Tests the /generate endpoint.
    """
    mock_generate_response.return_value = "This is a generated response."
    
    response = client.post("/generate", json={"query": "What is the meaning of life?", "context": ["chunk1", "chunk2"]})
    
    assert response.status_code == 200
    assert response.json() == {"response": "This is a generated response."}
