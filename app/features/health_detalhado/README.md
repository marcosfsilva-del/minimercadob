# Health Detalhado

Endpoint de health detalhado da aplicacao, usado para monitoramento.

## Rota

`GET /api/health/detailed`

## Requisito 100 - Endpoint De Health Detalhado

Resposta inclui:

- `status`: status atual da aplicacao;
- `version`: versao da aplicacao em execucao;
- `timestamp`: horario (UTC) em que a verificacao foi realizada.

## Requisito 101 - Health Do Banco

O endpoint tambem verifica a conexao com o banco SQLite:

- `database.status`: `"ok"` quando a conexao responde, `"falha"` caso contrario;
- quando o banco falha, `status` geral tambem vira `"falha"` e a resposta HTTP
  passa a ser `503` em vez de `200`.

## Requisito 102 - Testes De Health Avancado

Testes em `tests/test_health_detalhado.py` cobrem:

- status `"ok"` quando aplicacao e banco estao saudaveis;
- informacoes de versao (e horario) presentes na resposta;
- verificacao de banco nos cenarios de sucesso e de falha (com o respectivo
  status HTTP `503`).
