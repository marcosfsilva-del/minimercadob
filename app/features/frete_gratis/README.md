# Frete Grátis

## Regra de negócio

O frete grátis do MiniMercado é concedido para compras a partir de R$ 19,99.

- Se o subtotal for inferior a R$ 19,99, o sistema informa quanto falta para atingir o mínimo.
- Se o subtotal for igual ou superior a R$ 19,99, o sistema informa que o cliente ganhou frete grátis.
- O cálculo do restante usa valores monetários com centavos, então o arredondamento deve respeitar corretamente os centavos.

## Exemplos

- Compra de R$ 12,00 → "Faltam R$ 7,99 para ganhar frete grátis!"
- Compra de R$ 19,98 → "Faltam R$ 0,01 para ganhar frete grátis!"
- Compra de R$ 19,99 → "Parabéns! Você ganhou frete grátis!"
- Compra de R$ 25,00 → "Parabéns! Você ganhou frete grátis!"

## Integração

A mensagem aparece no resumo do carrinho por meio do slot `CART_SUMMARY` da arquitetura de features do MiniMercado.
