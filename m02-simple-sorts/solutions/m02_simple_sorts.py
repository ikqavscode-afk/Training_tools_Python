"""Модуль 2 · Простые сортировки. Эталонные решения (спойлеры!)."""

from __future__ import annotations


def bubble_sort(items: list[int]) -> list[int]:
    """Сортировка пузырьком с ранним выходом. Возвращает новый список."""
    result = items.copy()
    n = len(result)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break
    return result


def find_min_index(items: list[int], start: int) -> int:
    """Индекс первого наименьшего элемента среди items[start:]."""
    best = start
    for j in range(start + 1, len(items)):
        if items[j] < items[best]:
            best = j
    return best


def selection_sort(items: list[int]) -> list[int]:
    """Сортировка выбором. Возвращает новый список."""
    result = items.copy()
    for i in range(len(result)):
        m = find_min_index(result, i)
        result[i], result[m] = result[m], result[i]
    return result


def insertion_sort(items: list[int]) -> list[int]:
    """Сортировка вставками. Возвращает новый список."""
    result = items.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


def sort_cards(items: list[int]) -> list[int]:
    """Карты в руке (исправлено: условие `j >= 0`, иначе нулевой элемент не сдвигается)."""
    cards = items.copy()
    for i in range(1, len(cards)):
        key = cards[i]
        j = i - 1
        while j >= 0 and cards[j] > key:
            cards[j + 1] = cards[j]
            j -= 1
        cards[j + 1] = key
    return cards
