"""Ingestor for CSV quote files with a `body,author` header."""
from typing import List
import csv

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class CSVIngestor(IngestorInterface):
    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest {path}")
        quotes: List[QuoteModel] = []
        with open(path, 'r', encoding='utf-8-sig', newline='') as f:
            for row in csv.DictReader(f):
                body, author = row.get('body'), row.get('author')
                if body and author:
                    quotes.append(QuoteModel(body, author))
        return quotes
