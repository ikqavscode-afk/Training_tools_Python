"""Модуль 4 · Рекурсия глубже и QuickSort. Эталонные решения (спойлеры!)."""

from __future__ import annotations


def fibonacci(n: int) -> int:
    """Число Фибоначчи рекурсивно."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def count_fib_calls(n: int) -> int:
    """Сколько вызовов сделает fibonacci(n), считая первый."""
    if n <= 1:
        return 1
    return 1 + count_fib_calls(n - 1) + count_fib_calls(n - 2)


def find_max_rec(items: list[int], left: int = 0, right: int | None = None) -> int:
    """Максимум методом «разделяй и властвуй»."""
    if not items:
        raise ValueError("Максимум пустого списка не существует")
    if right is None:
        right = len(items) - 1
    if left == right:
        return items[left]
    mid = (left + right) // 2
    left_max = find_max_rec(items, left, mid)
    right_max = find_max_rec(items, mid + 1, right)
    return left_max if left_max >= right_max else right_max


def partition(items: list[int], low: int, high: int) -> int:
    """Разбиение Ломуто части items[low..high]; возвращает индекс опорного."""
    pivot = items[high]
    boundary = low - 1  # последний индекс «маленьких»
    for j in range(low, high):
        if items[j] <= pivot:
            boundary += 1
            items[boundary], items[j] = items[j], items[boundary]
    items[boundary + 1], items[high] = items[high], items[boundary + 1]
    return boundary + 1


def _quicksort_range(items: list[int], low: int, high: int) -> None:
    if low < high:
        p = partition(items, low, high)
        _quicksort_range(items, low, p - 1)
        _quicksort_range(items, p + 1, high)


def quicksort(items: list[int]) -> list[int]:
    """Быстрая сортировка. Возвращает новый список."""
    result = items.copy()
    _quicksort_range(result, 0, len(result) - 1)
    return result


def quicksort_lists(items: list[int]) -> list[int]:
    """QuickSort на списковых выражениях (исправлено: `>=`, чтобы не терять дубликаты)."""
    if len(items) <= 1:
        return items.copy()
    pivot = items[0]
    smaller = [x for x in items[1:] if x < pivot]
    larger = [x for x in items[1:] if x >= pivot]
    return quicksort_lists(smaller) + [pivot] + quicksort_lists(larger)
