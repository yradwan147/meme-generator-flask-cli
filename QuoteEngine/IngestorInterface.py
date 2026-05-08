"""Abstract base class for all quote-file ingestors."""
from abc import ABC, abstractmethod
from typing import List

from .QuoteModel import QuoteModel


class IngestorInterface(ABC):
    """Each concrete ingestor handles exactly one file extension."""

    allowed_extensions: List[str] = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return True iff `path` ends with one of `allowed_extensions`."""
        ext = path.rsplit('.', 1)[-1].lower()
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse the given file and return a list of QuoteModel."""
        ...
