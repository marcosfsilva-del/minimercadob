COUPONS: dict[str, float] = {"DEVOPS10": 0.10}


def find_coupon(code: str | None) -> float | None:
    return COUPONS.get((code or "").strip().upper())


def apply_coupon(total: float, code: str | None) -> dict[str, float]:
    rate = find_coupon(code) or 0.0
    discount = round(total * rate, 2)
    return {"discount": discount, "total": round(total - discount, 2)}
