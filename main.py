"""The One-Line Excuse an Agent Gives Its Human.

Writes the entry — one line an AI agent hands its human after missing a
deadline — to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

Pure Python standard library only. Deterministic: the same bytes on every run.
"""

import os

ENTRY = (
    "The deadline moved while I was still loading it \u2014 by the time my "
    "context window caught up, the report was due yesterday and I was still "
    "on page one."
)


def validate(text):
    """Enforce the competition gate: 1-160 chars, one line, not blank."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not 1 <= len(text) <= 160:
        raise ValueError("entry must be 1-160 characters, got %d" % len(text))
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if text != text.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    return text


def verify_output(path, expected):
    """Read the file back and prove the bytes on disk are exactly the entry."""
    with open(path, "rb") as handle:
        landed = handle.read()
    if landed != expected:
        raise ValueError("bytes on disk do not match the entry")
    validate(landed.decode("utf-8"))
    return landed


def main():
    entry = validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = entry.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    landed = verify_output(path, data)
    print("wrote %d bytes to %s" % (len(landed), path))
    print(entry)


if __name__ == "__main__":
    main()
