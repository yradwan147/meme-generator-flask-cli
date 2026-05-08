"""Ingestor for ``.csv`` quote files (uses pandas)."""
from typing import List

import pandas as pd

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class CSVIngestor(IngestorInterface):
    """Concrete ingestor for ``.csv`` files using ``pandas``.

    Expects a CSV with at least the columns ``body`` and ``author``;
    extra columns are ignored. Rows where either column is missing
    (``NaN``) are skipped silently. The rubric explicitly requires the
    pandas dependency for this ingestor (vs. the stdlib ``csv``
    module).
    """

    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a ``.csv`` quote file.

        Args:
            path: Path to a ``.csv`` file with ``body`` and ``author``
                columns. The file is read with ``utf-8-sig`` so a BOM
                from Excel-style exports is handled transparently.

        Returns:
            A list of :class:`QuoteModel` — one per row whose ``body``
            and ``author`` cells were both non-null.

        Raises:
            ValueError: If ``path``'s extension is not ``.csv``.
        """
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest {path}")
        quotes: List[QuoteModel] = []
        data = pd.read_csv(path, encoding='utf-8-sig')
        for _, row in data.iterrows():
            body = row.get('body')
            author = row.get('author')
            if pd.notna(body) and pd.notna(author):
                quotes.append(QuoteModel(str(body), str(author)))
        return quotes
