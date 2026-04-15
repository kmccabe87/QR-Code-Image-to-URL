# QR Toolkit

A streamlined Python tool to:

* Generate QR codes (SVG or PNG) from Excel files
* Decode QR codes from images into Excel spreadsheets

Built for fast, repeatable workflows like **laser engraving, batch QR creation, and data extraction**.

---

# 🚀 Features

* 📊 Automatically detects Excel files in the root folder
* 🧾 Converts spreadsheets → QR code images (SVG or PNG)
* 🖼️ Decodes QR codes from images → Excel
* 📁 Organized output folders (auto-created)
* 📅 Date-stamped decode results
* ⚡ No file browsing or manual paths required

---

# 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/qr-toolkit.git
cd qr-toolkit
```

### 2. Install dependencies

```bash
pip install pandas openpyxl qrcode[pil] pillow opencv-python
```

---

# 📁 Project Structure

```text
QR Code Tool/
│
├── qr_toolkit/
├── Images to Convert to URL's/   ← place images here for decoding
├── data.xlsx                     ← place Excel files here for generation
├── requirements.txt
```

---

# 📊 Excel Format (REQUIRED)

Your spreadsheet must follow this format:

| Column A | Column B |
| -------- | -------- |
| Filename | QR Data  |

### Example:

```text
BR-1    https://example.com/1
BR-2    https://example.com/2
BR-3    WIFI:S:Network;T:WPA;P:password;;
```

* **Column A** → Output filename
* **Column B** → QR code content

---

# 🧾 Generate QR Codes (from Excel)

## SVG (recommended for laser engraving)

```bash
python -m qr_toolkit.cli generate-svg
```

## PNG

```bash
python -m qr_toolkit.cli generate-png
```

### What happens:

* The tool scans the root folder for all `.xlsx` / `.xls` files
* Processes each file automatically
* Generates QR codes

### Output:

```text
QR Code Images/
    BR-1.svg
    BR-2.svg
```

✔ Filenames come directly from Column A
✔ No date added to image names

---

# 🖼️ Decode QR Codes from Images

### 1. Place images in:

```text
Images to Convert to URL's/
```

### Supported formats:

* PNG
* JPG / JPEG
* BMP
* WEBP
* GIF

---

### 2. Run:

```bash
python -m qr_toolkit.cli decode
```

---

### Output:

```text
QR Url's/
    2026-04-15_decoded_qr.xlsx
```

✔ File is saved automatically
✔ Date added to filename
✔ No manual paths required

---

# 📊 Decoded Output Format

| filename  | data                |
| --------- | ------------------- |
| code1.png | https://example.com |
| code2.jpg | WIFI:S:Network;...  |

---

# ⚠️ Important Notes

* ❌ SVG files are **not supported for decoding**
* QR codes must be:

  * clear
  * high contrast
  * not overly stylized
* Large or blurry QR codes may fail to decode

---

# 🔁 Workflow Summary

### Generate QR Codes

```text
Excel → QR Code Images/
```

### Decode QR Codes

```text
Images → QR Url's/
```

---

# 🛠️ Troubleshooting

### No Excel files found

* Make sure `.xlsx` files are in the root folder

### No QR codes detected

* Check image quality (blurry or low contrast may fail)

### Missing modules

```bash
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
