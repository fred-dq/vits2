"""
Text cleaners for character-based VITS2 training (Arabic).
Cleaners operate ONLY on raw text.
No tokenization, no vocab, no torchtext.
"""

import re
import unicodedata
from text.symbols import symbols

_symbol_set = set(symbols)


# --------------------------------------------------
# Whitespace
# --------------------------------------------------
_whitespace_re = re.compile(r"\s+")


def collapse_whitespace(text: str) -> str:
    return re.sub(_whitespace_re, " ", text).strip()


# --------------------------------------------------
# Arabic diacritics (harakat) Unicode ranges
# --------------------------------------------------
ARABIC_DIACRITICS = re.compile(
    r"""
    [\u0617-\u061A
     \u064B-\u0652
     \u0657-\u065F
     \u0670
     \u06D6-\u06ED]
    """,
    re.VERBOSE,
)


def remove_diacritics(text: str) -> str:
    """Remove Arabic diacritics (harakat)."""
    return re.sub(ARABIC_DIACRITICS, "", text)


# --------------------------------------------------
# Arabic normalization
# --------------------------------------------------
def normalize_arabic(text: str) -> str:
    """
    Normalize Arabic characters to reduce orthographic variance.
    """

    # Normalize Alef variants
    text = re.sub("[إأآا]", "ا", text)

    # Normalize Yaa / Alef Maqsura
    text = re.sub("ى", "ي", text)

    # Normalize Hamza forms
    text = re.sub("ؤ", "و", text)
    text = re.sub("ئ", "ي", text)

    # Normalize Taa Marbuta
    text = re.sub("ة", "ه", text)

    # Persian / Urdu letters → Arabic
    text = re.sub("گ", "ك", text)
    text = re.sub("چ", "ج", text)
    text = re.sub("پ", "ب", text)

    # Lam-Alef ligature
    text = re.sub("ﻻ", "لا", text)

    # Remove Tatweel
    text = re.sub("ـ", "", text)

    return text


def filter_oov_characters(text: str) -> str:
    return "".join(c for c in text if c in _symbol_set)

# --------------------------------------------------
# Main Arabic cleaner
# --------------------------------------------------
def arabic_cleaners(text: str) -> str:
    """
    Arabic text normalization pipeline for character-based TTS.
    """
    text = unicodedata.normalize("NFKC", text)
    text = text.strip()
    text = normalize_arabic(text)
    text = remove_diacritics(text)
    text = collapse_whitespace(text)
    text = filter_oov_characters(text)
    return text
