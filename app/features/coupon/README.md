# Cupom

Campo de cupom de desconto no resumo do carrinho.

- `service.py`: `find_coupon` procura o código em `COUPONS` e `apply_coupon` calcula desconto e total final.
- `routes.py`: `POST /coupon/apply` recebe o código do formulário e guarda o cupom válido na sessão.
- `manifest.py`: registra o formulário, o desconto e o total final no slot `CART_SUMMARY`.

Cupom disponível: `DEVOPS10`, com 10% de desconto sobre o total do carrinho.

Cupom desconhecido exibe a mensagem "Cupom não encontrado. Confira o código e tente novamente." e não altera o total.
