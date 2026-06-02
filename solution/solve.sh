#!/usr/bin/env bash
set -euo pipefail

python3 /workspace/solution/cleaner.py \
  /workspace/data/dirty_data.csv \
  /workspace/output/clean.csv
