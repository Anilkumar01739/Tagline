#!/usr/bin/env python3
"""Rename concat-* Rust crates and internal ids to tagline-* (keeps app.concat.editor etc.)."""
from __future__ import annotations

import os
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
CRATES = SRC / "crates"
SKIP_DIRS = {
    ".git",
    "target",
    "vendor",
    "node_modules",
    ".cursor",
    "agent-transcripts",
    "ffmpeg-8.1",
}
SKIP_FILES = {"Cargo.lock", "rebrand-crates-tagline.py", "ffmpeg-mobile.log", "android-libs.log"}
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
    ".nix",
    ".wgsl",
    ".gradle",
    ".kts",
    ".properties",
}

# Do not include bare "concat" here — use PACKAGE rename rules below.
CRATE_DIRS = [
    ("concat-android", "tagline-android"),
    ("concat-api", "tagline-api"),
    ("concat-cli", "tagline-cli"),
    ("concat-core", "tagline-core"),
    ("concat-effects", "tagline-effects"),
    ("concat-export", "tagline-export"),
    ("concat-host", "tagline-host"),
    ("concat-log", "tagline-log"),
    ("concat-mcp", "tagline-mcp"),
    ("concat-media", "tagline-media"),
    ("concat-mobile", "tagline-mobile"),
    ("concat-project", "tagline-project"),
    ("concat-render", "tagline-render"),
    ("concat-server", "tagline-server"),
    ("concat-speech", "tagline-speech"),
    ("concat-text", "tagline-text"),
    ("concat-vision", "tagline-vision"),
    ("concat", "tagline"),
]

HYPHEN_CRATES = sorted({old for old, _ in CRATE_DIRS if "-" in old}, key=len, reverse=True)

PACKAGE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r'name = "concat"'), 'name = "tagline"'),
    (re.compile(r'concat = \{ path = "crates/concat"'), 'tagline = { path = "crates/tagline"'),
    (re.compile(r"crates/concat([^a-zA-Z-])"), r"crates/tagline\1"),
    (re.compile(r"-p concat\b"), "-p tagline"),
    (re.compile(r"--exclude concat\b"), "--exclude tagline"),
    (re.compile(r"concat\.workspace = true"), "tagline.workspace = true"),
    (re.compile(r"concat --mcp"), "tagline --mcp"),
    (re.compile(r"`concat`"), "`tagline`"),
    (re.compile(r"bin concat\b"), "bin tagline"),
    (re.compile(r"run --bin concat\b"), "run --bin tagline"),
    (re.compile(r"CARGO_BIN_EXE_concat\b"), "CARGO_BIN_EXE_tagline"),
    (re.compile(r"package\.concat\b"), "package.tagline"),
    (re.compile(r"concat --"), "tagline --"),
]


def iter_text_files() -> list[pathlib.Path]:
    out: list[pathlib.Path] = []
    for base in (ROOT,):
        for path in base.rglob("*"):
            if path.is_dir():
                continue
            if path.name in SKIP_FILES:
                continue
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if path.suffix.lower() in EXT or path.name in {"PKGBUILD", "Dockerfile", "CMakeLists.txt"}:
                out.append(path)
    return out


def protect_legacy(text: str) -> tuple[str, dict[str, str]]:
    tokens: dict[str, str] = {}
    patterns = [
        r"app\.concat\.editor(?:\.spike)?",
        r"org\.standalones\.concat",
    ]

    def repl(m: re.Match[str]) -> str:
        key = f"__LEGACY_{len(tokens)}__"
        tokens[key] = m.group(0)
        return key

    for pat in patterns:
        text = re.sub(pat, repl, text)
    return text, tokens


def restore_legacy(text: str, tokens: dict[str, str]) -> str:
    for key, val in tokens.items():
        text = text.replace(key, val)
    return text


SOUNDS_UI = [
    ("ConcatState", "TaglineSoundsState"),
    ("ConcatLoaded", "TaglineSoundsLoaded"),
    ("sounds_concat", "sounds_tagline"),
    ("in property <[SoundCardData]> concat;", "in property <[SoundCardData]> tagline-sounds;"),
    ("concat-state", "tagline-sounds-state"),
    ("concat-category", "tagline-sounds-category"),
    ("load-concat", "load-tagline-sounds"),
    ("concat-category-changed", "tagline-sounds-category-changed"),
    ("set_concat(", "set_tagline_sounds("),
    ("set_concat_state", "set_tagline_sounds_state"),
    ("set_concat_category", "set_tagline_sounds_category"),
    ("on_load_concat", "on_load_tagline_sounds"),
    ("on_concat_category_changed", "on_tagline_sounds_category_changed"),
    ("pub concat: TaglineSoundsState", "pub tagline_sounds: TaglineSoundsState"),
    ("self.concat ", "self.tagline_sounds "),
    ("self.concat=", "self.tagline_sounds="),
    ("self.concat,", "self.tagline_sounds,"),
    ("self.concat)", "self.tagline_sounds)"),
    ("self.concat ==", "self.tagline_sounds =="),
    ("self.concat !=", "self.tagline_sounds !="),
    ("self.sounds.concat", "self.sounds.tagline_sounds"),
    ("concat_rows", "tagline_sounds_rows"),
]


