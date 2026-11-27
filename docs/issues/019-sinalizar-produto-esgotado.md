# requisito 019 - Sinalizar Produto Esgotado

## Objetivo

Exibir estado de produto esgotado no catálogo.

## Comportamento esperado

Quando o estoque de um produto chega a zero, o catálogo deve deixar isso
visível para o usuário: mostrar o texto "esgotado" e desabilitar o botão de
adicionar ao carrinho. O produto não deve sumir da listagem.

## Critérios de aceitação

- [ ] estoque zero mostra texto "esgotado";
- [ ] botão de adicionar fica desabilitado;
- [ ] produto continua visivel no catálogo.

## Area afetada

- [x] Frontend Flask/Jinja
- [ ] Backend Flask/API
- [ ] Banco
- [x] Testes
- [ ] Operação
