"""Модуль 1 · Поиск. Допишите функции и запустите: pytest m01-search"""

from __future__ import annotations


def linear_search(items: list[int], target: int) -> int:
    """Задание 1. Верните индекс первого элемента, равного target, или -1."""
    # TODO: пройдите по списку и сравнивайте элементы
    raise NotImplementedError


def next_bounds(left: int, right: int, mid_value: int, target: int) -> tuple[int, int]:
    """Задание 2. Один шаг бинарного поиска: куда сдвинуть границы?

    mid = (left + right) // 2, mid_value — элемент в середине.
    Верните новые (left, right).
    """
    # TODO: найдите mid = (left + right) // 2 и решите, куда сдвинуть границы:
    # если mid_value меньше target — ищем справа, иначе слева
    raise NotImplementedError


def binary_search(items: list[int], target: int) -> int:
    """Задание 3. Бинарный поиск в ОТСОРТИРОВАННОМ списке. Верните индекс или -1."""
    # TODO: две границы, цикл while, середина, сдвиг границ
    raise NotImplementedError


def contains(items: list[int], target: int) -> bool:
    """Задание 4 («найди ошибку»). Функция должна говорить, есть ли target в списке.

    В коде спрятана ошибка — найдите и исправьте её.
    """
    left, right = 0, len(items) - 1
    while left < right:
        mid = (left + right) // 2
        if items[mid] == target:
            return True
        if items[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False
