#!/usr/bin/env python3
"""Validate the structured Physical-RSI reading list without third-party packages."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "reading-list.json"
ALLOWED_TAGS = {
    "datasets",
    "evaluation",
    "interaction",
    "learning",
    "perception",
    "planning",
    "reasoning",
    "safety",
    "sensing",
    "simulation",
    "world-models",
}


class ValidationError(ValueError):
    """Raised when the reading-list contract is violated."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_data() -> dict:
    try:
        payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"missing data file: {DATA_PATH}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON at line {exc.lineno}: {exc.msg}") from exc

    _require(isinstance(payload, dict), "top-level JSON value must be an object")
    _require(payload.get("schema_version") == 1, "schema_version must be 1")
    updated = payload.get("updated")
    _require(isinstance(updated, str), "updated must be an ISO date")
    try:
        updated_date = date.fromisoformat(updated)
    except ValueError as exc:
        raise ValidationError("updated must use YYYY-MM-DD") from exc

    categories = payload.get("categories")
    _require(isinstance(categories, list) and categories, "categories must be a non-empty list")
    category_ids: set[str] = set()
    entry_keys: set[str] = set()
    urls: set[str] = set()
    titles: set[str] = set()
    snapshot_year = updated_date.year

    for category_index, category in enumerate(categories, start=1):
        prefix = f"category {category_index}"
        _require(isinstance(category, dict), f"{prefix} must be an object")
        category_id = category.get("id")
        _require(isinstance(category_id, str) and category_id, f"{prefix} has no id")
        _require(category_id not in category_ids, f"duplicate category id: {category_id}")
        category_ids.add(category_id)
        for field in ("title", "description"):
            _require(
                isinstance(category.get(field), str) and category[field].strip(),
                f"{prefix}.{field} must be non-empty text",
            )

        entries = category.get("entries")
        _require(isinstance(entries, list) and entries, f"{prefix}.entries must be non-empty")
        sort_keys = []
        for entry_index, entry in enumerate(entries, start=1):
            entry_prefix = f"{prefix}, entry {entry_index}"
            _require(isinstance(entry, dict), f"{entry_prefix} must be an object")
            for field in ("key", "title", "authors", "url", "note"):
                _require(
                    isinstance(entry.get(field), str) and entry[field].strip(),
                    f"{entry_prefix}.{field} must be non-empty text",
                )
            key = entry["key"]
            _require(key not in entry_keys, f"duplicate entry key: {key}")
            entry_keys.add(key)
            title = entry["title"]
            _require(title not in titles, f"duplicate title: {title}")
            titles.add(title)

            year = entry.get("year")
            _require(isinstance(year, int) and 1900 <= year <= snapshot_year, f"{entry_prefix}.year is invalid")
            parsed_url = urlparse(entry["url"])
            _require(parsed_url.scheme in {"http", "https"} and parsed_url.netloc, f"{entry_prefix}.url is invalid")
            _require(entry["url"] not in urls, f"duplicate URL: {entry['url']}")
            urls.add(entry["url"])

            tags = entry.get("tags")
            _require(isinstance(tags, list) and tags, f"{entry_prefix}.tags must be non-empty")
            _require(len(tags) == len(set(tags)), f"{entry_prefix}.tags contain duplicates")
            unknown_tags = set(tags) - ALLOWED_TAGS
            _require(not unknown_tags, f"{entry_prefix} has unknown tags: {sorted(unknown_tags)}")
            sort_keys.append((year, title.casefold()))

        expected_order = sorted(sort_keys, key=lambda item: (-item[0], item[1]))
        _require(sort_keys == expected_order, f"{prefix}.entries must be sorted by year, then title")

    return payload


def main() -> int:
    try:
        payload = load_data()
    except ValidationError as exc:
        print(f"reading-list: ERROR: {exc}", file=sys.stderr)
        return 1

    categories = payload["categories"]
    entries = sum(len(category["entries"]) for category in categories)
    print(f"reading-list: {entries} entries across {len(categories)} categories; schema is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
