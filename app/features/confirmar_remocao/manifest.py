"""Registro da feature no core.

O core varre app/features/, importa este arquivo e le o objeto `manifest`.
E assim que a feature passa a existir para a aplicacao, sem que nenhuma
linha de app/core/* precise ser alterada.
"""

from markupsafe import escape

from app.core.types.features import FeatureManifest, SlotContribution
from app.features.confirmar_remocao.routes import bp


def botao_remover_com_confirmacao(**context) -> str:
    """Conteudo injetado no slot CART_ITEM, dentro de cada item do carrinho.

    O core ja oferece este ponto de extensao no cart.html:

        {% for slot in slot_renderers("CART_ITEM") %}
          {{ slot.renderer(item=item)|safe }}
        {% endfor %}

    Por isso conseguimos acrescentar o link de remocao com confirmacao sem
    editar o template do core.
    """
    item = context.get("item")
    if not item:
        return ""

    product_id = item["product"].id
    # escape() protege contra HTML malicioso vindo do nome do produto.
    nome = escape(item["product"].name)

    return (
        f'<p class="muted">'
        f'<a href="/confirmar-remocao/{product_id}" '
        f'data-testid="link-confirmar-remocao">'
        f"Remover {nome} (com confirmação)"
        f"</a></p>"
    )


manifest = FeatureManifest(
    id="confirmar-remocao",
    name="Confirmar Remocao",
    blueprint=bp,
    # Sem item de menu: a feature nao tem pagina propria de entrada,
    # ela e acionada a partir do carrinho.
    menu=None,
    slots=[
        SlotContribution(
            slot="CART_ITEM",
            renderer=botao_remover_com_confirmacao,
        )
    ],
)