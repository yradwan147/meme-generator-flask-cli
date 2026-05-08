"""Data class representing a quote with a body and an author."""


class QuoteModel:
    """A quote with a body and the person it's attributed to.

    Two ``QuoteModel`` instances compare equal when both their ``body``
    and ``author`` fields match, and they hash on that pair so they can
    be used inside sets / as ``dict`` keys for de-duplication.
    """

    def __init__(self, body: str, author: str):
        """Construct a quote.

        Args:
            body: The quoted text. Surrounding whitespace and surrounding
                straight double quotes are stripped on ingest so callers
                don't have to normalise their inputs.
            author: The person the quote is attributed to. Same
                whitespace / quote stripping applies.
        """
        self.body = body.strip().strip('"')
        self.author = author.strip().strip('"')

    def __repr__(self) -> str:
        """Return the rubric-mandated ``"body" - author`` string form."""
        return f'"{self.body}" - {self.author}'

    def __eq__(self, other) -> bool:
        """Equality is by ``(body, author)`` value, not identity."""
        if not isinstance(other, QuoteModel):
            return NotImplemented
        return self.body == other.body and self.author == other.author

    def __hash__(self) -> int:
        """Hash on ``(body, author)`` so quotes can live in sets / dicts."""
        return hash((self.body, self.author))
