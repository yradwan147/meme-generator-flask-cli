# Meme Generator

Final project for Udacity's *Intermediate Python — Web Applications* course
(nd303). Two ways to use it:

* `python3 meme.py [...]` — CLI for one-off memes, with random defaults.
* `python3 app.py` — Flask web app at <http://localhost:5050/> for either a
  random meme or a custom-uploaded image + quote.

## Project layout

```
QuoteEngine/                Quote loading
├── QuoteModel.py             body / author dataclass
├── IngestorInterface.py      ABC; defines `can_ingest` + `parse`
├── CSVIngestor.py
├── TXTIngestor.py
├── DocxIngestor.py           uses python-docx
├── PDFIngestor.py            uses pdftotext, falls back to pypdf
└── Ingestor.py               facade that picks the right concrete one

MemeEngine/                 Image rendering
└── MemeEngine.py             open + resize + draw quote + save

meme.py                       CLI entry point
app.py                        Flask web app
templates/                    Jinja2 templates (meme.html, meme_form.html, base.html)
_data/DogQuotes/...           sample quote corpora in 4 file formats
_data/photos/dog/...          sample dog photos
```

## Running

```bash
pip install -r requirements.txt

# CLI
python3 meme.py
python3 meme.py --path my.jpg --body "Bork bork" --author "Buddy"

# Web app
python3 app.py
# open http://localhost:5050/
```

## Architecture

* **Strategy + Facade** — `IngestorInterface` is the strategy contract;
  `Ingestor` is the facade that, given any path, picks the right concrete
  ingestor by extension.
* **Single responsibility** — quote parsing knows nothing about images
  and vice versa.
* **PDF fallback** — `PDFIngestor` prefers the rubric-recommended
  `pdftotext` binary but transparently falls back to `pypdf` so the project
  runs on environments without xpdf installed.

## Dependencies

All declared in `requirements.txt`:

* `Flask` — web app
* `requests` — fetching user-submitted image URLs
* `Pillow` — image manipulation
* `python-docx` — DOCX ingest
* `pypdf` — PDF fallback when `pdftotext` is not on PATH
* `pandas` — CSV ingest

System dependency: `pdftotext` (xpdf/poppler) is preferred for PDF
ingest; the project falls back to `pypdf` if it's not installed.

## Standing-out work

* Fully-typed function signatures (`-> List[QuoteModel]`, `Optional[str]`,
  …) and PEP-257 module / class / public-method / `__init__` docstrings
  on every file.
* `MemeEngine` adds a 1-pixel black outline behind the white text so the
  caption stays readable on bright photos.
* The web app cleans up the temporary downloaded image in a `finally`
  block so concurrent requests don't pile up disk garbage.
* `_data/DogQuotes/DogQuotesPDF.pdf` is parsed via the `pdftotext` -layout
  flag for cleaner column ordering.

## License

Educational submission for Udacity nd303. Sample data © Udacity.
