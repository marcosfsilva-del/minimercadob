FROM python:3.14-slim@sha256:af8a5aa14780025dbfbcfbc81bd8a91ebd87711dd5b0f48ed71090949dd7cb1d AS builder

WORKDIR /app
COPY requirements-dev.txt requirements.txt ./
RUN python -m pip install --upgrade pip && python -m pip install --prefix=/install -r requirements.txt

COPY . .
RUN python -m compileall -q app scripts tasks.py

FROM python:3.14-slim@sha256:af8a5aa14780025dbfbcfbc81bd8a91ebd87711dd5b0f48ed71090949dd7cb1d

WORKDIR /app
ENV PORT=3000
ENV DATABASE_URL=sqlite:///data/devops_market.db

COPY --from=builder /install /usr/local
COPY . .

RUN mkdir -p data

EXPOSE 3000
CMD ["sh", "-c", "python tasks.py db-seed && python -m app.core.server"]
