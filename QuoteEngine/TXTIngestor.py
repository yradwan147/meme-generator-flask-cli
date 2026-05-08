"""Ingestor for plain-text quote files (one quote per line)."""
from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class TXTIngestor(IngestorInterface):
    """Concrete ingestor for ``.txt`` files.

    Each line is expected in the form ``body - author``; blank lines and
    lines that don't contain the ``" - "`` separator are silently
    skipped. The class deliberately uses only the standard library
    (``open``) — no third-party dependency — to satisfy the rubric's
    "ingest text files using the native file library" requirement.
    """

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a ``.txt`` quote file.

        Args:
            path: Path to a ``.txt`` file. Must end in ``.txt`` (the
                check is delegated to ``can_ingest``).

        Returns:
            A list of :class:`QuoteModel` — one per non-empty line that
            matched the ``body - author`` shape.

        Raises:
            ValueError: If ``path``'s extension is not ``.txt``.
        """
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
