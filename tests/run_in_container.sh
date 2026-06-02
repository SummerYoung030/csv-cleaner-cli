#!/usr/bin/env bash
set -euo pipefail

mkdir -p /workspace/output

/workspace/solution/solve.sh

python3 /workspace/tests/test_logic.py
