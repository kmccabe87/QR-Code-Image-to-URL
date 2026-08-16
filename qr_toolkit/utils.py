import re
from pathlib import Path
from urllib.parse import urlparse


def is_valid_url(value: str) -> bool:
    try:
        result = urlparse(value)
        return result.scheme in ("http", "https") and result.netloc
    except Exception:
        return False


def sanitize_filename(text: str, max_length=80) -> str:
    text = str(text).strip()
    text = text.replace(" ", "_")
    text = re.sub(r'[\\/:*?"<>|]', "", text)
    return text[:max_length] if text else "qr_code"


def ensure_output_dir(base_path: Path, name="qr_output") -> Path:
    output_dir = base_path / name
    output_dir.mkdir(exist_ok=True)
    return output_dir


def avoid_overwrite(path: Path) -> Path:
    if not path.exists():
        return path

    counter = 1
    new_path = path
    while new_path.exists():
        new_path = path.with_stem(f"{path.stem}_{counter}")
        counter += 1
    return new_path
