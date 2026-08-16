from pathlib import Path
import qrcode
from qrcode.constants import ERROR_CORRECT_Q
from qrcode.image.svg import SvgPathImage

from .utils import sanitize_filename, avoid_overwrite


def generate_png(data: str, output_path: Path):
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()
    img.save(output_path)


def generate_svg(data: str, output_path: Path):
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_Q,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(image_factory=SvgPathImage)
    img.save(output_path)


def process_generation(df, output_dir, mode="png", validate_urls=False):
    from .utils import is_valid_url

    created, skipped = 0, 0

    for i, row in df.iterrows():
        name, data = row["name"], row["data"]

        if not name or not data:
            skipped += 1
            continue

        if validate_urls and not is_valid_url(data):
            skipped += 1
            continue

        safe_name = sanitize_filename(name)

        ext = "png" if mode == "png" else "svg"
        path = output_dir / f"{safe_name}.{ext}"
        path = avoid_overwrite(path)

        try:
            if mode == "png":
                generate_png(data, path)
            else:
                generate_svg(data, path)

            created += 1
            print(f"✓ {path.name}")

        except Exception as e:
            print(f"✗ {name}: {e}")

    print(f"\nCreated: {created} | Skipped: {skipped}")
