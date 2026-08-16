import argparse
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

from .excel_io import read_excel, write_results
from .qr_generate import process_generation
from .qr_decode import decode_folder


# -------------------------------
# Confirm Excel Format
# -------------------------------
def confirm_structure():
    root = tk.Tk()
    root.withdraw()

    message = (
        "Excel format:\n\n"
        "Column A = filename\n"
        "Column B = QR code data (URL, text, etc.)\n\n"
        "All Excel files in this folder will be processed.\n\n"
        "Continue?"
    )

    return messagebox.askyesno("Confirm Format", message)


# -------------------------------
# Find Excel Files
# -------------------------------
def find_excel_files(root_dir: Path):
    return list(root_dir.glob("*.xlsx")) + list(root_dir.glob("*.xls"))


# -------------------------------
# Main CLI
# -------------------------------
def main():
    parser = argparse.ArgumentParser(prog="qr-toolkit")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("generate-svg")
    sub.add_parser("generate-png")
    sub.add_parser("decode")

    args = parser.parse_args()

    root_dir = Path.cwd()

    # --------------------------------
    # GENERATE QR CODES
    # --------------------------------
    if args.command in ("generate-svg", "generate-png"):
        excel_files = find_excel_files(root_dir)

        if not excel_files:
            print("No Excel files found in the root folder.")
            return

        if not confirm_structure():
            print("User cancelled.")
            return

        mode = "svg" if args.command == "generate-svg" else "png"

        output_dir = root_dir / "QR Code Images"
        output_dir.mkdir(exist_ok=True)

        for file in excel_files:
            print(f"\nProcessing: {file.name}")

            try:
                df = read_excel(file)

                process_generation(
                    df,
                    output_dir,
                    mode=mode
                )

            except Exception as e:
                print(f"Error processing {file.name}: {e}")

        messagebox.showinfo(
            "Done",
            f"Processed {len(excel_files)} Excel file(s).\n\nSaved to:\n{output_dir}"
        )

    # --------------------------------
    # DECODE QR CODES (AUTO FOLDER)
    # --------------------------------
    elif args.command == "decode":
        # 👉 Hardcoded folder name
        folder = root_dir / "Images to Convert to URL's"

        if not folder.exists():
            print(f"Folder not found: {folder}")
            print("Create a folder named 'Images to Convert to URL's' and add your images.")
            return

        results = decode_folder(folder)

        # 👉 Output folder
        output_dir = root_dir / "QR Url's"
        output_dir.mkdir(exist_ok=True)

        # 👉 Date prefix
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_file = output_dir / f"{date_str}_decoded_qr.xlsx"

        write_results(results, output_file)

        print(f"\nSaved: {output_file}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
