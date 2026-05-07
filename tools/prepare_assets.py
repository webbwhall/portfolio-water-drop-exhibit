import os
from dataclasses import dataclass

from PIL import Image, ImageEnhance


SITE = r"C:\Users\webbs\OneDrive\Desktop\Miami University\Intermed Interaction Design - IMS354 A\portfolio-water-drop-exhibit"
IMG_DIR = os.path.join(SITE, "assets", "images")


@dataclass(frozen=True)
class Target:
    src: str
    dst: str


def _p(path: str) -> str:
    return os.path.join(IMG_DIR, path)


def copy_as(src_name: str, dst_name: str, fmt: str | None = None, quality: int = 88) -> None:
    src = _p(src_name)
    dst = _p(dst_name)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    img = Image.open(src).convert("RGB")
    if fmt is None:
        img.save(dst)
        return
    if fmt.lower() in {"jpg", "jpeg"}:
        img.save(dst, format="JPEG", quality=quality, optimize=True, progressive=True)
    else:
        img.save(dst, format="PNG", optimize=True)


def crop_as(src_name: str, dst_name: str, box: tuple[int, int, int, int], quality: int = 88) -> None:
    src = _p(src_name)
    dst = _p(dst_name)
    img = Image.open(src).convert("RGB")
    cropped = img.crop(box)
    cropped.save(dst, format="JPEG", quality=quality, optimize=True, progressive=True)


def crop_band(src_name: str, dst_name: str, y0: float, y1: float, pad: int = 16, quality: int = 88) -> None:
    src = _p(src_name)
    dst = _p(dst_name)
    img = Image.open(src).convert("RGB")
    w, h = img.size
    top = max(0, int(h * y0) - pad)
    bot = min(h, int(h * y1) + pad)
    band = img.crop((0, top, w, bot))
    band.save(dst, format="PNG" if dst.lower().endswith(".png") else "JPEG", quality=quality, optimize=True)


def enhance_for_web(src_name: str, dst_name: str, brighten: float = 1.0, contrast: float = 1.0, quality: int = 88) -> None:
    src = _p(src_name)
    dst = _p(dst_name)
    img = Image.open(src).convert("RGB")
    if brighten != 1.0:
        img = ImageEnhance.Brightness(img).enhance(brighten)
    if contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    img.save(dst, format="JPEG", quality=quality, optimize=True, progressive=True)


