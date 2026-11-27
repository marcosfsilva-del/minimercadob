FROM python:3.12-alpine AS builder

WORKDIR /app
COPY requirements-dev.txt requirements.txt ./
RUN python -m pip install --upgrade pip && python -m pip install --prefix=/install -r requirements.txt

COPY . .
RUN python -m compileall -q app scripts tasks.py

# Base Alpine com pacotes atualizados: a base slim (Debian) trazia 54 CVEs HIGH,
# quase todas sem correcao, e o Trivy (security gate) reprovava a imagem.
FROM python:3.12-alpine

WORKDIR /app
# Commit que gerou a imagem, exposto em /api/health para provar qual versao esta no ar.
ARG COMMIT_SHA=local
ENV COMMIT_SHA=$COMMIT_SHA
ENV PORT=3000
ENV DATABASE_URL=sqlite:///data/devops_market.db

COPY --from=builder /install /usr/local
COPY . .

RUN apk upgrade --no-cache && mkdir -p data

EXPOSE 3000
CMD ["sh", "-c", "python tasks.py db-seed && python -m app.core.server"]
