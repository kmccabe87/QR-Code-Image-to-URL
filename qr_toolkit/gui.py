import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from .excel_io import read_excel
from .qr_generate import process_generation
from .utils import ensure_output_dir


def run_gui():
    root = tk.Tk()
    root.withdraw()

    file = filedialog.askopenfilename()

    if not file:
        return

    try:
        df = read_excel(file)
        output_dir = ensure_output_dir(Path(file).parent)

        process_generation(df, output_dir, mode="svg")

        messagebox.showinfo("Done", f"Saved to:\n{output_dir}")

    except Exception as e:
        messagebox.showerror("Error", str(e))
