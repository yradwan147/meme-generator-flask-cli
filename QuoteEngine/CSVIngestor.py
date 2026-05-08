"""Ingestor for CSV quote files with a `body,author` header.

Uses pandas (rubric requirement: "The class depends on the pandas library
to complete the defined, abstract method signatures to parse CSV files").
"""
from typing import List

import pandas as pd

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class CSVIngestor(IngestorInterface):
    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
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
