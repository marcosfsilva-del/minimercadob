from app.features.product_search.service import matches_query, status


def test_status():
    assert status() == {"feature": "product-search", "status": "ok"}


def test_matches_product_name_case_insensitively():
    assert matches_query("Arroz Integral", "Pacote de um quilo", "ARROZ")


def test_matches_product_description_case_insensitively():
    assert matches_query("Cafe", "Torra MEDIA e sabor suave", "media")


def test_empty_query_matches_all_products():
    assert matches_query("Qualquer produto", "Qualquer descricao", "   ")


def test_non_matching_query_is_rejected():
    assert not matches_query("Arroz Integral", "Pacote de um quilo", "detergente")
