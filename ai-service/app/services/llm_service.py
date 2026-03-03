import logging
import ollama
from typing import List

logger = logging.getLogger(__name__)

def generate_response(query: str, context: List[str]) -> str:
    """
    Generates a response from the LLM based on a query and context.
    """
    # Prepare the prompt for the LLM
    prompt = f"""Answer the following question based on the provided context.

Context:
{'\n'.join(context)}

Question: {query}

Answer:"""

    try:
        response = ollama.chat(
            model="mistral",
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ]
        )
        return response['message']['content']
    except Exception as e:
        logger.error(f"Error generating response from LLM: {e}")
        return "Sorry, I couldn't generate a response."
