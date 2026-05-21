FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --upgrade pip build \
    && python -m build --wheel


FROM python:3.11-slim AS runtime

WORKDIR /app

COPY --from=builder /app/dist/ /tmp/dist/

RUN pip install --no-cache-dir /tmp/dist/*.whl \
    && rm -rf /tmp/dist

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
