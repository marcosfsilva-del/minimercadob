# DevOps Market Python

Mini mercado web para a disciplina de Integração DevOps, feito em Python para facilitar execução em laboratório.

O frontend usa Flask + Jinja. O backend usa Flask API. O banco é SQLite com SQLAlchemy.

## Primeira execução

```bash
python -m pip install -r requirements-dev.txt
python tasks.py db-seed
python tasks.py dev
```

Acesse `http://localhost:3000`.

## Comandos base para CI dos alunos

```bash
python -m pip install -r requirements-dev.txt
python tasks.py lint
python tasks.py test
python tasks.py build
python tasks.py docker-build
python tasks.py smoke
```

O comando `build` em Python faz uma construção/validação com `compileall`, garantindo que o código importa e compila para bytecode. O Dockerfile também tem um stage `builder`.

## Docker

```bash
docker compose up --build
```

Para preview em outra porta:

```bash
PORT=3101 docker compose up --build
```

## Features

```bash
python tasks.py feature-create product-search
python tasks.py feature-check product-search
```

Cada feature fica em um pacote Python. Slugs com hífen viram pasta com underscore.

```text
app/features/product_search/
  manifest.py
  routes.py
  service.py
  templates/
  tests/
  README.md
```

## Core protegido

Não altere `app/core/*` para implementar uma feature comum. O aluno deve trabalhar em `app/features/<slug>`.

## CI

Este esqueleto não entrega workflow pronto. Cada aluno cria sua própria pipeline na branch, em `.github/workflows/<nome-do-aluno-ou-feature>.yml`, usando os comandos base acima.
