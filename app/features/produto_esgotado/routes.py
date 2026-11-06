"""A feature "produto-esgotado" não expõe rotas HTTP.

Ela apenas contribui para o slot PRODUCT_CARD do catálogo (ver manifest.py),
exibindo o texto "Esgotado" quando o estoque do produto é zero. O botão de
"Adicionar ao carrinho" já é desabilitado pelo template base do catálogo
(app/core/templates/catalog.html) quando product.stock <= 0.
"""
