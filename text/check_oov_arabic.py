"""
Check for Out-Of-Vocabulary (OOV) characters in an Arabic dataset.

Run this script BEFORE training.
Any printed character must be:
- Added to symbols.py, OR
- Removed/normalized in the Arabic cleaner
"""

from text.symbols import symbols

symbol_set = set(symbols)


def find_oov_characters(text: str):
    """Return characters not present in the symbol vocabulary."""
    return set(c for c in text if c not in symbol_set)


def main():
    metadata_path = "/home/fred/Projetos/DataQueue/DATASET/jordan_hasan_youtube_v20251224/metadata.csv"

    with open(metadata_path, encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            try:
                _, text = line.strip().split("|", 1)
            except ValueError:
                print(f"[ERROR] Invalid format at line {line_number}")
                continue

            oov_chars = find_oov_characters(text)
            if oov_chars:
                print(f"[OOV] Line {line_number}: {oov_chars}")


if __name__ == "__main__":
    main()
