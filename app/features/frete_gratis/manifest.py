from app.core.types.features import FeatureManifest, SlotContribution


def free_shipping_summary(**context) -> str:
    total = context.get("total", 0)
    from app.features.frete_gratis.service import build_free_shipping_message

    return f"<div class='frete-gratis-summary'><p>{build_free_shipping_message(total)}</p></div>"


manifest = FeatureManifest(
    id="frete-gratis",
    name="Frete Gratis",
    blueprint=None,
    menu=None,
    slots=[SlotContribution(slot="CART_SUMMARY", renderer=free_shipping_summary)],
)
