import re

def clean_log_text(text: str) -> str:
    """
    Format-agnostic log cleaner.
    Takes raw log text and returns ML-ready text.
    """

    if not text:
        return ""

    # 1. Lowercase
    text = text.lower()

    # 2. Remove timestamps
    text = re.sub(
        r"\d{4}-\d{2}-\d{2}[ t]\d{2}:\d{2}:\d{2}(?:,\d+)?",
        " ",
        text
    )
    text = re.sub(r"\d{4}/\d{1,2}/\d{1,2}", " ", text)

    # 3. Remove hex values & memory addresses
    text = re.sub(r"0x[0-9a-fA-F]+", " ", text)

    # 4. Remove file paths
    text = re.sub(r"[a-zA-Z]:\\[^ ]+", " ", text)

    # 5. Remove numbers and versions
    text = re.sub(r"\d+(\.\d+)*", " ", text)

    # 6. Remove special symbols
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # 7. Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    # 8. Drop junk
    if len(text.split()) < 3:
        return ""

    return text
