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

Os três requisitos estão implementados, sem alterar nada em `app/core/`.

- **070, filtro.** Campo "Cliente" na página. Busca por parte do nome, sem diferenciar
  maiúsculas e minúsculas. Termo vazio mostra todos os pedidos.
- **071, ordenação.** Mais recentes, mais antigos, maior total e menor total. O filtro é
  aplicado antes da ordenação, então os dois funcionam juntos.
- **072, testes.** `tests/test_historico_pedidos.py`, cobrindo filtro, ordenação por data,
  ordenação por total, filtro e ordenação combinados, consulta no banco, página e API.

A regra fica em `service.py`, em funções que recebem e devolvem listas de pedidos. A consulta
ao banco reutiliza `list_orders`, do core.

## Parâmetros

| Parâmetro | Valores | Padrão |
|---|---|---|
| `cliente` | qualquer texto | vazio, mostra todos |
| `ordem` | `data_desc`, `data_asc`, `total_desc`, `total_asc` | `data_desc` |

Valem para a página e para o endpoint `/historico-pedidos/api`.

## Como rodar

```bash
python3 tasks.py db-seed
python3 tasks.py dev
```

A página fica em `http://localhost:3000/historico-pedidos` e a API em
`http://localhost:3000/historico-pedidos/api?cliente=ana&ordem=total_desc`.
