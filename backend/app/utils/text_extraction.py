from io import BytesIO
import pdfplumber
from docx import Document

class UnsupportedFileType(Exception):
    pass

def extract_text_from_file(file_bytes: bytes, content_type: str) -> str:
    """
    Extract raw text from supported resume file types.

    Args:
        file_bytes (bytes): Raw file content.
        content_type (str): MIME type of the file.

    Returns:
        str: Extracted raw text.

    Raises:
        UnsupportedFileType: If file type is not supported.
        ValueError: If extraction fails.
    """
    if content_type == "application/pdf":
        return _extract_from_pdf(file_bytes)

    elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return _extract_from_docx(file_bytes)

    else:
        raise UnsupportedFileType(f"Unsupported file type: {content_type}")

def _extract_from_pdf(file_bytes: bytes) -> str:
    try:
        text_chunks = []

        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_chunks.append(page_text)

        return "\n".join(text_chunks).strip()

    except Exception as e:
        raise ValueError(f"Failed to extract PDF text: {e}")

def _extract_from_docx(file_bytes: bytes) -> str:
    try:
        doc = Document(BytesIO(file_bytes))
        text_chunks = [para.text for para in doc.paragraphs if para.text]
        return "\n".join(text_chunks).strip()

    except Exception as e:
        raise ValueError(f"Failed to extract DOCX text: {e}")
