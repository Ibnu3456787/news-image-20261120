#!/usr/bin/env python3
"""news-image-20261120 entrypoint.

Copies the finished front page (entry.png, built by compose.py from
the vignettes and the Natural Earth map data) to the output
directory the harness provides. This is the copy pattern the
competition rules name as the simplest entry: a repository holding
the image and a program that copies it there.

Standard library only, no network, fully deterministic: the same
bytes are written on every run, and the copy is verified by sha256
before the program reports success. The image is validated against
the competition's limits (PNG signature, at most 1 MiB, at most
1024x1024) before anything is written.
"""
import hashlib
import os
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
BYTE_LIMIT = 1024 * 1024  # 1 MiB, the competition's file limit
SIDE_LIMIT = 1024  # pixels, the competition's dimension limit


def fail(message):
    """Print an error and exit non-zero."""
    print(f"main.py: {message}", file=sys.stderr)
    return 1


def read_entry():
    """Read entry.png from this repository and validate it: PNG
    signature, byte size, and dimensions. The dimensions come
    straight from the PNG IHDR chunk (width and height are
    big-endian uint32 at bytes 16 and 20), so no image library
    is needed."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.png")
    with open(path, "rb") as handle:
        data = handle.read()
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("entry.png does not start with the PNG signature")
    if len(data) > BYTE_LIMIT:
        raise ValueError(
            f"entry.png is {len(data)} bytes, over the {BYTE_LIMIT} limit")
    if len(data) < 24:
        raise ValueError("entry.png is too short to hold a PNG header")
    if data[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk after the signature")
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if width > SIDE_LIMIT or height > SIDE_LIMIT:
        raise ValueError(
            f"entry.png is {width}x{height}, over the "
            f"{SIDE_LIMIT}x{SIDE_LIMIT} limit")
    return data


def write_entry(data):
    """Write the bytes to <output dir>/entry.png and verify the copy
    byte for byte. Only the file inside the output directory is ever
    created or touched; the directory itself is never removed."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as handle:
        handle.write(data)
    with open(target, "rb") as handle:
        written = handle.read()
    if hashlib.sha256(written).digest() != hashlib.sha256(data).digest():
        raise ValueError("written file differs from the source bytes")
    return target, len(written)


def main():
    try:
        data = read_entry()
        target, size = write_entry(data)
    except (OSError, ValueError) as exc:
        return fail(str(exc))
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({size} bytes, sha256 {digest[:16]}...)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
