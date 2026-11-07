FROM python:3.15-slim AS builder

WORKDIR /app
COPY requirements-dev.txt requirements.txt ./
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .
RUN python -m compileall -q app scripts tasks.py
RUN mkdir -p data

FROM cgr.dev/chainguard/python:latest

WORKDIR /app
ENV PORT=3000
ENV DATABASE_URL=sqlite:///data/devops_market.db
ENV PYTHONPATH=/usr/local/lib/python3.15/site-packages

COPY --from=builder /install /usr/local
COPY --from=builder --chown=65532:65532 /app/data ./data
COPY --chown=65532:65532 . .

EXPOSE 3000
CMD ["python", "-c", "import subprocess,sys; subprocess.run([sys.executable, 'tasks.py', 'db-seed'], check=True); subprocess.run([sys.executable, '-m', 'app.core.server'], check=True)"]
