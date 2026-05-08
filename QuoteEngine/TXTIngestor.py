"""Ingestor for plain-text quote files (one quote per line)."""
from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class TXTIngestor(IngestorInterface):
    """Each line is `body - author`."""

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest {path}")
        quotes: List[QuoteModel] = []
        # utf-8-sig swallows the BOM that Notepad and friends sometimes leave.
        with open(path, 'r', encoding='utf-8-sig') as f:
            for raw in f:
                line = raw.strip()
                if not line or ' - ' not in line:
                    continue
                body, author = line.rsplit(' - ', 1)
                quotes.append(QuoteModel(body, author))
        return quotes
