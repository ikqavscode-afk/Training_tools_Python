"""Модуль 1 · Поиск. Эталонные решения (спойлеры!)."""

from __future__ import annotations


def linear_search(items: list[int], target: int) -> int:
    """Вернуть индекс первого элемента, равного target, или -1."""
    for index, value in enumerate(items):
        if value == target:
            return index
    return -1


def next_bounds(left: int, right: int, mid_value: int, target: int) -> tuple[int, int]:
    """Один шаг бинарного поиска: вернуть новые границы (left, right)."""
    mid = (left + right) // 2
    if mid_value < target:
        return mid + 1, right
    return left, mid - 1


def binary_search(items: list[int], target: int) -> int:
    """Бинарный поиск в отсортированном списке: индекс или -1."""
    left, right = 0, len(items) - 1
    while left <= right:
        mid = (left + right) // 2
        value = items[mid]
        if value == target:
            return mid
        left, right = next_bounds(left, right, value, target)
    return -1


def contains(items: list[int], target: int) -> bool:
    """Есть ли target в отсортированном списке (исправлено: `left <= right`)."""
    left, right = 0, len(items) - 1
    while left <= right:
        mid = (left + right) // 2
        if items[mid] == target:
            return True
        if items[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False
