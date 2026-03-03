import logging
from sentence_transformers import SentenceTransformer
from typing import List

logger = logging.getLogger(__name__)

# Load the pre-trained model
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of texts.
    """
    return model.encode(texts).tolist()

def generate_embedding(text: str) -> List[float]:
    """
    Generates an embedding for a single text.
    """
    return model.encode(text).tolist()
