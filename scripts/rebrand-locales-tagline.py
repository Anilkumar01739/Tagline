#!/usr/bin/env python3
"""Replace user-visible TagLine with TagLine in locale JSON values."""
import json
import pathlib

LOCALES = (
    pathlib.Path(__file__).resolve().parent.parent
    / "src"
    / "crates"
    / "concat"
    / "locales"
)


def rebrand(value: str) -> str:
    return value.replace("TagLine's", "TagLine's").replace("TagLine", "TagLine")


def main() -> None:
    for path in sorted(LOCALES.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for key, val in data.items():
            if isinstance(val, str):
                new = rebrand(val)
                if new != val:
                    data[key] = new
                    changed = True
        if changed:
            path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(path.name)


if __name__ == "__main__":
    main()
