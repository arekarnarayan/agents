import os
import sys
from pathlib import Path

THRESHOLD_MB = 500
THRESHOLD_BYTES = THRESHOLD_MB * 1024 * 1024

def get_folder_size(path: Path) -> int:
    total = 0
    for p in path.rglob('*'):
        if p.is_file():
            try:
                total += p.stat().st_size
            except Exception:
                pass
    return total

def scan_path(path: Path):
    results = []
    # Check files
    for file in path.rglob('*'):
        if file.is_file():
            try:
                size = file.stat().st_size
                if size > THRESHOLD_BYTES:
                    results.append((size, f"FILE: {file}"))
            except Exception:
                pass
    # Check folders
    for folder in [p for p in path.rglob('*') if p.is_dir()]:
        try:
            size = get_folder_size(folder)
            if size > THRESHOLD_BYTES:
                results.append((size, f"FOLDER: {folder}"))
        except Exception:
            pass
    # Sort and print
    results.sort(reverse=True, key=lambda x: x[0])
    for size, label in results:
        print(f"{label} - {size / (1024*1024):.2f} MB")

def main():
    if len(sys.argv) > 1:
        base_path = Path(sys.argv[1])
    else:
        base_path = Path('.')
    if not base_path.exists():
        print(f"Path does not exist: {base_path}")
        sys.exit(1)
    print(f"Scanning: {base_path.resolve()}")
    scan_path(base_path)

if __name__ == "__main__":
    main()
