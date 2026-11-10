"""Проверка модуля 4. Запуск: pytest m04-quicksort"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from types import ModuleType

import pytest

SORT_CASES = [
    [64, 34, 25, 12, 22, 11, 90, 55, 0, 9],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
    [9, 5, 8, 3, 7, 6, 5, 4, 3, 8, 2, 1, 0],
    [],
    [55],
    [2, 2, 2, 2],
]
SORT_IDS = [
    "случайный",
    "уже отсортирован",
    "в обратном порядке",
    "дубликаты",
    "пустой",
    "один элемент",
    "все равны",
]


@pytest.mark.parametrize(
    ("n", "expected"),
    [(0, 0), (1, 1), (2, 1), (5, 5), (10, 55)],
    ids=["F(0)", "F(1)", "F(2)", "F(5)", "F(10)"],
)
def test_fibonacci(target: ModuleType, n: int, expected: int) -> None:
    assert target.fibonacci(n) == expected


@pytest.mark.parametrize(
    ("n", "expected"),
    [(0, 1), (1, 1), (2, 3), (3, 5), (4, 9), (5, 15)],
    ids=["n=0", "n=1", "n=2", "n=3", "n=4", "n=5"],
)
def test_count_fib_calls(target: ModuleType, n: int, expected: int) -> None:
    assert target.count_fib_calls(n) == expected, (
        "Подсказка: вызовов = 1 (этот) + вызовы для n-1 + вызовы для n-2"
    )


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5], 9),
        ([7], 7),
        ([1, 2], 2),
        ([2, 1], 2),
        ([-5, -1, -9], -1),
        ([4, 4, 4], 4),
    ],
    ids=[
        "из примера",
        "один элемент",
        "два по возрастанию",
        "два по убыванию",
        "отрицательные",
        "равные",
    ],
)
def test_find_max_rec(target: ModuleType, items: list[int], expected: int) -> None:
    assert target.find_max_rec(items) == expected


def test_find_max_rec_empty_raises(target: ModuleType) -> None:
    with pytest.raises(ValueError):
        target.find_max_rec([])


@pytest.mark.parametrize(
    ("items", "low", "high"),
    [
        ([3, 8, 2, 5, 1, 4, 7, 6], 0, 7),
        ([1, 2, 3, 4, 5], 0, 4),
        ([5, 4, 3, 2, 1], 0, 4),
        ([2, 2, 2], 0, 2),
        ([9, 3, 8, 1, 5, 0], 1, 4),
        ([7], 0, 0),
    ],
    ids=["случайный", "по возрастанию", "по убыванию", "равные", "часть списка", "один элемент"],
)
def test_partition(target: ModuleType, items: list[int], low: int, high: int) -> None:
    data = items.copy()
    pivot = data[high]
    p = target.partition(data, low, high)
    assert low <= p <= high, f"Индекс опорного {p} вне границ [{low}, {high}]"
    assert data[p] == pivot, "Опорный элемент должен оказаться на возвращённом индексе"
    assert all(x <= pivot for x in data[low:p]), (
        "Слева от опорного должны быть элементы <= опорного"
    )
    assert all(x > pivot for x in data[p + 1 : high + 1]), "Справа должны быть элементы > опорного"
    assert Counter(data) == Counter(items), "Разбиение не должно терять или добавлять элементы"
    assert data[:low] == items[:low] and data[high + 1 :] == items[high + 1 :], (
        "Элементы вне границ [low, high] менять нельзя"
    )


@pytest.mark.parametrize("items", SORT_CASES, ids=SORT_IDS)
def test_quicksort(target: ModuleType, items: list[int]) -> None:
    assert target.quicksort(items) == sorted(items)


def test_quicksort_does_not_change_input(target: ModuleType) -> None:
    original = [3, 1, 2]
    data = original.copy()
    target.quicksort(data)
    assert data == original, "Исходный список менять нельзя: сначала сделайте копию"


@pytest.mark.bugfix
def test_quicksort_lists(target: ModuleType) -> None:
    """Задание «найди ошибку»: засчитывается, только когда верны ВСЕ случаи."""
    func: Callable[[list[int]], list[int]] = target.quicksort_lists
    for items, name in zip(SORT_CASES, SORT_IDS, strict=True):
        assert func(items) == sorted(items), (
            f"Случай «{name}»: quicksort_lists({items}) вернула {func(items)}. "
            "Подсказка: сравните длину результата с длиной входа"
        )
