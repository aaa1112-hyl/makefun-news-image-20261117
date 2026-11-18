#!/usr/bin/env python3
"""Entry for make.fun news-image-20261117.

Ships the front-page image (entry.png, drawn by generate_image.py
from Tuesday 17 November 2026 world news) by copying it to
/output/entry.png. Standard library only, no network, deterministic.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
