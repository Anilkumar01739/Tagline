#!/usr/bin/env python3
"""URLs, bundle names, and product 'Concat' strings -> TagLine. Keeps Rust crate ids (concat-*)."""
from __future__ import annotations

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {
    ".git",
    "target",
    "vendor",
    "node_modules",
    ".cursor",
    "agent-transcripts",
}
SKIP_FILES = {
    "ffmpeg-mobile.log",
    "android-libs.log",
    "rebrand-complete-tagline.py",
    "rebrand-locale-keys-tagline.py",
}
EXT = {
    ".rs",
    ".slint",
    ".md",
    ".py",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".iss",
    ".wxs",
    ".sh",
    ".ps1",
    ".java",
    ".kt",
    ".xml",
    ".svg",
    ".desktop",
    ".entitlements",
    ".plist",
    ".iss",
}

URL_REPLACEMENTS = [
    ("https://api.github.com/repos/jub0t/Concat", "https://api.github.com/repos/anilk/TagLine"),
    ("https://github.com/jub0t/Concat", "https://github.com/anilk/TagLine"),
    ("https://github.com/jub0t/concat", "https://github.com/anilk/TagLine"),
    ("http://github.com/jub0t/Concat", "https://github.com/anilk/TagLine"),
    ("jub0t/Concat", "anilk/TagLine"),
    ("jub0t/concat", "anilk/TagLine"),
    ("https://tagline.standalones.org", "https://github.com/anilk/TagLine"),
    ("http://tagline.standalones.org", "https://github.com/anilk/TagLine"),
    ("tagline.standalones.org", "github.com/anilk/TagLine"),
    ("cdn.jsdelivr.net/gh/jub0t/Concat@", "cdn.jsdelivr.net/gh/anilk/TagLine@"),
    ("www.star-history.com/jub0t/concat", "www.star-history.com/anilk/TagLine"),
    ("contrib.rocks/image?repo=jub0t/concat", "contrib.rocks/image?repo=anilk/TagLine"),
    (
        "flatpark.org/apps/app.concat.editor/",
        "github.com/anilk/TagLine/releases",
    ),
]

# Lines/files where app.concat must stay (legacy Android ids).
LEGACY_PATH_MARKERS = (
    "dirs.rs",
    "TAGLINE-REBRAND.md",
    "android-native",
)


def should_skip_path(path: pathlib.Path) -> bool:
    if path.name in SKIP_FILES:
        return True
    if path.suffix.lower() not in EXT and path.name not in {"PKGBUILD", "Dockerfile"}:
        return False
    rel = path.relative_to(ROOT).as_posix()
    if any(m in rel for m in LEGACY_PATH_MARKERS):
        return False  # still process except we won't replace app.concat in dirs.rs manually
    return any(part in SKIP_DIRS for part in path.parts)


def protect_segments(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Hide concat-* crate paths and font filenames from product renames."""
    tokens: list[tuple[str, str]] = []

    def stash(match: re.Match[str]) -> str:
        key = f"\0TK{len(tokens)}\0"
        tokens.append((key, match.group(0)))
        return key

    text = re.sub(
        r"concat-[a-z0-9_]+|include_bytes!\([^)]*-Concat\.[a-z]+\)",
        stash,
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"app\.concat\.editor", stash, text)
    text = re.sub(r"org\.standalones\.concat", stash, text)
    return text, tokens


def restore_segments(text: str, tokens: list[tuple[str, str]]) -> str:
    for key, original in tokens:
        text = text.replace(key, original)
    return text


def product_concat_to_tagline(text: str) -> str:
    """Replace capital-C Concat product word, not lowercase crate ids."""
    replacements = [
        ("Concat contributors", "TagLine contributors"),
        ("Concat's", "TagLine's"),
        ("Concat-", "TagLine-"),
        (" Concat ", " TagLine "),
        (" Concat.", " TagLine."),
        (" Concat,", " TagLine,"),
        (" Concat:", " TagLine:"),
        (" Concat;", " TagLine;"),
        (' Concat"', ' TagLine"'),
        (" Concat'", " TagLine'"),
        (" Concat)", " TagLine)"),
        ("(Concat", "(TagLine"),
        (" Concat\n", " TagLine\n"),
        ("# Concat", "# TagLine"),
        ("> Concat", "> TagLine"),
        (" Concat<", " TagLine<"),
        ("Concat\n", "TagLine\n"),
        ("Concat.", "TagLine."),
        ("Concat,", "TagLine,"),
        ("Concat:", "TagLine:"),
        ("Concat;", "TagLine;"),
        ("Concat)", "TagLine)"),
        ("Concat]", "TagLine]"),
        ("Concat}", "TagLine}"),
        ("Concat?", "TagLine?"),
        ("Concat!", "TagLine!"),
        ('"Concat"', '"TagLine"'),
        ("'Concat'", "'TagLine'"),
        ("`Concat`", "`TagLine`"),
        ("Builds Concat ", "Builds TagLine "),
        ("build Concat", "build TagLine"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def transform(text: str, path: pathlib.Path) -> str:
    for old, new in URL_REPLACEMENTS:
        text = text.replace(old, new)
    text = re.sub(r"\bConcat\.apk\b", "TagLine.apk", text)
    if path.suffix in {".yml", ".yaml", ".md", ".iss", ".wxs", ".sh", ".ps1", ".json"} or "build-app" in path.name:
        text = re.sub(r"\bConcat-(?=\d|\$|\{|\*)", "TagLine-", text)
        text = re.sub(r"pattern: Concat-\*", "pattern: TagLine-*", text)
    if "dirs.rs" in path.as_posix():
        return text
    protected, tokens = protect_segments(text)
    protected = product_concat_to_tagline(protected)
    return restore_segments(protected, tokens)


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or should_skip_path(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new = transform(text, path)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print(path.relative_to(ROOT))
            changed += 1
    print(f"Updated {changed} files.")


if __name__ == "__main__":
    main()
