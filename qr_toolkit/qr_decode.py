from pathlib import Path
import cv2
import tempfile
from PIL import Image
import io

try:
    import cairosvg
    CAIRO_AVAILABLE = True
except Exception:
    CAIRO_AVAILABLE = False


def svg_to_png_bytes(svg_path: Path):
    """Convert SVG to PNG bytes using cairosvg if available."""
    if not CAIRO_AVAILABLE:
        return None

    try:
        return cairosvg.svg2png(url=str(svg_path))
    except Exception:
        return None


def load_image(path: Path):
    """Load image, handling SVG if possible."""
    try:
        if path.suffix.lower() == ".svg":
            png_bytes = svg_to_png_bytes(path)
            if png_bytes is None:
                print(f"⚠ Cannot read SVG (no renderer): {path.name}")
                return None

            image = Image.open(io.BytesIO(png_bytes)).convert("RGB")
            return cv2.cvtColor(
                cv2.imread(str(path)) if False else 
                cv2.cvtColor(
                    cv2.imdecode(
                        cv2.UMat(bytearray(png_bytes)).get(), 
                        cv2.IMREAD_COLOR
                    ), 
                    cv2.COLOR_BGR2RGB
                ),
                cv2.COLOR_RGB2BGR
            )

        else:
            return cv2.imread(str(path))

    except Exception:
        return None


def decode_image(path: Path):
    try:
        img = load_image(path)
        if img is None:
            return []

        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)

        return [data] if data else []

    except Exception:
        return []


def decode_folder(folder: Path):
    extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".svg"}

    results = []
    success = 0
    failed = 0
    skipped = 0

    for file in sorted(folder.iterdir()):
        if file.suffix.lower() not in extensions:
            continue

        decoded = decode_image(file)

        if decoded:
            for d in decoded:
                results.append({"filename": file.name, "data": d})
            print(f"✓ {file.name}")
            success += 1
        else:
            results.append({"filename": file.name, "data": None})
            print(f"✗ {file.name}")
            failed += 1

    print(f"\nDecoded: {success} | Failed: {failed}")
    return results
