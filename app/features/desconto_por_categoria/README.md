# Desconto Por Categoria

Requisito 040 - Issue #22.

## Regra

- A categoria **Mercearia** recebe **10%** de desconto no preço de cada produto.
- Todas as outras categorias **não** recebem desconto (preço original).
- A comparação da categoria ignora maiúsculas/minúsculas e espaços nas pontas.

A categoria e o percentual ficam nas constantes `DISCOUNT_CATEGORY` e `DISCOUNT_PERCENT`
em `service.py`. Para mudar a regra, basta alterar essas duas constantes.

## Onde está cada parte

- `service.py`: regra de negócio (`has_discount`, `discounted_price`, `cart_discount`).
- `routes.py`: página `/desconto-por-categoria` e API `/desconto-por-categoria/api`.
- `templates/`: tela que lista os produtos com preço original e preço final.
- `tests/`: testes que provam os critérios de aceitação.

## Critérios de aceitação e testes

| Critério | Teste |
| --- | --- |
| Uma categoria definida recebe desconto | `test_categoria_definida_recebe_desconto` |
| Outras categorias não recebem desconto | `test_outras_categorias_nao_recebem_desconto` |
| Regra fica documentada na feature | este README |

## Requisito 042 - Testes De Desconto Por Categoria (Issue #29)

Arquivo: `tests/test_requisito_042_desconto_por_categoria.py`.

| Critério | Teste |
| --- | --- |
| Teste cobre categoria com desconto | `test_categoria_com_desconto` |
| Teste cobre categoria sem desconto | `test_categoria_sem_desconto` |
| Teste cobre total final | `test_total_final_com_desconto`, `test_total_final_sem_desconto`, `test_total_final_carrinho_vazio` |
