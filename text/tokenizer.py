"""
Simple character-based tokenizer for VITS2.
"""

from text.symbols import UNK_ID, SPACE_ID

def tokenizer(
    text,
    vocab,
    cleaners,
    language=None,
    cleaned_text=False,
):
    if not cleaned_text:
        for cleaner in cleaners:
            text = cleaner(text)

    token_to_id = vocab["token_to_id"]
    sequence = []

    for ch in text:
        if ch == " ":
            sequence.append(SPACE_ID)
        elif ch in token_to_id:
            sequence.append(token_to_id[ch])
        else:
            sequence.append(UNK_ID)

    return sequence
