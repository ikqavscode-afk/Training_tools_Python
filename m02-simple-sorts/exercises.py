"""Модуль 2 · Простые сортировки. Допишите функции и запустите: pytest m02-simple-sorts"""

from __future__ import annotations


def bubble_sort(items: list[int]) -> list[int]:
    """Задание 1. Сортировка пузырьком. Верните НОВЫЙ отсортированный список.

    Исходный список менять нельзя. Если за проход не было ни одного обмена —
    список уже отсортирован, можно остановиться.
    """
    # TODO: сделайте копию, затем проходы по парам соседей
    raise NotImplementedError


def find_min_index(items: list[int], start: int) -> int:
    """Задание 2а. Индекс наименьшего элемента среди items[start:].

    Если наименьших несколько — верните индекс первого из них.
    """
    # TODO: запомните индекс лучшего кандидата и сравнивайте с остальными
    raise NotImplementedError


def selection_sort(items: list[int]) -> list[int]:
    """Задание 2б. Сортировка выбором. Верните НОВЫЙ отсортированный список."""
    # TODO: на каждом шаге ставьте минимальный из оставшихся на своё место
    raise NotImplementedError


def insertion_sort(items: list[int]) -> list[int]:
    """Задание 3. Сортировка вставками. Верните НОВЫЙ отсортированный список."""
    # TODO: берите по одному элементу и вставляйте в уже отсортированную левую часть
    raise NotImplementedError


def sort_cards(items: list[int]) -> list[int]:
    """Задание 4 («найди ошибку»). Раскладываем карты в руке по возрастанию.

    Функция написана, но иногда возвращает неотсортированный список.
    Найдите ошибку и исправьте её.
    """
    cards = items.copy()
    for i in range(1, len(cards)):
        key = cards[i]
        j = i - 1
        while j > 0 and cards[j] > key:
            cards[j + 1] = cards[j]
            j -= 1
        cards[j + 1] = key
    return cards
