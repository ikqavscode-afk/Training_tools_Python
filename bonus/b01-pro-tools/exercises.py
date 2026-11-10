"""Бонус b01 · Инструменты профи. Допишите код и запустите: pytest bonus/b01-pro-tools"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """Задание 1 🛠. Декоратор: измеряет время вызова функции.

    Обёртка должна: вернуть результат func, сохранить имя и описание func
    (functools.wraps) и записывать время последнего вызова в секундах в атрибут
    wrapper.last_time. Время берите из time.perf_counter().
    """
    # TODO: внутри объявите wrapper(*args, **kwargs), замерьте время, верните wrapper
    raise NotImplementedError


class Timer:
    """Задание 2 🛠. Контекстный менеджер: with Timer() as t: ... потом t.elapsed (секунды).

    Исключения внутри блока with подавлять нельзя, но elapsed всё равно должен быть записан.
    """

    def __init__(self) -> None:
        # TODO: заведите self.elapsed = 0.0 и место для времени старта
        raise NotImplementedError

    def __enter__(self) -> Timer:
        raise NotImplementedError

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        raise NotImplementedError


class Node:
    """Узел бинарного дерева. Уже готов."""

    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None


def inorder_iter(root: Node | None) -> Iterator[int]:
    """Задание 3 🛠. Генератор: значения дерева по порядку «левое → корень → правое».

    Нельзя собирать все значения в список заранее: генератор отдаёт значения по одному (yield).
    """
    # TODO: yield from для левого поддерева, yield для значения узла, yield from для правого
    raise NotImplementedError


def fibonacci_cached(n: int) -> int:
    """Задание 4 🛠. Фибоначчи рекурсивно, но с кэшем (functools.lru_cache).

    Без кэша fibonacci_cached(32) считается секунды, с кэшем — мгновенно.
    """
    # TODO: добавьте декоратор @lru_cache(maxsize=None) (или короткий @cache) и сделайте рекурсию
    raise NotImplementedError


def count_in_range(sorted_values: list[int], low: int, high: int) -> int:
    """Задание 5а 🧠. Сколько чисел из ОТСОРТИРОВАННОГО списка лежит в отрезке [low, high].

    Сначала измерьте простое решение (цикл по списку) с помощью Timer, потом ускорьте его
    через модуль bisect: на списке из 100 000 чисел допустимо не больше ~40 обращений к элементам.
    """
    # TODO: bisect_left и bisect_right дают границы отрезка
    raise NotImplementedError


def k_smallest(items: list[int], k: int) -> list[int]:
    """Задание 5б 🧠. k наименьших чисел списка по возрастанию (items менять нельзя).

    Полная сортировка здесь расточительна: подойдёт модуль heapq.
    Для k <= 0 верните [], для k больше длины списка — весь список по возрастанию.
    """
    # TODO: heapq.nsmallest
    raise NotImplementedError
