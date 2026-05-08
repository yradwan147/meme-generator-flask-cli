"""CLI entry point for the meme generator.

Usage:
    python3 meme.py                                   # random dog meme
    python3 meme.py --path my.jpg --body "..." --author "..."
"""
import argparse
import os
import random

from QuoteEngine import Ingestor, QuoteModel
from MemeEngine import MemeEngine


def _all_quotes(quote_files):
    quotes = []
    for f in quote_files:
        try:
            quotes.extend(Ingestor.parse(f))
        except Exception as e:                        # noqa: BLE001
            print(f"warning: could not parse {f} — {e}")
    return quotes


def _all_images(images_dir):
    paths = []
    for root, _, files in os.walk(images_dir):
        for name in files:
            if name.lower().endswith(('.jpg', '.jpeg', '.png')):
                paths.append(os.path.join(root, name))
    return paths


def generate_meme(path: str | None = None,
                  body: str | None = None,
                  author: str | None = None) -> str:
    """Build a meme. If path/body/author are None we sample at random
    from the bundled dog images and quote files."""
    if path is None:
        imgs = _all_images("./_data/photos/dog/")
        if not imgs:
            raise FileNotFoundError(
                "No dog images found under ./_data/photos/dog/"
            )
        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = [
            "./_data/DogQuotes/DogQuotesTXT.txt",
            "./_data/DogQuotes/DogQuotesDOCX.docx",
            "./_data/DogQuotes/DogQuotesPDF.pdf",
            "./_data/DogQuotes/DogQuotesCSV.csv",
        ]
        quotes = _all_quotes(quote_files)
        if not quotes:
            raise RuntimeError("No quotes parsed from any file")
        quote = random.choice(quotes)
    else:
        if author is None:
            raise ValueError("--author is required when --body is given")
        quote = QuoteModel(body, author)

    engine = MemeEngine("./tmp")
    return engine.make_meme(img, quote.body, quote.author)


def _parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Generate a meme.")
    ap.add_argument("--path",   help="Image path (default: random dog).")
    ap.add_argument("--body",   help="Quote body. Requires --author.")
    ap.add_argument("--author", help="Quote author.")
    return ap.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    print(generate_meme(args.path, args.body, args.author))
