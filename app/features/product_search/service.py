def status() -> dict[str, str]:
    return {"feature": "product-search", "status": "ok"}


def matches_query(name: str, description: str, query: str) -> bool:
    normalized_query = query.strip().casefold()
    if not normalized_query:
        return True
    return normalized_query in name.casefold() or normalized_query in description.casefold()
