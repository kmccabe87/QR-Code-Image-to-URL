import pandas as pd


def read_excel(file_path):
    df = pd.read_excel(file_path, usecols=[0, 1], dtype=str)
    df.columns = ["name", "data"]

    df["name"] = df["name"].astype(str).str.strip()
    df["data"] = df["data"].astype(str).str.strip()

    return df


def write_results(results, output_file):
    df = pd.DataFrame(results)
    df.to_excel(output_file, index=False)
