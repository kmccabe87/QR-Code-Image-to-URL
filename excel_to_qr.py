# qr_code_generator_from_excel.py
import os
import sys
from pathlib import Path
import pandas as pd
from urllib.parse import urlparse
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

def is_valid_url(string):
    try:
        result = urlparse(string)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except:
        return False


def main():
    print("QR Code Generator from Excel / Spreadsheet")
    print("Supports both .xlsx and .xls files")
    print("-" * 50)

    while True:
        user_input = input("\nEnter the full path to your Excel file (.xlsx or .xls): ").strip()

        # Handle drag-and-drop quotes (common on Windows)
        user_input = user_input.strip('"').strip("'")

        if not user_input:
            print("Please enter a path.")
            continue

        excel_path = Path(user_input)

        if not excel_path.exists():
            print("File not found. Please check the path.")
            continue

        if excel_path.suffix.lower() not in ('.xlsx', '.xls'):
            print("File must be an Excel file (.xlsx or .xls)")
            continue

        break

    # Create output folder next to the script
    script_dir = Path(__file__).parent
    output_folder = script_dir / "qr_codes"
    output_folder.mkdir(exist_ok=True)

    print(f"\nQR codes will be saved to: {output_folder}")
    print("Reading file...")

    success = 0
    skipped = 0
    errors = 0

    try:
        # pandas.read_excel supports both .xls and .xlsx
        df = pd.read_excel(
            excel_path,
            header=None,           # assuming no header row
            usecols=[0, 1],        # columns A and B
            names=['name', 'url'],
            dtype=str
        )

        # Clean up whitespace
        df['name'] = df['name'].str.strip()
        df['url'] = df['url'].str.strip()

        print(f"\nFound {len(df)} rows in the spreadsheet.\n")

        for idx, row in df.iterrows():
            name = row['name']
            url = row['url']

            if pd.isna(name) or not name:
                print(f"Row {idx+2}: Skipping - empty name")
                skipped += 1
                continue

            if pd.isna(url) or not url:
                print(f"Row {idx+2}: Skipping - empty URL ({name})")
                skipped += 1
                continue

            if not is_valid_url(url):
                print(f"Row {idx+2}: Invalid URL skipped → {name} | {url}")
                skipped += 1
                continue

            # Create safe filename
            safe_name = "".join(c for c in name if c.isalnum() or c in " -_()").strip()
            if not safe_name:
                safe_name = f"item_{idx+2}"

            filename = f"{safe_name}.png"
            output_path = output_folder / filename

            # Avoid overwriting
            counter = 1
            while output_path.exists():
                output_path = output_folder / f"{safe_name}_{counter}.png"
                counter += 1

            try:
                # Create QR code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )

                qr.add_data(url)
                qr.make(fit=True)

                # Styled QR: rounded modules + dark blue
                qr_image = qr.make_image(
                    image_factory=StyledPilImage,
                    module_drawer=RoundedModuleDrawer(),
                    color_mask=SolidFillColorMask(
                        front_color=(0, 51, 153),   # dark blue
                        back_color=(255, 255, 255)
                    )
                )

                qr_image.save(output_path)
                success += 1
                print(f"✓ Saved: {output_path.name}")

            except Exception as e:
                print(f"✗ Error creating QR for {name} → {url}")
                print(f"  {str(e)}")
                errors += 1

        print("\n" + "="*60)
        print("Finished!")
        print(f"Successfully created : {success}")
        print(f"Skipped (invalid/empty): {skipped}")
        print(f"Errors               : {errors}")
        print("="*60)

    except ImportError as ie:
        print("\nMissing required package(s):")
        print(str(ie))
        print("\nPlease install the necessary libraries:")
        print("  pip install pandas openpyxl qrcode[pil]")
        print("  For older .xls files you may also need: pip install xlrd")
        sys.exit(1)

    except Exception as e:
        print("\nError reading the Excel file:")
        print(str(e))
        print("\nCommon causes:")
        print("• File is open in Excel → close it first")
        print("• File is damaged or not a real Excel file")
        print("• Missing packages → see installation instructions above")


if __name__ == "__main__":
    try:
        # Early check for critical dependencies
        import pandas
        import qrcode
        import PIL
    except ImportError as e:
        print("Missing required packages!")
        print("Please run:")
        print("  pip install pandas openpyxl qrcode[pil]")
        print("  For old .xls files (Excel 97-2003): pip install xlrd")
        sys.exit(1)

    main()

    # Keep window open when double-clicked (Windows convenience)
    if os.name == 'nt':
        input("\nPress Enter to close...")
