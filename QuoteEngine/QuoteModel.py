"""Data class representing a quote with a body and an author."""


class QuoteModel:
    """A quote with a body and the person it's attributed to."""

    def __init__(self, body: str, author: str):
        self.body = body.strip().strip('"')
        self.author = author.strip().strip('"')

    def __repr__(self):
        return f'"{self.body}" - {self.author}'

    def __eq__(self, other):
        if not isinstance(other, QuoteModel):
            return NotImplemented
        return self.body == other.body and self.author == other.author

    def __hash__(self):
        return hash((self.body, self.author))
