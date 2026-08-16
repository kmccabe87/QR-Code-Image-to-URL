# QR Code Image-to-URL Toolkit

Batch-generate QR code images from an Excel spreadsheet, and decode QR code images back into URLs — both in bulk.

Built in Python with OpenCV, qrcode, and pandas. Runs locally; no data leaves your machine.

## Features

- **Generate**: read an Excel file (column A = filename, column B = QR data) and produce one QR image per row, as **PNG** or **SVG**.
- **Decode**: read every image in a folder, extract the QR payload (typically a URL), and write the results to a date-stamped Excel file.
- Handles SVG input during decode (rendered to PNG via `cairosvg` before detection).

## Repository layout

```
qr_toolkit/                      # the Python package
├── cli.py                       # CLI entry point (generate-svg / generate-png / decode)
├── excel_io.py                  # Excel read/write (pandas)
├── qr_generate.py               # PNG/SVG QR generation
├── qr_decode.py                 # QR detection via OpenCV
├── gui.py                       # minimal file-picker helper (not wired into the CLI yet)
└── utils.py                     # filename sanitizing, overwrite avoidance, URL check
Images to Convert to URL's/      # ← drop images here for decode (required input folder)
QR Code Images/                  # generation output (gitignored)
QR Url's/                        # decode output (gitignored)
requirements.txt
```

## Install

```bash
git clone https://github.com/kmccabe87/QR-Code-Image-to-URL.git
cd QR-Code-Image-to-URL
python -m venv .venv
# Windows: .venv\Scripts\activate   |   macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

All commands are run from the repository root, as a package:

```bash
# 1) Put your Excel file(s) in the current folder
#    (column A = output filename, column B = the QR code data, e.g. a URL)

python -m qr_toolkit.cli generate-svg   # QR Code Images/*.svg
python -m qr_toolkit.cli generate-png   # QR Code Images/*.png

# 2) Decode: put images into "Images to Convert to URL's/" then
python -m qr_toolkit.cli decode         # writes QR Url's/YYYY-MM-DD_decoded_qr.xlsx
```

A small confirmation dialog appears before generation (tkinter). Decoding prints per-file ✓/✗ results and a summary.

## Notes

- Output folders are created automatically if missing and gitignored so generated images don't bloat the repo.
- `qr_toolkit/gui.py` provides a single-file picker flow; it isn't invoked by the CLI yet — the CLI is the intended entry point.

## License

MIT — see [LICENSE](LICENSE).
