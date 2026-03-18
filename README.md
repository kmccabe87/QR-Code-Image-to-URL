# QR Code ↔ Excel Converter Tools

Two simple Python scripts for bidirectional conversion:

- Extract URLs from QR code images → Excel spreadsheet
- Generate QR code images from Excel spreadsheet (filename + URL)

## Features

- **qr_to_excel.py**: Scans images in a folder, decodes QR codes, outputs `qr_codes_decoded.xlsx` with filename and URL
- **excel_to_qr.py**: Reads `.xlsx` file (Column A = filename, Column B = URL), generates PNG QR codes in a new folder

## Requirements

These libraries are required for full functionality:

| Library          | Purpose                              | Installation command                  | Used in              | Notes                              |
|------------------|--------------------------------------|---------------------------------------|----------------------|------------------------------------|
| **pillow**       | Image processing (open, save, etc.)  | `pip install pillow`                  | Both scripts         | Core dependency (formerly PIL)     |
| **pyzbar**       | QR/barcode decoding from images      | `pip install pyzbar`                  | qr_to_excel.py       | Wraps ZBar library                 |
| **qrcode**       | QR code generation                   | `pip install qrcode[pil]`             | excel_to_qr.py       | `[pil]` installs Pillow integration|
| **openpyxl**     | Read/write Excel `.xlsx` files       | `pip install openpyxl`                | Both scripts         | Pure Python, no Excel needed       |

**One-line install for everything:**
```bash
pip install pillow pyzbar qrcode[pil] openpyxl
