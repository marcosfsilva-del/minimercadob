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
