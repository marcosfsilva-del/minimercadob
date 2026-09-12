# Health Detalhado

Endpoint de health detalhado da aplicacao, usado para monitoramento.

## Rota

`GET /api/health/detailed`

## Requisito 100 - Endpoint De Health Detalhado

Resposta inclui:

- `status`: status atual da aplicacao;
- `version`: versao da aplicacao em execucao;
- `timestamp`: horario (UTC) em que a verificacao foi realizada.
