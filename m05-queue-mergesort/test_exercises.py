"""Проверка модуля 5. Запуск: pytest m05-queue-mergesort"""

from __future__ import annotations

from collections.abc import Callable
from types import ModuleType

import pytest

SORT_CASES = [
    [64, 34, 25, 12, 22, 11, 90],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [3, 1, 2, 3, 1, 2],
    [-5, 10, 0, -1],
    [],
    [42],
    [2, 1],
    [8, 3, 5],
]
SORT_IDS = [
    "случайный",
    "уже отсортирован",
    "в обратном порядке",
    "дубликаты",
    "отрицательные",
    "пустой",
    "один элемент",
    "два элемента",
    "три элемента",
]


def test_queue_is_empty_at_start(target: ModuleType) -> None:
    queue = target.Queue()
    assert queue.is_empty() is True
    assert queue.size() == 0


def test_queue_enqueue_changes_size(target: ModuleType) -> None:
    queue = target.Queue()
    queue.enqueue(10)
    queue.enqueue(20)
    assert queue.size() == 2
    assert queue.is_empty() is False


def test_queue_is_fifo(target: ModuleType) -> None:
    """FIFO: первым пришёл — первым ушёл (в отличие от стека)."""
    queue = target.Queue()
    for item in [10, 20, 30]:
        queue.enqueue(item)
    assert [queue.dequeue(), queue.dequeue(), queue.dequeue()] == [10, 20, 30]
    assert queue.is_empty()


def test_queue_peek_does_not_remove(target: ModuleType) -> None:
    queue = target.Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    assert queue.peek() == 1
    assert queue.size() == 2


def test_queue_dequeue_empty_raises(target: ModuleType) -> None:
    with pytest.raises(IndexError):
        target.Queue().dequeue()


def test_queue_peek_empty_raises(target: ModuleType) -> None:
    with pytest.raises(IndexError):
        target.Queue().peek()


@pytest.mark.parametrize(
    ("tasks", "expected"),
    [
        ([("A", 3), ("B", 5)], [("A", 3), ("B", 8)]),
        (
            [("Загрузка", 3), ("Обработка", 5), ("Почта", 1), ("Отчёт", 4)],
            [("Загрузка", 3), ("Обработка", 8), ("Почта", 9), ("Отчёт", 13)],
        ),
        ([("Одна", 7)], [("Одна", 7)]),
        ([], []),
    ],
    ids=["две задачи", "четыре задачи", "одна задача", "нет задач"],
)
def test_simulate_tasks(
    target: ModuleType, tasks: list[tuple[str, int]], expected: list[tuple[str, int]]
) -> None:
    assert target.simulate_tasks(tasks) == expected


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ([1, 3, 5], [2, 4, 6], [1, 2, 3, 4, 5, 6]),
        ([], [1, 2], [1, 2]),
        ([1, 2], [], [1, 2]),
        ([], [], []),
        ([1, 1, 2], [1, 3], [1, 1, 1, 2, 3]),
        ([5, 6], [1, 2], [1, 2, 5, 6]),
    ],
    ids=["чередуются", "левый пуст", "правый пуст", "оба пусты", "дубликаты", "правый меньше"],
)
def test_merge(target: ModuleType, left: list[int], right: list[int], expected: list[int]) -> None:
    assert target.merge(left, right) == expected


def test_merge_does_not_change_inputs(target: ModuleType) -> None:
    left, right = [1, 3], [2, 4]
    target.merge(left, right)
    assert left == [1, 3] and right == [2, 4], "Входные списки менять нельзя"


@pytest.mark.parametrize("items", SORT_CASES, ids=SORT_IDS)
def test_merge_sort(target: ModuleType, items: list[int]) -> None:
    assert target.merge_sort(items) == sorted(items)


def test_merge_sort_does_not_change_input(target: ModuleType) -> None:
    original = [3, 1, 2]
    data = original.copy()
    target.merge_sort(data)
    assert data == original, "Исходный список менять нельзя"


@pytest.mark.bugfix
def test_sort_by_halves(target: ModuleType) -> None:
    """Задание «найди ошибку»: засчитывается, только когда верны ВСЕ случаи."""
    func: Callable[[list[int]], list[int]] = target.sort_by_halves
    for items, name in zip(SORT_CASES, SORT_IDS, strict=True):
        assert func(items) == sorted(items), (
            f"Случай «{name}»: sort_by_halves({items}) вернула {func(items)}. "
            "Подсказка: сложите длины обеих половин, сошлись ли они с длиной входа?"
        )
