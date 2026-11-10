"""Бонус b01 · Инструменты профи. Эталонные решения (спойлеры!)."""

from __future__ import annotations

import functools
import heapq
import time
from bisect import bisect_left, bisect_right
from collections.abc import Callable, Iterator
from types import TracebackType
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Декоратор: записывает время последнего вызова в ``wrapper.last_time`` (секунды)."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            wrapper.last_time = time.perf_counter() - start  # type: ignore[attr-defined]

    wrapper.last_time = 0.0  # type: ignore[attr-defined]
    return wrapper


class Timer:
    """Контекстный менеджер: замеряет время блока ``with`` в ``elapsed`` (секунды)."""

    def __init__(self) -> None:
        self.elapsed = 0.0
        self._start = 0.0

    def __enter__(self) -> Timer:
        self._start = time.perf_counter()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.elapsed = time.perf_counter() - self._start  # исключение не подавляем


class Node:
    """Узел бинарного дерева."""

    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None


def inorder_iter(root: Node | None) -> Iterator[int]:
    """Генератор: левое → корень → правое."""
    if root is None:
        return
    yield from inorder_iter(root.left)
    yield root.value
    yield from inorder_iter(root.right)


@functools.cache  # то же, что @functools.lru_cache(maxsize=None)
def fibonacci_cached(n: int) -> int:
    """Фибоначчи с кэшем результатов."""
    if n <= 1:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)


def count_in_range(sorted_values: list[int], low: int, high: int) -> int:
    """Сколько чисел отсортированного списка лежит в [low, high]: два бинарных поиска."""
    if low > high:
        return 0
    return bisect_right(sorted_values, high) - bisect_left(sorted_values, low)


def k_smallest(items: list[int], k: int) -> list[int]:
    """k наименьших чисел по возрастанию через кучу."""
    if k <= 0:
        return []
    return heapq.nsmallest(k, items)
