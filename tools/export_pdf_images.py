import argparse
import os
from dataclasses import dataclass

import fitz  # PyMuPDF
from PIL import Image, ImageChops, ImageEnhance


@dataclass
class ExportOptions:
    dpi: int
    fmt: str
    quality: int
    autocrop: bool
    pad: int
    brighten: float
    contrast: float
    max_width: int


def _autocrop(img: Image.Image, pad: int) -> Image.Image:
    if img.mode != "RGB":
        img = img.convert("RGB")
    bg = Image.new("RGB", img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if not bbox:
        return img
    left, top, right, bottom = bbox
    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(img.size[0], right + pad)
    bottom = min(img.size[1], bottom + pad)
    return img.crop((left, top, right, bottom))


def _enhance(img: Image.Image, brighten: float, contrast: float) -> Image.Image:
    if brighten != 1.0:
        img = ImageEnhance.Brightness(img).enhance(brighten)
    if contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    return img


def _downscale(img: Image.Image, max_width: int) -> Image.Image:
    if max_width <= 0:
        return img
    w, h = img.size
    if w <= max_width:
        return img
    new_h = int(h * (max_width / w))
    return img.resize((max_width, new_h), Image.Resampling.LANCZOS)


def _parse_pages(pages_str: str) -> list[int] | None:
    if not pages_str.strip():
        return None
    parts = [p.strip() for p in pages_str.split(",") if p.strip()]
    parsed: list[int] = []
    for part in parts:
        if "-" in part:
            a, b = part.split("-", 1)
            try:
                start = int(a)
                end = int(b)
            except ValueError:
                continue
            if start <= end:
                parsed.extend(list(range(start, end + 1)))
            else:
                parsed.extend(list(range(end, start + 1)))
        else:
            try:
                parsed.append(int(part))
            except ValueError:
                continue
    return sorted(set([p for p in parsed if p > 0]))


def export_pdf(
    pdf_path: str,
    out_dir: str,
    out_prefix: str,
    pages: list[int] | None,
    opts: ExportOptions,
) -> list[str]:
    doc = fitz.open(pdf_path)
    if pages is None:
        page_indexes = list(range(doc.page_count))
    else:
        page_indexes = [p - 1 for p in pages if 1 <= p <= doc.page_count]

    os.makedirs(out_dir, exist_ok=True)
    written: list[str] = []

    for idx in page_indexes:
        page = doc.load_page(idx)
        zoom = opts.dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

        if opts.autocrop:
            img = _autocrop(img, opts.pad)
        img = _enhance(img, opts.brighten, opts.contrast)
        img = _downscale(img, opts.max_width)

        page_num = idx + 1
        out_name = f"{out_prefix}-p{page_num:02d}.{opts.fmt}"
        out_path = os.path.join(out_dir, out_name)

        if opts.fmt.lower() in {"jpg", "jpeg"}:
            img.save(
                out_path,
                format="JPEG",
                quality=opts.quality,
                optimize=True,
                progressive=True,
            )
        else:
            img.save(out_path, format="PNG", optimize=True)

        written.append(out_path)

    return written


def main() -> None:
    ap = argparse.ArgumentParser(description="Export PDF pages to optimized images.")
    ap.add_argument("pdf", help="Input PDF path")
    ap.add_argument("--out-dir", required=True, help="Output directory")
    ap.add_argument("--prefix", required=True, help="Output filename prefix")
    ap.add_argument(
        "--pages",
        default="",
        help="Comma list or ranges (e.g. 1,2,5-7). Empty = all",
    )
    ap.add_argument("--dpi", type=int, default=220)
    ap.add_argument("--fmt", choices=["png", "jpg"], default="png")
    ap.add_argument("--quality", type=int, default=86)
    ap.add_argument("--autocrop", action="store_true")
    ap.add_argument("--pad", type=int, default=12)
    ap.add_argument("--brighten", type=float, default=1.0)
    ap.add_argument("--contrast", type=float, default=1.0)
    ap.add_argument("--max-width", type=int, default=2200)

    args = ap.parse_args()
    pages = _parse_pages(args.pages)

    opts = ExportOptions(
        dpi=args.dpi,
        fmt=args.fmt,
        quality=args.quality,
        autocrop=args.autocrop,
        pad=args.pad,
        brighten=args.brighten,
        contrast=args.contrast,
        max_width=args.max_width,
    )

    written = export_pdf(args.pdf, args.out_dir, args.prefix, pages, opts)
    print("\n".join(written))


if __name__ == "__main__":
    main()

