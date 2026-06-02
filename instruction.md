# CSV Cleaner CLI

## Overview

Build a Python command-line tool named `cleaner.py` that reads a messy CSV file and writes a cleaned CSV file.

The evaluator provides:

- Input path (first argument)
- Output path (second argument)

Example:

```bash
python cleaner.py /workspace/data/dirty_data.csv /workspace/output/clean.csv
```

Paths inside the benchmark Docker image:

- Input: `/workspace/data/dirty_data.csv`
- Output: `/workspace/output/clean.csv`

## Input format

- UTF-8 text, optionally prefixed with a UTF-8 BOM (`\ufeff`)
- Comma-separated values
- The first non-empty row is the header
- Later rows are data rows

## Cleaning rules

Apply these rules in order:

1. **Header**
   - Use the first non-empty row as the header.
   - Trim leading and trailing whitespace from every header field.
   - The header defines the expected number of columns for all data rows.

2. **Skip invalid data rows** — do not write these to the output:
   - Completely empty rows (all fields empty after trimming)
   - Rows whose column count differs from the header column count
   - Rows where the `score` column (third column, index `2`) is not a non-negative integer (`0`, `1`, `2`, ...)

3. **Normalize valid rows**
   - Trim leading and trailing whitespace from every field.

4. **Deduplicate**
   - After normalization, drop duplicate data rows.
   - Two rows are duplicates if all fields are identical (case-sensitive).
   - Keep the first occurrence and discard later duplicates.

5. **Output format**
   - Write UTF-8 CSV without BOM.
   - Include the normalized header as the first row.
   - Use Unix line endings (`\n`).
   - Use a comma as the delimiter.
   - Do not surround fields with quotes unless the `csv` writer requires it for special characters.

## Constraints

- Use only the Python standard library (no third-party packages).
- Do not modify the input file.
- The output file must be created at the path given on the command line (create parent directories if needed).

## Success criteria

Given the provided `dirty_data.csv`, your tool must produce a deterministic cleaned file that satisfies all rules above.
