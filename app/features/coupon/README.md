# Cupom

Campo de cupom de desconto no resumo do carrinho.

- `service.py`: `find_coupon` procura o código em `COUPONS`.
- `routes.py`: `POST /coupon/apply` recebe o código do formulário.
- `manifest.py`: registra o formulário no slot `CART_SUMMARY`.

Cupom desconhecido exibe a mensagem "Cupom não encontrado. Confira o código e tente novamente."
