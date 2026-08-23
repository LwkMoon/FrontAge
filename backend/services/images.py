"""Logo upload processing and favicon generation.

Uploaded logos are resized, compressed, and returned as a data URI so the
exported site stays a self-contained index.html + style.css. No separate
image files to keep track of.
"""
import base64
import io

from PIL import Image

MAX_DIMENSION = 480
MAX_UPLOAD_BYTES = 3 * 1024 * 1024  # 3MB
ALLOWED_MIMETYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp"}


class ImageError(ValueError):
    """Raised for any problem with an uploaded image; message is user-facing."""


def process_logo_upload(file_storage):
    """Take a Flask FileStorage, return a compressed data URI string."""
    if file_storage is None:
        raise ImageError("No file provided")

    if file_storage.mimetype not in ALLOWED_MIMETYPES:
        raise ImageError("Please upload a PNG, JPEG, or WebP image")

    raw = file_storage.read()
    if not raw:
        raise ImageError("That file appears to be empty")
    if len(raw) > MAX_UPLOAD_BYTES:
        raise ImageError("Image is too large (max 3MB)")

    try:
        img = Image.open(io.BytesIO(raw))
        img.load()
    except Exception:
        raise ImageError("Could not read that image file")

    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)

    if has_alpha:
        img = img.convert("RGBA")
        fmt, mime = "PNG", "image/png"
    else:
        img = img.convert("RGB")
        fmt, mime = "JPEG", "image/jpeg"

    img.thumbnail((MAX_DIMENSION, MAX_DIMENSION))

    buf = io.BytesIO()
    if fmt == "JPEG":
        img.save(buf, format="JPEG", optimize=True, quality=85)
    else:
        img.save(buf, format="PNG", optimize=True)

    encoded = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def generate_monogram_favicon(business_name, primary_color, bg_color):
    """Build a simple monogram favicon (first letter on a rounded square) as
    an SVG data URI, used when no logo has been uploaded."""
    letter = next((ch for ch in (business_name or "").strip().upper() if ch.isalnum()), "?")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        f'<rect width="64" height="64" rx="14" fill="{bg_color}"/>'
        f'<text x="32" y="43" font-family="Arial, sans-serif" font-size="30" '
        f'font-weight="700" fill="{primary_color}" text-anchor="middle">{letter}</text>'
        '</svg>'
    )
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"
