COUPONS: dict[str, float] = {}


def find_coupon(code: str | None) -> float | None:
    return COUPONS.get((code or "").strip().upper())
