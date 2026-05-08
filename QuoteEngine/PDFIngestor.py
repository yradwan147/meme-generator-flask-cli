"""Ingestor for .pdf quote files.

Per the project rubric, this uses the `pdftotext` command-line tool from
xpdf-utils to convert the PDF to text, then parses the text the same way
TXTIngestor does. Falls back to pypdf if pdftotext is not on the PATH so
the project still runs in environments without xpdf installed.
"""
import os
import shutil
import subprocess
import tempfile
from typing import List

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class PDFIngestor(IngestorInterface):
    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        if not cls.can_ingest(path):
            raise ValueError(f"Cannot ingest {path}")

        text = cls._extract_with_pdftotext(path) or cls._extract_with_pypdf(path)
        if text is None:
            raise RuntimeError(
                "Neither pdftotext nor pypdf is available to parse PDFs."
            )

        quotes: List[QuoteModel] = []
        for raw in text.splitlines():
            line = raw.strip().lstrip('“').rstrip('”')
            if not line or ' - ' not in line:
                continue
            body, author = line.rsplit(' - ', 1)
            quotes.append(QuoteModel(body, author))
        return quotes

    # -- backends -----------------------------------------------------------
    @staticmethod
    def _extract_with_pdftotext(path: str) -> str | None:
        if shutil.which('pdftotext') is None:
            return None
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.txt', delete=False
        ) as tmp:
            tmp_path = tmp.name
        try:
            subprocess.run(
                ['pdftotext', '-layout', path, tmp_path],
                check=True, capture_output=True,
            )
            with open(tmp_path, 'r', encoding='utf-8', errors='replace') as f:
                return f.read()
        except subprocess.CalledProcessError:
            return None
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    @staticmethod
    def _extract_with_pypdf(path: str) -> str | None:
        try:
            import pypdf
        except ImportError:
            return None
        reader = pypdf.PdfReader(path)
        return "\n".join(p.extract_text() or "" for p in reader.pages)
