#!/usr/bin/env python3
"""CONCAT_* environment variable names → TAGLINE_* (phase 2)."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = {"target", "vendor", "node_modules", ".git", "patches/whisper-rs-sys"}
EXT = {".rs", ".sh", ".ps1", ".md", ".slint", ".toml", ".yml", ".yaml", ".json", ".kt", ".java"}

for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix not in EXT:
        continue
    if any(part in SKIP for part in path.parts):
        continue
    if path.name == "rebrand-phase2-env.py":
        continue
    text = path.read_text(encoding="utf-8")
    new = re.sub(r"CONCAT_([A-Z0-9_]+)", r"TAGLINE_\1", text)
    if new != text:
        path.write_text(new, encoding="utf-8")
        print(path.relative_to(ROOT))
