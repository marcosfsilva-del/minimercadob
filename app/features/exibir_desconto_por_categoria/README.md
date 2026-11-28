# Exibir Desconto Por Categoria

Requisito 041 - Issue #27. Depende da regra do requisito 040 (Issue #22).

## O que faz

Mostra no resumo do carrinho (`/cart`) o desconto da categoria definida na regra
(`app/features/desconto_por_categoria`, hoje **Mercearia** com **10%**):

- com desconto: exibe subtotal, linha de desconto e total final;
- sem desconto: exibe só o total final, sem linha de desconto.

A feature entra no carrinho pelo slot `CART_SUMMARY`, sem alterar o core.

## Onde está cada parte

- `service.py`: `cart_summary` calcula subtotal, desconto e total final.
- `routes.py`: `render_cart_summary`, renderer usado pelo slot.
- `manifest.py`: registra o renderer no slot `CART_SUMMARY`.
- `templates/`: bloco HTML do resumo.
- `tests/`: testes dos critérios de aceitação.

## Critérios de aceitação e testes

| Critério | Teste |
| --- | --- |
| Resumo exibe valor do desconto | `test_resumo_exibe_valor_do_desconto_e_total_final` |
| Resumo exibe total final | `test_resumo_calcula_desconto_e_total_final` |
| Layout claro com ou sem desconto | `test_resumo_sem_desconto_nao_exibe_linha_de_desconto` |
