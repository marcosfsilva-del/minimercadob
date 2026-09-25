from flask import url_for

from app.core.types.features import FeatureManifest, MenuItem, SlotContribution
from app.features.repeat_order.routes import bp


def repeat_button(order, **_context) -> str:
    action = url_for("repeat_order.repeat", order_id=order.id)
    return (
        f'<form method="post" action="{action}">'
        '<button type="submit">Repetir compra</button>'
        "</form>"
    )


manifest = FeatureManifest(
    id="repeat-order",
    name="Repeat Order",
    blueprint=bp,
    menu=MenuItem(label="Repetir compra", endpoint="repeat_order.page", order=50),
    slots=[SlotContribution(slot="ORDER_SUMMARY", renderer=repeat_button)],
)
