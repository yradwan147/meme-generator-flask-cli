"""Ingestor for .docx quote files (uses python-docx)."""
from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class DocxIngestor(IngestorInterface):
    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest {path}")
        # Imported lazily so a missing optional dep doesn't crash the
        # package when other ingestors are still usable.
        try:
            import docx
        except ImportError as e:
            raise ImportError(
                "DocxIngestor needs python-docx (pip install python-docx)"
            ) from e

        quotes: List[QuoteModel] = []
        document = docx.Document(path)
        for para in document.paragraphs:
            text = para.text.strip()
            if not text or ' - ' not in text:
                continue
            body, author = text.rsplit(' - ', 1)
            quotes.append(QuoteModel(body, author))
        return quotes
