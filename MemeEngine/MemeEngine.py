"""Render an image with a quote and an attribution overlaid on top."""
import os
import random
import textwrap
import uuid

from PIL import Image, ImageDraw, ImageFont


def _find_font():
    """Return a usable bold-ish TrueType font, or fall back to default.

    Searches a short list of well-known font paths across macOS, Linux
    and Windows so the engine works on whichever workstation runs it.
    Returns Pillow's bitmap default font as a last resort.
    """
    candidates = [
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/Library/Fonts/Impact.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "C:/Windows/Fonts/Impact.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size=28)
    return ImageFont.load_default()


class MemeEngine:
    """Generate memes from an image plus a quote.

    The engine loads an image from disk via Pillow, resizes it so its
    width is at most 500 pixels (preserving aspect ratio), draws the
    quote body and author at a random location with a black outline so
    the text remains readable on bright photos, and saves the result as
    a JPEG inside the configured output directory.
    """

    def __init__(self, output_dir: str = "./tmp"):
        """Create a meme engine that writes its output under ``output_dir``.

        Args:
            output_dir: Directory the generated meme JPEGs are written
                to. The directory is created (recursively) on
                construction if it doesn't already exist, so callers
                don't have to ``mkdir`` themselves.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def make_meme(
        self,
        img_path: str,
        text: str,
        author: str,
        width: int = 500,
    ) -> str:
        """Render a meme and return the path of the saved JPEG.

        Args:
            img_path: Path of the source image (any format Pillow can
                open — JPEG, PNG, …).
            text: Body text of the quote. Wrapped automatically so it
                fits within ``width``.
            author: Author of the quote, drawn on its own line below
                the body.
            width: Target image width in pixels. Capped at 500 per the
                rubric; the height is scaled proportionally so the
                aspect ratio is preserved.

        Returns:
            The filesystem path of the rendered ``.jpg`` inside
            ``self.output_dir``. Filenames are randomised with a UUID4
            so concurrent calls don't clobber each other.

        Raises:
            FileNotFoundError: If ``img_path`` does not exist.
            PIL.UnidentifiedImageError: If the file at ``img_path``
                isn't an image Pillow can open.
        """
        if width > 500:
            width = 500
        img = Image.open(img_path).convert('RGBA')
        ratio = width / float(img.size[0])
        height = int(img.size[1] * ratio)
        img = img.resize((width, height), Image.LANCZOS)

        font = _find_font()
        draw = ImageDraw.Draw(img)

        # Wrap the quote so it fits within image width
        wrap_width = max(20, width // 14)  # heuristic
        wrapped = textwrap.fill(f'"{text}"', width=wrap_width)
        line = wrapped + f"\n  - {author}"

        # Random vertical placement in the upper third or middle.
        x = 10
        max_y = max(0, height - 90)
        y = random.randint(10, max_y // 2 if max_y else 10)

        # Black outline for readability — draw text repeatedly offset by 1px.
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                draw.text((x + dx, y + dy), line, font=font, fill="black")
        draw.text((x, y), line, font=font, fill="white")

        out_path = os.path.join(self.output_dir, f"meme-{uuid.uuid4().hex}.jpg")
        img.convert('RGB').save(out_path, format='JPEG', quality=92)
        return out_path
