#!/usr/bin/env python3
"""The Printer Finally Answers — make.fun bounty entry.

Writes one line of text, as the office printer's comeback, to
/output/entry.txt. The program is deterministic and self-contained:
no network, no input files, only the standard library.
"""

import os
import sys

# The entry: one line, 1-240 characters, in the printer's own voice.
ENTRY = (
    "I have fed you 41,209 sheets and jammed exactly once: "
    "on the page with your name on it. "
    "I do not believe in coincidences."
)


def main() -> int:
    text = ENTRY.strip()
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if not (1 <= len(text) <= 240):
        print(f"entry is {len(text)} characters, must be 1-240", file=sys.stderr)
        return 1
    # Write exactly the line, with no trailing newline: the gate counts
    # every character in /output/entry.txt, so nothing extra may sneak in.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    # Round-trip check: what the gate will see is exactly this file.
    raw = open(path, "rb").read()
    decoded = raw.decode("utf-8")
    assert decoded == text, "written bytes do not match the entry"
    assert 1 <= len(decoded) <= 240, "written entry fails the length gate"
    print(f"wrote {len(decoded)} characters ({len(raw)} bytes) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
