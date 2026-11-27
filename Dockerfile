FROM python:3.12-alpine AS builder

WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .
RUN python -m compileall -q app scripts tasks.py


FROM python:3.12-alpine

# Atualiza o krb5-libs (1.22.2-r1 -> 1.22.3-r0+) e demais pacotes base para zerar as 16 CVEs
RUN apk update && apk upgrade --no-cache

# Cria usuário sem privilégios de root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app
ENV PORT=3000 \
    DATABASE_URL=sqlite:///data/devops_market.db \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder /install /usr/local
COPY --from=builder --chown=appuser:appgroup /app /app

RUN mkdir -p /app/data && chown -R appuser:appgroup /app/data

USER appuser

EXPOSE 3000
CMD ["sh", "-c", "python tasks.py db-seed && python -m app.core.server"]
