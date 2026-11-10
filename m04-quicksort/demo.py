"""Демо модуля 4: дерево вызовов Фибоначчи и скорость QuickSort.

Запуск: python m04-quicksort/demo.py
"""

from __future__ import annotations

import random
import sys
import time
from collections.abc import Callable
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "solutions"))
sys.path.insert(0, str(HERE.parent / "m02-simple-sorts" / "solutions"))
from m02_simple_sorts import insertion_sort  # noqa: E402
from m04_quicksort import count_fib_calls, quicksort  # noqa: E402


def fib_tree(n: int, depth: int = 0) -> int:
    """Фибоначчи с печатью дерева вызовов."""
    print("  " * depth + f"fib({n})")
    if n <= 1:
        return n
    return fib_tree(n - 1, depth + 1) + fib_tree(n - 2, depth + 1)


def measure(func: Callable[[list[int]], list[int]], data: list[int]) -> float:
    start = time.perf_counter()
    func(data)
    return (time.perf_counter() - start) * 1000


def main() -> None:
    print("=== Дерево вызовов fib(4) ===")
    fib_tree(4)

    print("\n=== Сколько вызовов делает fib(n) ===")
    for n in [5, 10, 15, 20, 25]:
        print(f"n={n:>2}: {count_fib_calls(n):>9} вызовов")
    print("Вызовов растёт очень быстро: каждый вызов порождает ещё два.")

    print("\n=== QuickSort против вставок и sorted(), мс ===")
    random.seed(1)
    print(f"{'Размер':>7} | {'QuickSort':>10} | {'Вставки':>10} | {'sorted()':>10}")
    print("-" * 47)
    for size in [10, 100, 1000]:
        data = [random.randint(0, 1000) for _ in range(size)]
        t_q = measure(quicksort, data)
        t_i = measure(insertion_sort, data)
        t_s = measure(sorted, data)
        print(f"{size:>7} | {t_q:>10.3f} | {t_i:>10.3f} | {t_s:>10.3f}")

    print("\n=== Подвох: QuickSort с опорой «последний» на уже отсортированных данных ===")
    n = 500
    random_data = [random.randint(0, 1000) for _ in range(n)]
    sorted_data = sorted(random_data)
    print(f"Случайный список: {measure(quicksort, random_data):.3f} мс")
    print(f"Отсортированный:  {measure(quicksort, sorted_data):.3f} мс (опора всегда максимум)")


if __name__ == "__main__":
    main()
