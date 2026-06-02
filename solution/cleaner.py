#!/usr/bin/env python3
"""Standard solution: clean messy CSV per instruction.md rules."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


def is_non_negative_int(value: str) -> bool:
    return bool(value) and value.isdigit()


def read_logical_rows(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.reader(handle))


def clean_rows(rows: list[list[str]]) -> list[list[str]]:
    header: list[str] | None = None
    cleaned: list[list[str]] = []
    seen: set[tuple[str, ...]] = set()

    for raw_row in rows:
        row = [field.strip() for field in raw_row]

        if not any(row):
            continue

        if header is None:
            header = row
            cleaned.append(header)
            continue

        if len(row) != len(header):
            continue

        if not is_non_negative_int(row[2]):
            continue

        key = tuple(row)
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(row)

    return cleaned


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.csv> <output.csv>", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = read_logical_rows(input_path)
    cleaned = clean_rows(rows)

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerows(cleaned)


if __name__ == "__main__":
    main()
