"""Демо модуля 5: очередь задач, MergeSort против пузырька, deque против list.pop(0).

Запуск: python m05-queue-mergesort/demo.py
"""

from __future__ import annotations

import random
import sys
import time
from collections import deque
from collections.abc import Callable
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "solutions"))
sys.path.insert(0, str(HERE.parent / "m02-simple-sorts" / "solutions"))
from m02_simple_sorts import bubble_sort  # noqa: E402
from m05_queue_mergesort import Queue, merge_sort, simulate_tasks  # noqa: E402


def queue_demo() -> None:
    queue = Queue()
    for x in [10, 20, 30]:
        queue.enqueue(x)
        print(f"enqueue({x}) -> {queue}")
    print(f"peek() = {queue.peek()}")
    print(f"dequeue() = {queue.dequeue()} -> {queue}")


def tasks_demo() -> None:
    tasks = [
        ("Загрузка данных", 3),
        ("Обработка", 5),
        ("Отправка почты", 1),
        ("Отчёт", 4),
        ("Резервное копирование", 7),
    ]
    for name, finished_at in simulate_tasks(tasks):
        print(f"[{finished_at:>3} с] задача «{name}» завершена")


def measure(func: Callable[[list[int]], list[int]], data: list[int]) -> float:
    start = time.perf_counter()
    func(data)
    return time.perf_counter() - start


def sorts_demo() -> None:
    random.seed(1)
    print(f"{'Размер':>7} | {'MergeSort, с':>13} | {'Пузырёк, с':>11} | {'Во сколько раз':>14}")
    print("-" * 56)
    for size in [10, 100, 1000]:
        data = [random.randint(0, 1000) for _ in range(size)]
        t_merge = measure(merge_sort, data)
        t_bubble = measure(bubble_sort, data)
        print(f"{size:>7} | {t_merge:>13.6f} | {t_bubble:>11.6f} | {t_bubble / t_merge:>13.1f}x")


def pop_demo() -> None:
    n = 50_000
    as_list = list(range(n))
    start = time.perf_counter()
    while as_list:
        as_list.pop(0)
    t_list = time.perf_counter() - start

    as_deque = deque(range(n))
    start = time.perf_counter()
    while as_deque:
        as_deque.popleft()
    t_deque = time.perf_counter() - start
    print(f"list.pop(0):   {t_list:.4f} с")
    print(f"deque.popleft: {t_deque:.4f} с  (быстрее в {t_list / t_deque:.0f} раз)")


def main() -> None:
    print("=== Очередь ===")
    queue_demo()
    print("\n=== Обработка задач по очереди ===")
    tasks_demo()
    print("\n=== MergeSort против пузырька ===")
    sorts_demo()
    print("\n=== Снимаем элементы с начала: список и deque (по 50 000) ===")
    pop_demo()


if __name__ == "__main__":
    main()
