# Produto Esgotado

Sinaliza no catálogo quando um produto está com estoque zero (requisito 019).

## Comportamento

- Quando `product.stock <= 0`, o slot `PRODUCT_CARD` passa a exibir o selo
  "Esgotado" no card do produto.
- O botão "Adicionar ao carrinho" já é desabilitado pelo template base
  (`app/core/templates/catalog.html`) nesse mesmo caso.
- O produto permanece visível no catálogo normalmente.

## Sem rotas HTTP

Essa feature não tem tela própria: ela só contribui com um renderer para o
slot `PRODUCT_CARD`. Ver `manifest.py` e `service.py`.
