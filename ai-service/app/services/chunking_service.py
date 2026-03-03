import logging
from typing import List

logger = logging.getLogger(__name__)

# A simple chunking strategy - splitting by paragraphs
def chunk_text(text: str) -> List[str]:
    """
    Splits text into chunks based on paragraphs.
    """
    return [paragraph for paragraph in text.split("\n\n") if paragraph.strip()]
