#!/usr/bin/env python3
"""Replace product name TagLine with TagLine in README sources (not repo paths)."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Keep upstream paths and hostnames; change the product name in prose.
REPLACEMENTS = [
    ("TagLine's", "TagLine's"),
    ("Concat editor", "TagLine editor"),
    ("Concat API", "TagLine API"),
    ("TagLine-", "TagLine-"),  # README "Concat-API" style rare
    ("Concat ", "TagLine "),
    ("TagLine.", "TagLine."),
    ("TagLine,", "TagLine,"),
    ("TagLine:", "TagLine:"),
    ("TagLine;", "TagLine;"),
    ("Concat\"", "TagLine\""),
    ("Concat'", "TagLine'"),
    ("TagLine)", "TagLine)"),
    ("(TagLine", "(TagLine"),
    ("Concat\n", "TagLine\n"),
    ("Concat</", "TagLine</"),
    ("TagLine.app", "TagLine.app"),
    ("Download TagLine", "Download TagLine"),
    ("edit with TagLine", "edit with TagLine"),
    ("Join TagLine", "Join TagLine"),
    ("Driving TagLine", "Driving TagLine"),
    ("the TagLine ", "the TagLine "),
]

SKIP_URL_FRAGMENT = ("anilk/TagLine", "github.com/jub0t", "flatpark.org/apps/app.concat")


def rebrand_text(text: str) -> str:
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text


def main() -> None:
    paths = [ROOT / "README.md", ROOT / "docs"]
    paths.extend((ROOT / "scripts" / "readme").glob("*.py"))
    for path in sorted(paths):
        if path.is_dir():
            for file in path.glob("README*.md"):
                _process(file)
            continue
        _process(path)


def _process(path: pathlib.Path) -> None:
    if path.suffix not in {".md", ".py"}:
        return
    text = path.read_text(encoding="utf-8")
    new = rebrand_text(text)
    if new != text:
        path.write_text(new, encoding="utf-8")
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
