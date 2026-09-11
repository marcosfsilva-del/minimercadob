# Regra Leve 3 Pague 2

Promocao "leve 3, pague 2" do DevOps Market.

## Regra documentada

- **Categoria contemplada:** `Higiene` (constante `CATEGORIA_PROMOCIONAL` em `service.py`).
- **Produto do seed que participa hoje:** Sabonete (`Higiene`, R$ 2,49).
- A cada grupo de **3 unidades do mesmo produto** dessa categoria, **1 unidade sai de graca**.
- Quantidade **menor que 3 nao recebe desconto**.
- 6 unidades recebem o desconto **duas vezes**; 4 unidades recebem **uma vez** (sobra nao conta).
- Produtos de outras categorias nao entram na promocao.

Para mudar a categoria da promocao, basta alterar `CATEGORIA_PROMOCIONAL` em `service.py`.

## Onde a economia aparece

A feature nao altera `app/core/*`. Ela se liga ao carrinho e ao checkout pelos slots do registry:

| Slot | Renderer | O que mostra |
| --- | --- | --- |
| `CART_SUMMARY` | `resumo_economia` | valor economizado, total com desconto e detalhe por produto |
| `CHECKOUT_FORM` | `resumo_economia` | mesmo resumo na tela de checkout |
| `CART_ITEM` | `selo_item` | selo com as unidades gratis daquele item |

Os dois renderers devolvem string vazia quando a regra nao se aplica, entao a
mensagem so aparece quando existe desconto real.

## Rotas

| Rota | Descricao |
| --- | --- |
| `GET /regra-leve3-pague2` | pagina que documenta a regra na interface |
| `GET /regra-leve3-pague2/api` | JSON com `regra`, `categoria` e `status` |

## Funcoes principais (`service.py`)

| Funcao | Papel |
| --- | --- |
| `produto_elegivel(produto)` | diz se o produto participa da promocao |
| `grupos_promocionais(qtd)` | quantos grupos completos de 3 existem |
| `unidades_gratuitas(qtd)` | 1 unidade gratis por grupo completo |
| `desconto_do_item(preco, qtd)` | valor economizado no item |
| `calcular_promocao(itens)` | total sem desconto, economia, total final e itens afetados |

## Issues

- #41 - requisito 046 - Regra Leve 3 Pague 2
- #48 - requisito 047 - Exibir Economia Da Promocao
