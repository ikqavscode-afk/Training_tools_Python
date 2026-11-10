"""Модуль 5 · Очередь и MergeSort. Допишите код и запустите: pytest m05-queue-mergesort"""

from __future__ import annotations

from typing import Any


class Queue:
    """Задание 1. Очередь: первым пришёл — первым ушёл (FIFO).

    Внутри используйте collections.deque: у него быстрое снятие с левого края.
    """

    def __init__(self) -> None:
        # TODO: from collections import deque и создайте пустую очередь
        raise NotImplementedError

    def enqueue(self, item: Any) -> None:
        """Встать в конец очереди."""
        raise NotImplementedError

    def dequeue(self) -> Any:
        """Покинуть очередь с начала и вернуть элемент. Для пустой очереди — IndexError."""
        raise NotImplementedError

    def peek(self) -> Any:
        """Посмотреть первого в очереди, не убирая. Для пустой очереди — IndexError."""
        raise NotImplementedError

    def is_empty(self) -> bool:
        """Пуста ли очередь."""
        raise NotImplementedError

    def size(self) -> int:
        """Сколько элементов в очереди."""
        raise NotImplementedError


def simulate_tasks(tasks: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Задание 2. Обработка задач по очереди, по одной за раз.

    tasks — список (название, длительность в секундах). Верните список
    (название, время завершения) в порядке выполнения. Используйте свой Queue.
    Пример: [("A", 3), ("B", 5)] -> [("A", 3), ("B", 8)]
    """
    # TODO: поставьте все задачи в очередь, затем снимайте по одной и копите время
    raise NotImplementedError


def merge(left: list[int], right: list[int]) -> list[int]:
    """Задание 3. Слить два ОТСОРТИРОВАННЫХ списка в один отсортированный. Входные не менять."""
    # TODO: два указателя i и j, берите меньший из текущих; в конце допишите «хвосты»
    raise NotImplementedError


def merge_sort(items: list[int]) -> list[int]:
    """Задание 4. Сортировка слиянием. Верните НОВЫЙ список."""
    # TODO: длина <= 1 — уже отсортировано; иначе разделите пополам, отсортируйте и слейте
    raise NotImplementedError


def sort_by_halves(items: list[int]) -> list[int]:
    """Задание 5 («найди ошибку»). Сортировка слиянием «в одну строку».

    Функция написана, но иногда «теряет» элементы. Найдите ошибку и исправьте её.
    """
    if len(items) <= 1:
        return items.copy()
    mid = len(items) // 2
    left = sort_by_halves(items[:mid])
    right = sort_by_halves(items[mid + 1 :])
    return sorted(left + right)
