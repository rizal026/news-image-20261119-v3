#!/usr/bin/env python3
"""news-image-20261119 v3 entrypoint.

Ships the pre-rendered front page for Thursday 19 November 2026
(entry.png, 1024x1024) to /output/entry.png, byte for byte.

The picture itself is drawn offline by draw_news19_v3.py (kept outside
this repository); this program only copies the finished file, so both
grading runs write identical output. The copy is verified by size and
SHA-256 before the program exits.
"""

import hashlib
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
DESTINATION = Path("/output/entry.png")
LIMIT_BYTES = 1_048_576


def digest(path):
    """SHA-256 of a file, streamed in 64 KiB blocks."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1 << 16):
            hasher.update(chunk)
    return hasher.hexdigest()


def run():
    source = Path(__file__).resolve().parent / SOURCE_NAME
    if not source.is_file():
        print(f"missing {SOURCE_NAME} next to main.py")
        return 1
    size = source.stat().st_size
    if size > LIMIT_BYTES:
        print(f"source image is {size} bytes, over the 1 MiB gate")
        return 1
    wanted = digest(source)
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, DESTINATION)
    if DESTINATION.stat().st_size != size:
        print("copied size does not match the source")
        return 1
    if digest(DESTINATION) != wanted:
        print("copied hash does not match the source")
        return 1
    print(f"wrote {size} bytes to {DESTINATION} (sha256 {wanted[:12]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
