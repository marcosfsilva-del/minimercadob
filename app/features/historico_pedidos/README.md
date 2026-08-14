# Historico Pedidos

Feature do Módulo 24 - Histórico De Pedidos.

## Objetivo

Tornar o histórico de pedidos consultável: hoje a tela lista todos os pedidos em ordem
fixa, o que fica inviável conforme o número de pedidos cresce. A feature adiciona filtro
por nome do cliente e ordenação por data e por total.

## Requisitos do módulo

| Requisito | Issue | Entrega |
|---|---|---|
| 070 | #57 | Filtro por nome do cliente |
| 071 | #58 | Ordenação por data e por total |
| 072 | #59 | Testes de filtro e ordenação |

## Estado atual

Estrutura inicial gerada com `python3 tasks.py feature-create historico-pedidos` e
validada com `python3 tasks.py feature-check historico-pedidos`. A implementação dos
requisitos acontece nas próximas etapas, uma issue por vez.

## Como rodar

```bash
python3 tasks.py db-seed
python3 tasks.py dev
```

A página fica em `http://localhost:3000/historico-pedidos` e o endpoint de status em
`http://localhost:3000/historico-pedidos/api`.
