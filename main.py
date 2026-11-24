#!/usr/bin/env python3
"""Entry point for the News Image 24 Nov 2026 front page.

Copies the rendered front page (news.png, drawn by generate.py) to the
entry output directory as entry.png.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "news.png")


def main():
    out_dir = (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
