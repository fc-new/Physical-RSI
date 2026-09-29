#!/usr/bin/env python3
"""Render the generated reading-list section in README.md."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from validate_reading_list import DATA_PATH, ROOT, load_data


README_PATH = ROOT / "README.md"
START = "<!-- BEGIN GENERATED READING LIST -->"
END = "<!-- END GENERATED READING LIST -->"


def render_section(payload: dict) -> str:
    chunks = [START]
    for category in payload["categories"]:
        chunks.extend((f"## {category['title']}", "", category["description"], ""))
        for entry in category["entries"]:
            tags = ", ".join(entry["tags"])
            chunks.append(
                f"- [{entry['title']}]({entry['url']}) -- {entry['authors']}, {entry['year']}. "
                f"Tags: {tags}. {entry['note']}"
            )
        chunks.append("")
    chunks.append(END)
    return "\n".join(chunks)


def replace_section(readme: str, section: str) -> str:
    start = readme.find(START)
    end = readme.find(END)
    if start == -1 or end == -1 or end < start:
        raise ValueError("README.md must contain both generated-section markers")
    end += len(END)
    return readme[:start] + section + readme[end:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if README.md is not up to date")
    args = parser.parse_args()

    # load_data also validates the source before generating anything.
    payload = load_data()
    rendered = replace_section(README_PATH.read_text(encoding="utf-8"), render_section(payload))
    current = README_PATH.read_text(encoding="utf-8")
    if args.check:
        if current != rendered:
            print("README.md: generated reading list is stale; run `make render`", file=sys.stderr)
            return 1
        print("README.md: generated reading list is up to date")
        return 0

    README_PATH.write_text(rendered, encoding="utf-8")
    print(f"rendered {DATA_PATH.relative_to(ROOT)} into {README_PATH.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
