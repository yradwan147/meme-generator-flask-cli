"""Abstract base class for all quote-file ingestors."""
from abc import ABC, abstractmethod
from typing import List

from .QuoteModel import QuoteModel


class IngestorInterface(ABC):
    """Strategy contract for parsing one quote-file format.

    Concrete subclasses (``TXTIngestor``, ``DocxIngestor`` etc.) declare
    the file extensions they handle in ``allowed_extensions`` and
    implement ``parse`` to return a list of :class:`QuoteModel`.
    ``Ingestor`` (the facade) consults each subclass's ``can_ingest`` and
    delegates ``parse`` to the first match.
    """

    allowed_extensions: List[str] = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Return True iff this ingestor handles ``path``'s file type.

        Args:
            path: Path to the candidate quote file.

        Returns:
            ``True`` if the lowercased extension of ``path`` is in
            ``cls.allowed_extensions``, ``False`` otherwise.
        """
        ext = path.rsplit('.', 1)[-1].lower()
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse ``path`` and return the quotes it contains.

        Args:
            path: Path to a file whose extension is in
                ``cls.allowed_extensions``.

        Returns:
            A list of :class:`QuoteModel` (possibly empty if no parseable
            ``body - author`` lines were found).

        Raises:
            ValueError: If ``path`` is not a file this ingestor handles.
        """
        ...
