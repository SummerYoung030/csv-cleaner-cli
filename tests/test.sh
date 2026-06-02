#!/usr/bin/env bash
# Host-side orchestration only: build image, run container, rely on in-container checks.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
IMAGE_NAME="csv-cleaner-cli:bench"

cd "${TASK_ROOT}"

echo "[test.sh] Building Docker image..."
if ! docker build -f environment/Dockerfile -t "${IMAGE_NAME}" .; then
  echo "[test.sh] docker build failed" >&2
  exit 1
fi

echo "[test.sh] Running cleaner and verifier inside container..."
if ! docker run --rm "${IMAGE_NAME}"; then
  echo "[test.sh] docker run failed" >&2
  exit 1
fi

echo "[test.sh] All checks passed"
exit 0
