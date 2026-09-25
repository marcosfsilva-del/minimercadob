# Compra Finalizada

Tela de sucesso exibida depois que o usuário finaliza a compra.

## O que a feature entrega

- redireciona o usuário para uma tela própria ao concluir o checkout;
- mostra o código público do pedido;
- mostra o total da compra, os itens e o cliente informado;
- oferece ações para voltar ao catálogo e ver o histórico de pedidos.

## Rota

`GET /compra-finalizada/<codigo-publico>`

O código vem da coluna `public_code` do pedido. Código inexistente devolve `404`
com mensagem amigável, então a URL pode ser aberta de novo ou compartilhada sem quebrar.

## Como o redirecionamento acontece sem tocar em `app/core`

`app/core/routes/web.py` termina o checkout com `redirect(url_for("web.orders"))` e não
expõe slot nem hook para esse momento. Como o core é protegido, a feature usa os hooks de
aplicação do próprio blueprint:

1. `before_app_request` guarda o id do último pedido existente antes do checkout;
2. `after_app_request` identifica o pedido criado depois desse id e troca apenas o
   cabeçalho `Location` da resposta do core.

Os hooks só agem quando `request.endpoint == "web.finish_checkout"` e a resposta é um
redirect; qualquer outra requisição passa intacta. A resposta original é preservada, então
o cookie de sessão, o carrinho limpo e a mensagem flash do core continuam funcionando.

Limitação conhecida: o pedido é identificado por "o mais recente criado depois do id
guardado". Em dois checkouts simultâneos no mesmo instante isso poderia apontar para o
pedido errado. Resolver de vez exige o core devolver o pedido criado.
