from decimal import ROUND_HALF_UP, Decimal
from typing import Any

FREE_SHIPPING_THRESHOLD = 19.99


def _to_decimal(value: float | Decimal) -> Decimal:  # type: ignore[operator]  # noqa: UP007
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def get_free_shipping_status(subtotal: float | Decimal) -> dict[str, Any]:  # type: ignore[operator]  # noqa: UP007
    subtotal_decimal = _to_decimal(subtotal)
    threshold_decimal = _to_decimal(FREE_SHIPPING_THRESHOLD)

    if subtotal_decimal >= threshold_decimal:
        return {"is_free_shipping": True, "remaining": 0.0}

    remaining = (threshold_decimal - subtotal_decimal).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    return {"is_free_shipping": False, "remaining": float(remaining)}


def _format_currency(value: Decimal | float) -> str:  # type: ignore[operator]  # noqa: UP007
    number = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{number:.2f}".replace(".", ",")


def build_free_shipping_message(subtotal: float | Decimal) -> str:  # type: ignore[operator]  # noqa: UP007
    status = get_free_shipping_status(subtotal)
    if status["is_free_shipping"]:
        return "Parabéns! Você ganhou frete grátis!"

    remaining = status["remaining"]
    return f"Faltam R$ {_format_currency(remaining)} para ganhar frete grátis!"
