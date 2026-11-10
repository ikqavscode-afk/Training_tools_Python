"""Проверка модуля 2. Запуск: pytest m02-simple-sorts"""

from __future__ import annotations

from collections.abc import Callable
from types import ModuleType
from typing import Any

import pytest

CASES = [
    [64, 34, 25, 12, 22, 11, 90],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [3, 1, 2, 3, 1, 2],
    [-5, 10, 0, -1],
    [],
    [42],
    [2, 1],
]
CASE_IDS = [
    "случайный",
    "уже отсортирован",
    "в обратном порядке",
    "дубликаты",
    "отрицательные",
    "пустой",
    "один элемент",
    "два элемента",
]
SORT_NAMES = ["bubble_sort", "selection_sort", "insertion_sort"]


@pytest.mark.parametrize("name", SORT_NAMES)
@pytest.mark.parametrize("items", CASES, ids=CASE_IDS)
def test_sorts_correctly(target: ModuleType, name: str, items: list[int]) -> None:
    func: Callable[[list[int]], list[int]] = getattr(target, name)
    assert func(items) == sorted(items), f"{name}({items}) вернула не отсортированный список"


@pytest.mark.parametrize("name", SORT_NAMES)
def test_does_not_change_input(target: ModuleType, name: str) -> None:
    func: Callable[[list[int]], list[int]] = getattr(target, name)
    original = [3, 1, 2]
    data = original.copy()
    func(data)
    assert data == original, (
        "Исходный список менять нельзя: сначала сделайте копию (`items.copy()`)"
    )


@pytest.mark.parametrize(
    ("items", "start", "expected"),
    [
        ([5, 3, 8, 1], 0, 3),
        ([5, 3, 8, 1], 1, 3),
        ([5, 3, 8, 1], 3, 3),
        ([4, 1, 1], 0, 1),
        ([2, 9, 7], 0, 0),
    ],
    ids=["в конце", "со второго", "один элемент", "первый из равных", "в начале"],
)
def test_find_min_index(target: ModuleType, items: list[int], start: int, expected: int) -> None:
    assert target.find_min_index(items, start) == expected


class Tracked(int):
    """Число, которое считает, сколько раз его сравнили."""

    comparisons = 0

    def __gt__(self, other: Any) -> bool:
        Tracked.comparisons += 1
        return int(self) > int(other)

    def __lt__(self, other: Any) -> bool:
        Tracked.comparisons += 1
        return int(self) < int(other)


def test_bubble_sort_stops_early_on_sorted_list(target: ModuleType) -> None:
    """На отсортированном списке пузырёк делает один проход: n - 1 сравнений."""
    n = 100
    Tracked.comparisons = 0
    target.bubble_sort([Tracked(i) for i in range(n)])
    assert Tracked.comparisons <= n - 1, (
        f"Сравнений: {Tracked.comparisons}, ожидалось ≤ {n - 1}. "
        "Подсказка: если за проход не было обменов, список уже отсортирован."
    )


@pytest.mark.bugfix
def test_sort_cards(target: ModuleType) -> None:
    """Задание «найди ошибку»: засчитывается, только когда верны ВСЕ случаи."""
    for items, name in zip(CASES, CASE_IDS, strict=True):
        assert target.sort_cards(items) == sorted(items), (
            f"Случай «{name}»: sort_cards({items}) ошибается. "
            "Подсказка: какой элемент никогда не сравнивается с ключом?"
        )
