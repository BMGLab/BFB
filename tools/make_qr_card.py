#!/usr/bin/env python3
"""
make_qr_card.py — a projection-ready QR card for a course link.

    python3 tools/make_qr_card.py URL -o Entry_Diagnostic_QR.png \
        --title "Entry Diagnostic" --subtitle "Giriş Değerlendirmesi" \
        --note "Ungraded · 15 minutes · Notlandırılmaz"

Designed to be thrown on a projector and scanned from the back of the room, so:

  * high error correction, because a projector screen is a poor scanning target
    and a lens flare across a corner should not break it;
  * a wide quiet zone, because a QR with no margin fails on many phones;
  * the URL printed underneath in large type, because a handful of phones will
    always fail to scan and those students need to type it instead.

The decoded contents are verified against the input before the file is written,
so a card that cannot be read never reaches the repository.
"""
import argparse
import sys
from pathlib import Path

try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Needs qrcode and Pillow:  pip install 'qrcode[pil]'")


def load_font(size, bold=False):
    """A real font if one can be found; Pillow's bitmap default otherwise."""
    for path in ("/System/Library/Fonts/Helvetica.ttc",
                 "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size, index=1 if (bold and path.endswith(".ttc")) else 0)
            except Exception:
                continue
    return ImageFont.load_default()


def build(url, title, subtitle, note, out, box=16):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=box, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    code = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    pad = 90
    head_h = 230 if title else 0
    foot_h = 190
    W = code.width + pad * 2
    H = head_h + code.height + foot_h

    card = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(card)

    def centre(text, y, size, fill="black", bold=False, max_w=None):
        """Centre text, shrinking it until it fits — a clipped URL is useless."""
        limit = max_w or (W - 2 * 24)
        font = load_font(size, bold)
        while size > 12:
            w = draw.textbbox((0, 0), text, font=font)[2]
            if w <= limit:
                break
            size -= 2
            font = load_font(size, bold)
        w = draw.textbbox((0, 0), text, font=font)[2]
        draw.text(((W - w) / 2, y), text, font=font, fill=fill)
        return draw.textbbox((0, 0), text, font=font)[3]

    if title:
        centre(title, 48, 76, bold=True)
    if subtitle:
        centre(subtitle, 142, 46, fill="#52514e")

    card.paste(code, (pad, head_h))

    y = head_h + code.height + 18
    centre(url, y, 52, bold=True)
    if note:
        centre(note, y + 76, 40, fill="#52514e")

    # Verify before writing: decode the rendered card and compare.
    try:
        import cv2
        import numpy as np
        arr = np.array(card.convert("L"))
        decoded, _, _ = cv2.QRCodeDetector().detectAndDecode(arr)
        if decoded != url:
            sys.exit(f"REFUSING TO WRITE: the card decodes to {decoded!r}, not {url!r}")
        verified = "decoded and matches"
    except ImportError:
        verified = "NOT verified (install opencv-python-headless to check)"

    card.save(out, dpi=(300, 300))
    print(f"{out}  {card.width}x{card.height}px  ·  {verified}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--note", default="")
    a = ap.parse_args()
    build(a.url, a.title, a.subtitle, a.note, a.out)


if __name__ == "__main__":
    main()
