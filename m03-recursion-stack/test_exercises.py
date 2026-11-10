"""Проверка модуля 3. Запуск: pytest m03-recursion-stack"""

from __future__ import annotations

from types import ModuleType

import pytest

SORTED = [2, 5, 8, 12, 16, 23, 38, 56, 72, 92]


@pytest.mark.parametrize(
    ("n", "expected"),
    [(0, 1), (1, 1), (5, 120), (7, 5040), (10, 3628800)],
    ids=["ноль", "единица", "пять", "семь", "десять"],
)
def test_factorial(target: ModuleType, n: int, expected: int) -> None:
    assert target.factorial(n) == expected


def test_factorial_negative_raises(target: ModuleType) -> None:
    with pytest.raises(ValueError):
        target.factorial(-1)


@pytest.mark.parametrize(
    ("items", "expected"),
    [([1, 2, 3, 4, 5], 15), ([10, -2, 3], 11), ([], 0), ([42], 42)],
    ids=["пять чисел", "с отрицательным", "пустой", "один элемент"],
)
def test_recursive_sum(target: ModuleType, items: list[int], expected: int) -> None:
    assert target.recursive_sum(items) == expected


def test_recursive_sum_does_not_change_input(target: ModuleType) -> None:
    data = [1, 2, 3]
    target.recursive_sum(data)
    assert data == [1, 2, 3]


@pytest.mark.parametrize(
    ("value", "expected"),
    [(23, 5), (2, 0), (92, 9), (100, -1), (1, -1), (40, -1)],
    ids=["в середине", "первый", "последний", "больше всех", "меньше всех", "между"],
)
def test_binary_search_rec(target: ModuleType, value: int, expected: int) -> None:
    assert target.binary_search_rec(SORTED, value) == expected


def test_binary_search_rec_empty(target: ModuleType) -> None:
    assert target.binary_search_rec([], 5) == -1


def test_binary_search_rec_with_explicit_left(target: ModuleType) -> None:
    """Если задан только left, right всё равно должен стать последним индексом."""
    assert target.binary_search_rec(SORTED, 92, 0) == 9


def test_stack_is_empty_at_start(target: ModuleType) -> None:
    stack = target.Stack()
    assert stack.is_empty() is True
    assert len(stack) == 0


def test_stack_push_changes_size(target: ModuleType) -> None:
    stack = target.Stack()
    stack.push(10)
    stack.push(20)
    assert len(stack) == 2
    assert stack.is_empty() is False


def test_stack_pops_in_reverse_order(target: ModuleType) -> None:
    """LIFO: последним пришёл — первым ушёл."""
    stack = target.Stack()
    for item in [10, 20, 30]:
        stack.push(item)
    assert [stack.pop(), stack.pop(), stack.pop()] == [30, 20, 10]
    assert stack.is_empty()


def test_stack_peek_does_not_remove(target: ModuleType) -> None:
    stack = target.Stack()
    stack.push(1)
    stack.push(2)
    assert stack.peek() == 2
    assert len(stack) == 2


def test_stack_pop_empty_raises(target: ModuleType) -> None:
    with pytest.raises(IndexError):
        target.Stack().pop()


def test_stack_peek_empty_raises(target: ModuleType) -> None:
    """Посмотреть верхний элемент пустого стека нельзя: нужно IndexError."""
    with pytest.raises(IndexError):
        target.Stack().peek()


@pytest.mark.bugfix
def test_power(target: ModuleType) -> None:
    """Задание «найди ошибку»: засчитывается, только когда верны ВСЕ случаи."""
    cases = [(2, 0, 1), (2, 3, 8), (5, 1, 5), (3, 4, 81), (0, 0, 1), (7, 0, 1)]
    for base, exp, expected in cases:
        try:
            got = target.power(base, exp)
        except RecursionError:
            pytest.fail(
                f"power({base}, {exp}) ушла в бесконечную рекурсию. "
                "Подсказка: у какого значения exp рекурсия не останавливается?"
            )
        assert got == expected, f"power({base}, {exp}) = {got}, ожидалось {expected}"