def main() -> None:
    # --- Moodboards / directions ---
    copy_as("moodboard-p02.jpg", "moodboard-direction-a.jpg", fmt="jpg")
    copy_as("moodboard-p03.jpg", "moodboard-direction-b.jpg", fmt="jpg")
    copy_as("moodboard-p05.jpg", "direction-a-palette.jpg", fmt="jpg")
    copy_as("moodboard-p06.jpg", "direction-b-palette.jpg", fmt="jpg")
    copy_as("moodboard-p07.jpg", "direction-compare.jpg", fmt="jpg")
    copy_as("moodboard-p09.jpg", "direction-choice.jpg", fmt="jpg")

    # Use the exhibit layout as the \"concept\" image for the moodboard section.
    copy_as("exhibit-p01.jpg", "moodboard-concept.jpg", fmt="jpg")

    # --- Typography ---
    copy_as("type-p01.jpg", "type-treatment.jpg", fmt="jpg", quality=90)

    # --- AI exploration ---
    copy_as("ai-journey-p02.jpg", "ai-water-cycle-early.jpg", fmt="jpg")
    copy_as("ai-journey-p03.jpg", "ai-museum-journey.jpg", fmt="jpg")
    copy_as("ai-journey-p05.jpg", "ai-hero-banner-experiments.jpg", fmt="jpg")
    copy_as("ai-journey-p06.jpg", "ai-final-heroes.jpg", fmt="jpg")

    # --- Sketches ---
    enhance_for_web("sketches-web-p01.jpg", "sketches-website.jpg", brighten=1.03, contrast=1.12)
    enhance_for_web("sketchbook-p03.jpg", "sketches-app-flow.jpg", brighten=1.03, contrast=1.12)

    # Reuse website sketches for wireframes \"Hand Sketches\" compare card
    enhance_for_web("sketches-web-p01.jpg", "web-sketches.jpg", brighten=1.03, contrast=1.12)

    # --- Website wireframes ---
    copy_as("lowfi-screen-p01.png", "lofi-wireframes.png", fmt="png")
    copy_as("lofi-web-p01.png", "lofi-wireframes.jpg", fmt="jpg", quality=90)
    copy_as("hifi-proto-p01.jpg", "web-screen-refined.jpg", fmt="jpg", quality=88)

    # --- IA / Sitemap substitute (until a dedicated sitemap PDF is found) ---
    copy_as("exhibit-p01.jpg", "sitemap.jpg", fmt="jpg")

    # --- App wireframes / workflows: crop the large LoFi board into 4 readable panels ---
    # lofi-app-p01.png is a tall board. We slice it into bands that match your section cards.
    crop_band("lofi-app-p01.png", "app-ar-scan.png", 0.00, 0.33)
    crop_band("lofi-app-p01.png", "app-collect-stations.png", 0.33, 0.67)
    crop_band("lofi-app-p01.png", "app-complete-cycle.png", 0.67, 1.00)

    # High fidelity workflow as the \"learning flow\" visual
    copy_as("hifi-workflow-p01.jpg", "app-workflow.jpg", fmt="jpg", quality=88)

    # --- Final deliverables (use the strongest high-fidelity boards available) ---
    copy_as("hifi-proto-p01.jpg", "final-website.jpg", fmt="jpg", quality=88)
    copy_as("hifi-app-p01.jpg", "final-app.jpg", fmt="jpg", quality=88)
    copy_as("exhibit-p01.jpg", "final-exhibit.jpg", fmt="jpg", quality=88)
    copy_as("type-p01.jpg", "final-type.jpg", fmt="jpg", quality=90)
    copy_as("ai-journey-p03.jpg", "final-hero-graphics.jpg", fmt="jpg", quality=88)

    # Signage mockups (real images added by user)
    copy_as("Webb Hall - outdoor Aframe.jpg", "signage-a-frame.jpg", fmt="jpg", quality=88)
    copy_as("Webb Hall - lit exhibit sign.jpg", "signage-directory-wall.jpg", fmt="jpg", quality=88)
    copy_as("Webb Hall - Elevator Sign.jpg", "signage-elevator-directory.jpg", fmt="jpg", quality=88)
    copy_as("Webb Hall - overhang sign.jpg", "signage-banner-hallway.jpg", fmt="jpg", quality=88)
    copy_as("Webb Hall - poster on steps.jpg", "signage-continue-up.jpg", fmt="jpg", quality=88)
    copy_as("Webb Hall - corner sign.jpg", "signage-corner-arrow.jpg", fmt="jpg", quality=88)
    copy_as("Webb Hall - exhibit poster.jpg", "signage-collection-door.jpg", fmt="jpg", quality=88)

    # Featured signage (best first impression)
    copy_as("signage-a-frame.jpg", "final-signage.jpg", fmt="jpg", quality=88)

    # Optional extra slot
    copy_as("direction-choice.jpg", "deliverable-extra-1.jpg", fmt="jpg", quality=88)

    # --- Hero image: crop a wide slice from the refined website screen (left panel hero area) ---
    # Crop coordinates tuned to the exported hifi prototype board.
    # If you prefer a different hero, swap this file with any 1920x1080-ish export.
    img = Image.open(_p("hifi-proto-p01.jpg")).convert("RGB")
    w, h = img.size
    # Take a wide, cinematic crop across the top third
    y_top = int(h * 0.00)
    y_bot = int(h * 0.40)
    hero = img.crop((0, y_top, w, y_bot))
    hero = hero.resize((1920, int(1920 * hero.size[1] / hero.size[0])), Image.Resampling.LANCZOS)
    hero.save(_p("hero-waterdrop.jpg"), format="JPEG", quality=88, optimize=True, progressive=True)

    print("Prepared assets in:", IMG_DIR)


if __name__ == "__main__":
    main()

