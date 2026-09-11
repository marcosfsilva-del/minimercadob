# cpf no checkout

issues 44, 51 e 52: campo de cpf, validação de formato e testes.

o campo aparece no checkout pelo slot do projeto. aceita 11 números ou o formato 000.000.000-00 e salva só os números no cadastro do cliente. a validação é de formato, sem cálculo dos dígitos verificadores, conforme a issue 51.

o pedido e o cliente são salvos na mesma transação. se o cpf estiver errado ou faltar estoque, a compra não é concluída e o carrinho continua preenchido.

a feature usa um hook antes do envio do checkout e não altera os arquivos do core. o cpf fica no cliente; o modelo atual não tem vínculo entre cliente e pedido. pedidos feitos pela api continuam no fluxo original.

os testes usam banco temporário e conferem campo, formato, persistência, estoque e carrinho em caso de erro.

```sh
python -m pytest app/features/cpf_checkout/tests -v
```
