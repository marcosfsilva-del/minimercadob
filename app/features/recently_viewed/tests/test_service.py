import pytest

from app.features.recently_viewed.service import (
    MAX_RECENTLY_VIEWED,
    register_recently_viewed,
)


def test_registers_first_product():
    result = register_recently_viewed([], product_id=1)
    assert result == [1]


def test_new_product_goes_to_front():
    result = register_recently_viewed([2, 3], product_id=1)
    assert result == [1, 2, 3]


def test_revisiting_product_moves_it_to_front_without_duplicating():
    result = register_recently_viewed([3, 2, 1], product_id=1)
    assert result == [1, 3, 2]
    assert result.count(1) == 1


def test_order_is_most_recent_first():
    history: list[int] = []
    for product_id in [1, 2, 3]:
        history = register_recently_viewed(history, product_id)
    assert history == [3, 2, 1]


def test_respects_custom_limit():
    history: list[int] = []
    for product_id in range(1, 6):
        history = register_recently_viewed(history, product_id, limit=3)
    assert history == [5, 4, 3]
    assert len(history) == 3


def test_default_limit_is_ten():
    history: list[int] = []
    for product_id in range(1, 16):
        history = register_recently_viewed(history, product_id)
    assert len(history) == MAX_RECENTLY_VIEWED
    assert history == list(range(15, 5, -1))


def test_revisiting_within_limit_keeps_list_size_stable():
    history: list[int] = []
    for product_id in range(1, 11):
        history = register_recently_viewed(history, product_id)

    history = register_recently_viewed(history, product_id=5)

    assert len(history) == 10
    assert history[0] == 5
    assert history.count(5) == 1


def test_invalid_limit_raises():
    with pytest.raises(ValueError):
        register_recently_viewed([], product_id=1, limit=0)


def test_does_not_mutate_input_list():
    original = [1, 2, 3]
    register_recently_viewed(original, product_id=4)
    assert original == [1, 2, 3]