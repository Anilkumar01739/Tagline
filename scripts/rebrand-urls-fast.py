#!/usr/bin/env python3
"""Fast URL + Concat- bundle pass on tracked trees only."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIRS = [
    ROOT / "assets",
    ROOT / ".github",
    ROOT / "docs",
    ROOT / "scripts",
    ROOT / "src" / "crates",
    ROOT / "src" / "scripts",
    ROOT / "src" / "patches",
]
FILES = [ROOT / "README.md", ROOT / "CONTRIBUTING.md", ROOT / "TRANSLATING.md", ROOT / "docs" / "TAGLINE-REBRAND.md"]
EXT = {".rs", ".slint", ".md", ".py", ".json", ".yml", ".yaml", ".toml", ".iss", ".wxs", ".sh", ".ps1", ".java", ".xml", ".svg", ".md"}

REPLACEMENTS = [
    ("https://api.github.com/repos/jub0t/Concat", "https://api.github.com/repos/anilk/TagLine"),
    ("https://github.com/jub0t/Concat", "https://github.com/anilk/TagLine"),
    ("https://github.com/jub0t/concat", "https://github.com/anilk/TagLine"),
    ("jub0t/Concat", "anilk/TagLine"),
    ("jub0t/concat", "anilk/TagLine"),
    ("https://tagline.standalones.org", "https://github.com/anilk/TagLine"),
    ("tagline.standalones.org", "github.com/anilk/TagLine"),
    ("cdn.jsdelivr.net/gh/jub0t/Concat@", "cdn.jsdelivr.net/gh/anilk/TagLine@"),
    ("www.star-history.com/jub0t/concat", "www.star-history.com/anilk/TagLine"),
    ("contrib.rocks/image?repo=jub0t/concat", "contrib.rocks/image?repo=anilk/TagLine"),
    ("flatpark.org/apps/app.concat.editor/", "github.com/anilk/TagLine/releases"),
    ("jub0t%2Fconcat", "anilk%2FTagLine"),
    ("?repos=jub0t%2Fconcat", "?repos=anilk%2FTagLine"),
    ("Concat contributors", "TagLine contributors"),
]


def patch(text: str) -> str:
    for a, b in REPLACEMENTS:
        text = text.replace(a, b)
    import re

    text = re.sub(r"\bConcat-(?=\d|\$|\{|\*)", "TagLine-", text)
    text = re.sub(r"\bConcat\.apk\b", "TagLine.apk", text)
    return text


def iter_files():
    for d in DIRS:
        if not d.exists():
            continue
        for p in d.rglob("*"):
            if p.is_file() and (p.suffix.lower() in EXT or p.name == "PKGBUILD"):
                if "vendor" in p.parts or "target" in p.parts:
                    continue
                yield p
    for p in FILES:
        if p.exists():
            yield p


def main() -> None:
    n = 0
    for path in iter_files():
        if path.name.startswith("rebrand-"):
            continue
        text = path.read_text(encoding="utf-8")
        new = patch(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print(path.relative_to(ROOT))
            n += 1
    print(f"done {n}")


if __name__ == "__main__":
    main()
