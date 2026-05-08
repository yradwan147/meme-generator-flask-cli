"""Flask front-end for the meme generator."""
import os
import random
import tempfile

import requests
from flask import Flask, abort, render_template, request

from QuoteEngine import Ingestor
from MemeEngine import MemeEngine


app = Flask(__name__)
meme = MemeEngine("./static")


def setup():
    """Read every supplied quote file and dog photo. Run once at boot."""
    quote_files = [
        "./_data/DogQuotes/DogQuotesTXT.txt",
        "./_data/DogQuotes/DogQuotesDOCX.docx",
        "./_data/DogQuotes/DogQuotesPDF.pdf",
        "./_data/DogQuotes/DogQuotesCSV.csv",
    ]
    quotes = []
    for f in quote_files:
        try:
            quotes.extend(Ingestor.parse(f))
        except Exception as e:                        # noqa: BLE001
            app.logger.warning("could not parse %s — %s", f, e)

    imgs = []
    images_path = "./_data/photos/dog/"
    for root, _, files in os.walk(images_path):
        for name in files:
            if name.lower().endswith((".jpg", ".jpeg", ".png")):
                imgs.append(os.path.join(root, name))

    return quotes, imgs


quotes, imgs = setup()


@app.route("/")
def meme_rand():
    """Serve a meme built from a random image and a random quote."""
    if not imgs or not quotes:
        abort(500, "Run setup data not available.")
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template("meme.html", path=path)


@app.route("/create", methods=["GET"])
def meme_form():
    """User input form for a custom meme."""
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post():
    """Pull the user-submitted image URL, run it through MemeEngine."""
    image_url = request.form.get("image_url")
    body      = request.form.get("body")
    author    = request.form.get("author")
    if not (image_url and body and author):
        return render_template("meme_form.html",
                               error="image_url, body, author all required."), 400

    tmp_path = None
    try:
        resp = requests.get(image_url, timeout=15, stream=True)
        resp.raise_for_status()
        with tempfile.NamedTemporaryFile(
            suffix=".jpg", delete=False
        ) as tmp:
            for chunk in resp.iter_content(chunk_size=8192):
                tmp.write(chunk)
            tmp_path = tmp.name
        path = meme.make_meme(tmp_path, body, author)
        return render_template("meme.html", path=path)
    except Exception as e:                            # noqa: BLE001
        return render_template("meme_form.html",
                               error=f"could not build meme: {e}"), 502
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
