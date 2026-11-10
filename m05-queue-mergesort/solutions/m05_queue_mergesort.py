"""Модуль 5 · Очередь и MergeSort. Эталонные решения (спойлеры!)."""

from __future__ import annotations

from collections import deque
from typing import Any


class Queue:
    """Очередь (FIFO) на основе deque."""

    def __init__(self) -> None:
        self._items: deque[Any] = deque()

    def enqueue(self, item: Any) -> None:
        """Встать в конец очереди."""
        self._items.append(item)

    def dequeue(self) -> Any:
        """Снять первого; для пустой очереди — IndexError."""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self._items.popleft()

    def peek(self) -> Any:
        """Посмотреть первого; для пустой очереди — IndexError."""
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self._items[0]

    def is_empty(self) -> bool:
        """Пуста ли очередь."""
        return not self._items

    def size(self) -> int:
        """Сколько элементов в очереди."""
        return len(self._items)

    def __repr__(self) -> str:
        return f"Queue({list(self._items)!r})"


def simulate_tasks(tasks: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Выполнить задачи по очереди; вернуть (название, время завершения)."""
    queue = Queue()
    for task in tasks:
        queue.enqueue(task)
    finished: list[tuple[str, int]] = []
    current_time = 0
    while not queue.is_empty():
        name, duration = queue.dequeue()
        current_time += duration
        finished.append((name, current_time))
    return finished


def merge(left: list[int], right: list[int]) -> list[int]:
    """Слить два отсортированных списка."""
    result: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(items: list[int]) -> list[int]:
    """Сортировка слиянием. Возвращает новый список."""
    if len(items) <= 1:
        return items.copy()
    mid = len(items) // 2
    return merge(merge_sort(items[:mid]), merge_sort(items[mid:]))


def sort_by_halves(items: list[int]) -> list[int]:
    """Сортировка по половинам (исправлено: `items[mid:]`, иначе элемент в середине теряется)."""
    if len(items) <= 1:
        return items.copy()
    mid = len(items) // 2
    left = sort_by_halves(items[:mid])
    right = sort_by_halves(items[mid:])
    return sorted(left + right)
