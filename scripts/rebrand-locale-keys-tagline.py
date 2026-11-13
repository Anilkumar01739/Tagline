#!/usr/bin/env python3
"""Rename locale keys and code refs that still say Concat."""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOCALES = ROOT / "src" / "crates" / "concat" / "locales"

KEY_MAP = {
    "settings.tagline": "settings.tagline",
    "settings.taglineMirror": "settings.taglineMirror",
    "settings.servesTagLineApiWhile": "settings.servesTagLineApiWhile",
    "start.notTagLineProjectFolder": "start.notTagLineProjectFolder",
}

CODE_REPLACEMENTS = [
    ('"settings.tagline"', '"settings.tagline"'),
    ('"settings.taglineMirror"', '"settings.taglineMirror"'),
    ('"settings.servesTagLineApiWhile"', '"settings.servesTagLineApiWhile"'),
    ('"start.notTagLineProjectFolder"', '"start.notTagLineProjectFolder"'),
    ("SoundsMsg::LoadTagLine", "SoundsMsg::LoadTagLine"),
    ("LoadTagLine,", "LoadTagLine,"),
    ("LoadTagLine =>", "LoadTagLine =>"),
    ("TagLineCategory", "TagLineCategory"),
    ("LoadTagLine)", "LoadTagLine)"),
]


def rename_locale_keys() -> None:
    for path in sorted(LOCALES.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        out = {}
        for key, value in data.items():
            out[KEY_MAP.get(key, key)] = value
        path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))


def patch_code() -> None:
    bases = [ROOT / "src" / "crates", ROOT / "scripts"]
    for base in bases:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in {".rs", ".slint", ".py"}:
                continue
            text = path.read_text(encoding="utf-8")
            new = text
            for old, rep in CODE_REPLACEMENTS:
                new = new.replace(old, rep)
            if new != text:
                path.write_text(new, encoding="utf-8")
                print(path.relative_to(ROOT))


def main() -> None:
    rename_locale_keys()
    patch_code()


if __name__ == "__main__":
    main()
