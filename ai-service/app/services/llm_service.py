import ollama

async def generate_response(query: str, context: list[str], model: str = "llama2") -> str:
    """
    Generates a response to a query using the given context and Ollama model.
    """
    prompt = f"""Use the following context to answer the user's query.

Context:
{''.join(context)}

Query: {query}
"""
    
    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Use the provided context to answer the user's query."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    return response["message"]["content"]
