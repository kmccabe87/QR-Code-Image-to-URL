#!/usr/bin/env python3
"""
Scan folder of QR code images → decode → save filename + URL to Excel
"""

import sys
from pathlib import Path
import pandas as pd
from PIL import Image
import pyzbar.pyzbar as pyzbar  # pip install pyzbar
# Also needs: pillow + pyzbar (and on Linux often: sudo apt install libzbar0)

def decode_qr_from_image(image_path: Path) -> str | None:
    """Try to read first QR code from image. Returns data or None."""
    try:
        img = Image.open(image_path).convert('RGB')
        decoded = pyzbar.decode(img)
        if decoded:
            # Take the first QR code found
            return decoded[0].data.decode('utf-8').strip()
        return None
    except Exception as e:
        print(f"  Error reading {image_path.name}: {e}")
        return None


def main():
    # 1. Choose folder -------------------------------------------------------
    if len(sys.argv) > 1:
        folder = Path(sys.argv[1]).resolve()
    else:
        print("Paste full path to folder containing QR images (or drag folder here):")
        try:
            folder_input = input("> ").strip().strip("'\"")
            folder = Path(folder_input).resolve()
        except KeyboardInterrupt:
            print("\nCancelled.")
            return

    if not folder.is_dir():
        print(f"Error: Not a valid folder → {folder}")
        return

    print(f"\nScanning folder: {folder}")
    print("Looking for: .png  .jpg  .jpeg  .webp  .gif ...\n")

    # 2. Find image files ----------------------------------------------------
    extensions = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp'}
    image_files = [
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() in extensions
    ]

    if not image_files:
        print("No image files found in the folder.")
        return

    print(f"Found {len(image_files)} image file(s)\n")

    # 3. Decode each one -----------------------------------------------------
    results = []

    for img_path in sorted(image_files):  # sorted = consistent order
        url = decode_qr_from_image(img_path)
        results.append({
            "filename": img_path.name,
            "url": url if url else "[NOT READ / NO QR / ERROR]"
        })
        status = "✓" if url else "✗"
        print(f"{status}  {img_path.name:<35}  →  {url or '—'}")

    # 4. Save to Excel -------------------------------------------------------
    if not results:
        print("\nNothing to save.")
        return

    df = pd.DataFrame(results)

    output_file = Path(__file__).resolve().parent / "qr_codes_decoded.xlsx"

    try:
        df.to_excel(output_file, index=False, sheet_name="QR Results")
        print(f"\nSaved to:  {output_file}")
        print(f"Rows written: {len(df)}")
    except Exception as e:
        print(f"\nCould not save Excel file: {e}")
        # Fallback: csv
        csv_file = output_file.with_suffix(".csv")
        df.to_csv(csv_file, index=False)
        print(f"Fallback → saved CSV: {csv_file}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")