"""Модуль 3 · Рекурсия и стек. Эталонные решения (спойлеры!)."""

from __future__ import annotations

from typing import Any


def factorial(n: int) -> int:
    """Факториал рекурсивно. Для n < 0 — ValueError."""
    if n < 0:
        raise ValueError("Факториал определён только для неотрицательных чисел")
    if n <= 1:  # базовый случай
        return 1
    return n * factorial(n - 1)  # рекурсивный случай


def recursive_sum(items: list[int]) -> int:
    """Сумма списка рекурсивно."""
    if not items:  # базовый случай
        return 0
    return items[0] + recursive_sum(items[1:])


def binary_search_rec(
    items: list[int], target: int, left: int = 0, right: int | None = None
) -> int:
    """Рекурсивный бинарный поиск: индекс или -1."""
    if right is None:
        right = len(items) - 1
    if left > right:  # базовый случай: искать негде
        return -1
    mid = (left + right) // 2
    value = items[mid]
    if value == target:
        return mid
    if value < target:
        return binary_search_rec(items, target, mid + 1, right)
    return binary_search_rec(items, target, left, mid - 1)


class Stack:
    """Стек (LIFO) на основе списка."""

    def __init__(self) -> None:
        self._items: list[Any] = []

    def push(self, item: Any) -> None:
        """Положить элемент наверх."""
        self._items.append(item)

    def pop(self) -> Any:
        """Снять верхний элемент; для пустого стека — IndexError."""
        if self.is_empty():
            raise IndexError("Нельзя снять элемент: стек пуст")
        return self._items.pop()

    def peek(self) -> Any:
        """Посмотреть верхний элемент; для пустого стека — IndexError."""
        if self.is_empty():
            raise IndexError("Нельзя посмотреть: стек пуст")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Пуст ли стек."""
        return not self._items

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items!r})"


def power(base: int, exp: int) -> int:
    """Степень рекурсивно (исправлено: базовый случай `exp == 0`, а не `exp == 1`)."""
    if exp == 0:
        return 1
    return base * power(base, exp - 1)
