#!/usr/bin/env python3
"""Validation logic executed inside the Docker container."""

from __future__ import annotations

import csv
import hashlib
import os
import sys
from pathlib import Path

INPUT_PATH = Path(os.environ.get("BENCHMARK_INPUT", "/workspace/data/dirty_data.csv"))
OUTPUT_PATH = Path(os.environ.get("BENCHMARK_OUTPUT", "/workspace/output/clean.csv"))

EXPECTED_ROWS = [
    ["name", "email", "score"],
    ["Alice", "alice@example.com", "95"],
    ["Bob", "bob@example.com", "88"],
    ["Frank", "frank@example.com", "80"],
    ["Ivy", "ivy@example.com", "70"],
]

INPUT_SHA256 = "5414766b1c8b025bbf708f3d248ab282635639dbdf90d9348135421fece73dc0"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def read_rows(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.reader(handle))


def verify_output_not_copy_of_input() -> None:
    if not OUTPUT_PATH.exists():
        fail("output file was not created")

    output_text = OUTPUT_PATH.read_text(encoding="utf-8")
    input_text = INPUT_PATH.read_text(encoding="utf-8-sig")

    if output_text.strip() == input_text.strip():
        fail("output appears to be an unmodified copy of the input")

    output_rows = read_rows(OUTPUT_PATH)
    if len(output_rows) >= len(read_rows(INPUT_PATH)):
        fail("output should contain fewer rows than the dirty input after cleaning")


def verify_expected_content() -> None:
    rows = read_rows(OUTPUT_PATH)
    if rows != EXPECTED_ROWS:
        fail(
            "cleaned CSV does not match expected rows\n"
            f"expected: {EXPECTED_ROWS!r}\n"
            f"actual:   {rows!r}"
        )


def verify_format_rules() -> None:
    raw = OUTPUT_PATH.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        fail("output must not include a UTF-8 BOM")

    if b"\r\n" in raw:
        fail("output must use Unix line endings only")

    rows = read_rows(OUTPUT_PATH)
    if not rows:
        fail("output is empty")

    header_len = len(rows[0])
    for index, row in enumerate(rows):
        if len(row) != header_len:
            fail(f"row {index} has inconsistent column count")

        for field in row:
            if field != field.strip():
                fail(f"row {index} contains untrimmed whitespace")

    data_rows = [tuple(row) for row in rows[1:]]
    if len(data_rows) != len(set(data_rows)):
        fail("output contains duplicate data rows")

    for row in rows[1:]:
        score = row[2]
        if not score.isdigit():
            fail(f"invalid score value in output: {score!r}")


def verify_input_unmodified() -> None:
    digest = hashlib.sha256(INPUT_PATH.read_bytes()).hexdigest()
    if digest != INPUT_SHA256:
        fail("input fixture was modified inside the container")


def main() -> None:
    verify_output_not_copy_of_input()
    verify_expected_content()
    verify_format_rules()
    verify_input_unmodified()
    print("PASS: cleaned CSV satisfies all benchmark checks")
    sys.exit(0)


if __name__ == "__main__":
    main()
