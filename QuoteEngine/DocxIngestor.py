"""Ingestor for ``.docx`` quote files (uses python-docx)."""
from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class DocxIngestor(IngestorInterface):
    """Concrete ingestor for ``.docx`` files using ``python-docx``.

    Each paragraph in the document is treated as one candidate quote;
    paragraphs that don't contain the ``" - "`` body / author separator
    are silently skipped, so the same Word document can mix quote
    paragraphs with section headings or empty lines.
    """

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a ``.docx`` quote file.

        Args:
            path: Path to a ``.docx`` file.

        Returns:
            A list of :class:`QuoteModel` — one per paragraph that
            matched the ``body - author`` shape.

        Raises:
            ValueError: If ``path``'s extension is not ``.docx``.
            ImportError: If ``python-docx`` is not installed.
        """
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
