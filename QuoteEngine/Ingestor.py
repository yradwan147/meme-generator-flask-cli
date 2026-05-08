"""Facade that picks the right ingestor by file extension."""
from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from .CSVIngestor import CSVIngestor
from .TXTIngestor import TXTIngestor
from .DocxIngestor import DocxIngestor
from .PDFIngestor import PDFIngestor


class Ingestor(IngestorInterface):
    """Single entry point for parsing any supported quote file.

    ``Ingestor`` realises the *strategy + facade* design pattern: it
    iterates over the registered concrete ingestors
    (:class:`CSVIngestor`, :class:`TXTIngestor`, :class:`DocxIngestor`,
    :class:`PDFIngestor`) and delegates ``parse`` to the first one
    whose ``can_ingest`` returns ``True`` for the given path. Callers
    therefore never need to know which concrete class handles which
    extension.
    """

    ingestors = [CSVIngestor, TXTIngestor, DocxIngestor, PDFIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Dispatch ``path`` to the first concrete ingestor that handles it.

        Args:
            path: Path to a quote file in any supported format
                (``.csv``, ``.txt``, ``.docx``, ``.pdf``).

        Returns:
            A list of :class:`QuoteModel` parsed by the chosen concrete
            ingestor.

        Raises:
            ValueError: If no registered concrete ingestor can handle
                the extension of ``path``.
        """
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f"No ingestor for {path}")
