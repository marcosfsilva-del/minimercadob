
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .
RUN python -m compileall -q app scripts tasks.py


FROM python:3.12-slim


ARG COMMIT_SHA=local

WORKDIR /app
ENV PORT=3000 \
    DATABASE_URL=sqlite:///data/devops_market.db \
    COMMIT_SHA=${COMMIT_SHA} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


RUN useradd --create-home --shell /bin/bash appuser

COPY --from=builder /install /usr/local
COPY --chown=appuser:appuser . .

RUN mkdir -p data && chown -R appuser:appuser /app

USER appuser

EXPOSE 3000
CMD ["sh", "-c", "python tasks.py db-seed && python -m app.core.server"]