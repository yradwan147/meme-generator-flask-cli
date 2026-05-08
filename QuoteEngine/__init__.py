"""QuoteEngine — load quotes from .csv, .txt, .docx, .pdf files."""
from .QuoteModel import QuoteModel
from .IngestorInterface import IngestorInterface
from .CSVIngestor import CSVIngestor
from .TXTIngestor import TXTIngestor
from .DocxIngestor import DocxIngestor
from .PDFIngestor import PDFIngestor
from .Ingestor import Ingestor

__all__ = [
    'QuoteModel',
    'Ingestor',
    'IngestorInterface',
    'CSVIngestor',
    'TXTIngestor',
    'DocxIngestor',
    'PDFIngestor',
]
