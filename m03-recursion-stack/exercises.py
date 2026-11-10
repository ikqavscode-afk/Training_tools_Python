"""Модуль 3 · Рекурсия и стек. Допишите код и запустите: pytest m03-recursion-stack"""

from __future__ import annotations

from typing import Any


def factorial(n: int) -> int:
    """Задание 1. n! = n * (n-1) * ... * 1, причём 0! = 1 и 1! = 1.

    Для отрицательного n выбросьте ValueError. Решите РЕКУРСИВНО.
    """
    # TODO: базовый случай (когда остановиться) и рекурсивный случай
    raise NotImplementedError


def recursive_sum(items: list[int]) -> int:
    """Задание 2. Сумма элементов списка без циклов и без sum(). Для [] — 0."""
    # TODO: сумма пустого списка — базовый случай; иначе первый + сумма остальных
    raise NotImplementedError


def binary_search_rec(
    items: list[int], target: int, left: int = 0, right: int | None = None
) -> int:
    """Задание 3. Рекурсивный бинарный поиск в отсортированном списке. Индекс или -1.

    left и right — границы поиска (right=None означает «до конца списка»).
    """
    # TODO: если right не задан — возьмите последний индекс; если left > right — это -1
    raise NotImplementedError


class Stack:
    """Задание 4. Стек: последним пришёл — первым ушёл (LIFO)."""

    def __init__(self) -> None:
        # TODO: заведите внутренний список (по соглашению имя начинается с _)
        raise NotImplementedError

    def push(self, item: Any) -> None:
        """Положить элемент наверх."""
        raise NotImplementedError

    def pop(self) -> Any:
        """Снять и вернуть верхний элемент. Для пустого стека — IndexError."""
        raise NotImplementedError

    def peek(self) -> Any:
        """Вернуть верхний элемент, не снимая. Для пустого стека — IndexError."""
        raise NotImplementedError

    def is_empty(self) -> bool:
        """Пуст ли стек."""
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError


def power(base: int, exp: int) -> int:
    """Задание 5 («найди ошибку»). base в степени exp (exp ≥ 0) рекурсивно.

    Для некоторых значений функция «зависает» до RecursionError. Исправьте её.
    """
    if exp == 1:
        return base
    return base * power(base, exp - 1)
