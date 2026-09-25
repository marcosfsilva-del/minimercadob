# Feature `Registrar Produtos Vistos`

Registra os produtos que o usuário acessou recentemente e mantém uma lista
ordenada do mais recente para o mais antigo, sem duplicidade, limitada a 10
itens.

- `manifest.py` registra o blueprint e contribui um link "Ver detalhes" no
  slot `PRODUCT_CARD` do catálogo.
- `routes.py` expõe `GET /produtos/<id>`, que registra o acesso na sessão e
  renderiza a página de detalhes.
- `service.py` concentra a regra de negócio: a lógica pura de
  ordenação/dedupe/limite (`register_recently_viewed`) e as consultas ao
  `Product` usadas pela rota.
- `tests/` guarda os testes da feature.

A lista fica em `session["recently_viewed"]` (lista de ids de produto), sem
persistência em banco.