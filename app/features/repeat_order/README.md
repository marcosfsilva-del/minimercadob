# \# Repetir Compra

# 

# Issue #104 - REQUISITO 73.

# 

# Permite repetir um pedido anterior: os itens do pedido voltam ao carrinho

# com as mesmas quantidades, desde que haja estoque.

# 

# \## Onde aparece

# 

# \- Botão "Repetir compra" em cada pedido da página Pedidos (slot ORDER\_SUMMARY).

# \- Página própria em /repeat-order, acessível pelo menu.

# 

# \## Regras

# 

# \- Itens sem estoque suficiente são ignorados. O tratamento completo da falta

# &#x20; de estoque é escopo da Issue #105.

# \- Se o produto já estiver no carrinho, as quantidades são somadas.

# 

# \## Testes

# 

# \- test\_repeat\_order.py: itens e quantidades preservados; itens entram no carrinho.

# \- test\_botao\_repetir.py: cada pedido exibe o botão "Repetir compra".

