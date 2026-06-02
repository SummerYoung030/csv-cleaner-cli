#!/usr/bin/env bash
# Local smoke test without Docker (logic only). Official grading uses tests/test.sh.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
INPUT="${TASK_ROOT}/environment/dirty_data.csv"
OUTPUT_DIR="${TASK_ROOT}/.local_output"
OUTPUT="${OUTPUT_DIR}/clean.csv"

mkdir -p "${OUTPUT_DIR}"

echo "[test_local.sh] Running cleaner..."
python3 "${TASK_ROOT}/solution/cleaner.py" "${INPUT}" "${OUTPUT}"

echo "[test_local.sh] Running verifier..."
export BENCHMARK_INPUT="${INPUT}"
export BENCHMARK_OUTPUT="${OUTPUT}"
python3 "${TASK_ROOT}/tests/test_logic.py"

echo "[test_local.sh] All local checks passed"
