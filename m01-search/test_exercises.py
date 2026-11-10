"""Проверка модуля 1. Запуск: pytest m01-search"""

from __future__ import annotations

import math
from collections.abc import Callable
from types import ModuleType
from typing import Any

import pytest

SORTED = [1, 3, 5, 7, 9, 11]
CASES = [
    (SORTED, 5, 2),
    (SORTED, 1, 0),
    (SORTED, 11, 5),
    (SORTED, 4, -1),
    ([], 1, -1),
    ([7], 7, 0),
]
CASE_IDS = ["в середине", "первый", "последний", "нет в списке", "пустой", "один элемент"]


@pytest.mark.parametrize(("items", "value", "expected"), CASES, ids=CASE_IDS)
def test_linear_search(target: ModuleType, items: list[int], value: int, expected: int) -> None:
    assert target.linear_search(items, value) == expected


def test_linear_search_returns_first_of_duplicates(target: ModuleType) -> None:
    assert target.linear_search([2, 2, 2], 2) == 0, "нужен ИНДЕКС ПЕРВОГО совпадения"


@pytest.mark.parametrize(
    ("mid_value", "value", "expected"),
    [
        (5, 9, (3, 5)),  # середина меньше цели → ищем справа
        (9, 3, (0, 1)),  # середина больше цели → ищем слева
    ],
    ids=["вправо", "влево"],
)
def test_next_bounds(
    target: ModuleType, mid_value: int, value: int, expected: tuple[int, int]
) -> None:
    got = target.next_bounds(0, 5, mid_value, value)
    assert got == expected, "подсказка: если mid_value < target, то left = mid + 1"


@pytest.mark.parametrize(("items", "value", "expected"), CASES, ids=CASE_IDS)
def test_binary_search(target: ModuleType, items: list[int], value: int, expected: int) -> None:
    assert target.binary_search(items, value) == expected


def test_binary_search_is_fast(target: ModuleType, counting_list: Callable[[Any], Any]) -> None:
    """Бинарный поиск должен смотреть в список не больше log2(n) + 2 раз."""
    n = 1024
    data = counting_list(range(n))
    assert target.binary_search(data, n - 1) == n - 1
    limit = int(math.log2(n)) + 2
    assert data.accesses <= limit, (
        f"Слишком много обращений к списку: {data.accesses}, ожидалось ≤ {limit}. "
        "Подсказка: на каждом шаге отбрасываем половину."
    )


@pytest.mark.bugfix
def test_contains(target: ModuleType) -> None:
    """Задание «найди ошибку»: засчитывается, только когда верны ВСЕ случаи."""
    for (items, value, expected), name in zip(CASES, CASE_IDS, strict=True):
        assert target.contains(items, value) == (expected != -1), (
            f"Случай «{name}»: contains({items}, {value}) ошибается. "
            "Подсказка: проверьте, какие элементы остаются, когда left == right"
        )
