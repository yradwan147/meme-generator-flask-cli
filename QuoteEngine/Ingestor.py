"""Facade that picks the right ingestor by file extension."""
from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel
from .CSVIngestor import CSVIngestor
from .TXTIngestor import TXTIngestor
from .DocxIngestor import DocxIngestor
from .PDFIngestor import PDFIngestor


class Ingestor(IngestorInterface):
    """Delegates `parse` to the first concrete ingestor that can handle
    the file extension. Concrete ingestors live next to this file."""

    ingestors = [CSVIngestor, TXTIngestor, DocxIngestor, PDFIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f"No ingestor for {path}")
