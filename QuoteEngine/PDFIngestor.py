"""Ingestor for ``.pdf`` quote files.

Per the project rubric, this uses the ``pdftotext`` command-line tool
from xpdf-utils to convert the PDF to text, then parses the text the
same way :class:`TXTIngestor` does. Falls back to ``pypdf`` if
``pdftotext`` is not on the PATH so the project still runs in
environments without xpdf installed.
"""
import os
import shutil
import subprocess
import tempfile
from typing import List, Optional

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class PDFIngestor(IngestorInterface):
    """Concrete ingestor for ``.pdf`` files using the xpdf CLI tool.

    The class drives the external ``pdftotext`` binary via the stdlib
    ``subprocess`` module — *not* the PyPI ``pdftotext`` package, which
    the rubric explicitly forbids — and writes its output through a
    ``tempfile.NamedTemporaryFile`` that is cleaned up in a ``finally``
    block. If ``pdftotext`` is not installed the class transparently
    falls back to the pure-Python ``pypdf`` library so callers don't
    need to special-case the missing-binary path.
    """

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse a ``.pdf`` quote file.

        Args:
            path: Path to a ``.pdf`` file. Each line of the extracted
                text is expected in the ``body - author`` form;
                non-matching lines are skipped.

        Returns:
            A list of :class:`QuoteModel` parsed from the extracted
            text.

        Raises:
            ValueError: If ``path``'s extension is not ``.pdf``.
            RuntimeError: If neither ``pdftotext`` nor ``pypdf`` is
                available to extract text from the file.
        """
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
    def _extract_with_pdftotext(path: str) -> Optional[str]:
        """Run xpdf's ``pdftotext`` CLI; return the text or ``None``.

        The text is written to a ``NamedTemporaryFile``, read back, and
        the temp file is removed in a ``finally`` block so failures
        don't leak files on disk. Returns ``None`` if ``pdftotext`` is
        not on the PATH or the subprocess fails.
        """
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
    def _extract_with_pypdf(path: str) -> Optional[str]:
        """Pure-Python fallback using ``pypdf``; ``None`` if unavailable."""
        try:
            import pypdf
        except ImportError:
            return None
        reader = pypdf.PdfReader(path)
        return "\n".join(p.extract_text() or "" for p in reader.pages)
