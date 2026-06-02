FROM python:3.11.9-slim-bookworm

WORKDIR /workspace

RUN useradd --create-home --shell /bin/bash appuser

COPY environment/dirty_data.csv /workspace/data/dirty_data.csv
COPY solution/ /workspace/solution/
COPY tests/test_logic.py /workspace/tests/test_logic.py
COPY tests/run_in_container.sh /workspace/tests/run_in_container.sh

RUN chmod +x /workspace/solution/solve.sh /workspace/tests/run_in_container.sh \
    && chown -R appuser:appuser /workspace

USER appuser

ENTRYPOINT ["/workspace/tests/run_in_container.sh"]
