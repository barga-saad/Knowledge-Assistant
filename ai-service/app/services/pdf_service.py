import logging
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file.
    """
    try:
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            text = "".join(page.extract_text() for page in reader.pages)
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF {file_path}: {e}")
        return ""
