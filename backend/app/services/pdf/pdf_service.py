import fitz
from typing import Tuple
from ...core.logging import get_logger

logger = get_logger(__name__)


class PDFService:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> Tuple[str, int, int, int]:
        try:
            doc = fitz.open(pdf_path)
            page_count = len(doc)
            full_text = ""
            for page in doc:
                text = page.get_text()
                full_text += text + "\n"

            cleaned_text = PDFService._clean_text(full_text)
            word_count = len(cleaned_text.split())
            character_count = len(cleaned_text)
            doc.close()

            logger.info(
                "PDF extracted successfully",
                page_count=page_count,
                word_count=word_count,
                character_count=character_count,
            )

            return cleaned_text, page_count, word_count, character_count
        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {e}")
            raise e

    @staticmethod
    def extract_pages_from_pdf(pdf_path: str) -> list[dict]:
        try:
            doc = fitz.open(pdf_path)
            pages = []
            for i, page in enumerate(doc):
                text = page.get_text()
                cleaned = PDFService._clean_text(text)
                if cleaned:
                    pages.append({
                        "page_number": i + 1,
                        "text": cleaned
                    })
            doc.close()
            return pages
        except Exception as e:
            logger.error(f"Failed to extract pages from PDF: {e}")
            raise e

    @staticmethod
    def _clean_text(text: str) -> str:
        # Remove extra whitespace
        lines = text.splitlines()
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        return "\n".join(cleaned_lines)
