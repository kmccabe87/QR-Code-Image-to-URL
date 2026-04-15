# QR Toolkit

A streamlined Python tool for two core tasks:

* Generate **QR code SVGs from Excel spreadsheets**
* Extract **URLs/data from QR code images (PNG, JPG, etc.) into Excel**

Built for efficient workflows like **laser engraving, batch QR creation, and data recovery**.

---

# 🚀 What This Tool Does

### 1. Generate QR Codes

* Input: Excel spreadsheet
* Output: **SVG QR codes**

### 2. Extract QR Data

* Input: Image files (PNG, JPG, etc.)
* Output: Excel spreadsheet with decoded URLs/data

---

# 📦 Installation

### Clone the repository

```bash id="y2b0rs"
git clone https://github.com/yourusername/qr-toolkit.git
cd qr-toolkit
```

### Install dependencies

```bash id="gkqz2q"
pip install pandas openpyxl qrcode[pil] pillow opencv-python
```

---

# 📁 Project Structure

```text id="e7q6hx"
QR Code Tool/
│
├── qr_toolkit/
├── Images to Convert to URL's/   ← place QR images here
├── data.xlsx                     ← place Excel files here
├── requirements.txt
```

---

# 📊 Excel Format (FOR QR GENERATION)

Your spreadsheet must follow this structure:

| Column A | Column B |
| -------- | -------- |
| Filename | QR Data  |

### Example:

```text id="5u5a3y"
BR-1    https://example.com/1
BR-2    https://example.com/2
```

* **Column A** → SVG filename
* **Column B** → QR code content (URL, text, WiFi config, etc.)

---

# 🧾 Generate QR Code SVGs

```bash id="gdx3pg"
python -m qr_toolkit.cli generate-svg
```

### What happens:

* Scans the root folder for all `.xlsx` / `.xls` files
* Converts each row into a QR code
* Saves SVG files automatically

---

### Output:

```text id="6w6s9c"
QR Code Images/
    BR-1.svg
    BR-2.svg
```

✔ Filenames come from Column A
✔ No renaming or date added

---

# 🖼️ Convert QR Code Images → URLs

### 1. Place images in:

```text id="3q3z1c"
Images to Convert to URL's/
```

Supported formats:

* PNG
* JPG / JPEG
* BMP
* WEBP
* GIF

---

### 2. Run:

```bash id="r3lqdp"
python -m qr_toolkit.cli decode
```

---

### Output:

```text id="j9c3tt"
QR Url's/
    2026-04-15_decoded_qr.xlsx
```

✔ Contains:

* Column A → image filename
* Column B → decoded URL/data
  ✔ File is automatically date-stamped

---

# 🔁 Workflow Summary

### Generate QR Codes

```text id="k1k3c9"
Excel (URLs) → SVG QR Codes
```

### Extract URLs

```text id="y9p8tr"
QR Images (PNG/JPG) → Excel (URLs)
```

---

# ⚠️ Important Notes

* ❌ Only SVG output is supported for QR generation
* ❌ SVG files are NOT supported for decoding
* QR codes must be:

  * clear
  * high contrast
  * not overly stylized

---

# 🛠️ Troubleshooting

### No Excel files found

* Ensure `.xlsx` files are in the root folder

### No QR codes detected

* Check image quality (blurry or low contrast may fail)

### Missing modules

```bash id="q4y7m1"
pip install pandas pillow opencv-python qrcode[pil] openpyxl
```

---

# 📄 License

MIT License (or your choice)

---

# 🙌 Built With

* qrcode
* OpenCV
* pandas
* Pillow
