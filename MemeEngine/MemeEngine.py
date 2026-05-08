"""Render an image with a quote and an attribution overlaid on top."""
import os
import random
import textwrap
import uuid

from PIL import Image, ImageDraw, ImageFont


def _find_font():
    """Return a usable bold-ish TrueType font, or fall back to default."""
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
    """Generate memes from an image + quote."""

    def __init__(self, output_dir: str = "./tmp"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def make_meme(
        self,
        img_path: str,
        text: str,
        author: str,
        width: int = 500,
    ) -> str:
        """Open image, resize to `width` keeping aspect ratio, write the
        quote on top, save to disk and return the saved path."""
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
