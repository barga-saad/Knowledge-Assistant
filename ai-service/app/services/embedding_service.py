import ollama

async def generate_embedding(text: str, model: str = "all-minilm") -> list[float]:
    """
    Generates an embedding for the given text using the specified Ollama model.
    """
    return ollama.embeddings(model=model, prompt=text)["embedding"]