def transform_content(text: str, path: pathlib.Path) -> str:
    text, tokens = protect_legacy(text)

    for old, new in SOUNDS_UI:
        text = text.replace(old, new)

    for old in HYPHEN_CRATES:
        new = old.replace("concat", "tagline", 1)
        text = text.replace(old, new)

    for pattern, repl in PACKAGE_PATTERNS:
        text = pattern.sub(repl, text)

    # Effect / manifest ids (not app.__LEGACY__)
    text = re.sub(r"(?<!app\.)\bconcat\.", "tagline.", text)

    # Rust crate module paths and env keys (after hyphen crate names).
    text = re.sub(r"\bconcat_", "tagline_", text)

    text = text.replace("concat.json", "tagline.json")
    text = text.replace("tagline.json.saving", "tagline.json.saving")  # idempotent
    text = text.replace("concat.lock", "tagline.lock")
    text = text.replace("concat_version", "tagline_version")
    text = text.replace("concat-spike", "tagline-spike")
    text = text.replace("concat_logo_512", "tagline_logo_512")
    text = text.replace("new_concat_logo", "new_tagline_logo")
    text = text.replace("/opt/concat/", "/opt/tagline/")
    text = text.replace('Exec=concat', "Exec=tagline")
    text = text.replace("concat.desktop", "tagline.desktop")
    text = text.replace("concat.png", "tagline.png")
    text = text.replace('pname = "concat"', 'pname = "tagline"')
    text = text.replace('name = "concat"', 'name = "tagline"')

    text = restore_legacy(text, tokens)
    return text


def rewrite_files() -> int:
    changed = 0
    for path in iter_text_files():
        try:
            raw = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new = transform_content(raw, path)
        if new != raw:
            path.write_text(new, encoding="utf-8", newline="\n")
            changed += 1
    return changed


def rename_effect_packages() -> int:
    packages = CRATES / "concat-effects" / "packages"
    if not packages.is_dir():
        packages = CRATES / "tagline-effects" / "packages"
    n = 0
    for entry in sorted(packages.iterdir()):
        if not entry.is_dir():
            continue
        name = entry.name
        if not name.startswith("concat."):
            continue
        new_name = "tagline." + name[len("concat.") :]
        dest = entry.parent / new_name
        if dest.exists():
            continue
        entry.rename(dest)
        n += 1
    return n


def rename_card_jpegs() -> int:
    for cards in (
        CRATES / "concat" / "cards",
        CRATES / "tagline" / "cards",
    ):
        if not cards.is_dir():
            continue
        n = 0
        for jpg in cards.glob("concat.*.jpg"):
            dest = jpg.with_name("tagline." + jpg.name[len("concat.") :])
            jpg.rename(dest)
            n += 1
        return n
    return 0


def rename_crate_dirs() -> None:
    for old, new in CRATE_DIRS:
        src = CRATES / old
        dst = CRATES / new
        if not src.is_dir():
            if dst.is_dir():
                continue
            raise SystemExit(f"missing crate dir {src}")
        if dst.exists():
            continue
        src.rename(dst)


def rename_mcp_bin() -> None:
    for base in ("tagline-mcp", "concat-mcp"):
        crate = CRATES / base
        if not crate.is_dir():
            continue
        old = crate / "src" / "bin" / "concat-mcp.rs"
        new = crate / "src" / "bin" / "tagline-mcp.rs"
        if old.is_file():
            old.rename(new)
        return


def main() -> None:
    os.chdir(ROOT)
    n_files = rewrite_files()
    print(f"rewrote {n_files} files")
  # dirs must match updated paths in Cargo.toml
    n_fx = rename_effect_packages()
    print(f"renamed {n_fx} effect package folders")
    n_cards = rename_card_jpegs()
    print(f"renamed {n_cards} card jpgs")
    rename_crate_dirs()
    print("renamed crate directories")
    rename_mcp_bin()
    print("done")


if __name__ == "__main__":
    main()
