"""Демо b01: измеряем до оптимизации, кэшируем, ленимся и ищем быстро.

Запуск: python bonus/b01-pro-tools/demo.py
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "solutions"))
from b01_pro_tools import (  # noqa: E402
    Node,
    Timer,
    count_in_range,
    fibonacci_cached,
    inorder_iter,
    k_smallest,
    timer,
)


@timer
def fibonacci_plain(n: int) -> int:
    return n if n <= 1 else fibonacci_plain(n - 1) + fibonacci_plain(n - 2)


@timer
def count_naive(values: list[int], low: int, high: int) -> int:
    return sum(1 for v in values if low <= v <= high)


@timer
def count_fast(values: list[int], low: int, high: int) -> int:
    return count_in_range(values, low, high)


def build_balanced(low: int, high: int) -> Node | None:
    """Сбалансированное дерево поиска со значениями low..high (глубина около log2(n))."""
    if low > high:
        return None
    mid = (low + high) // 2
    node = Node(mid)
    node.left = build_balanced(low, mid - 1)
    node.right = build_balanced(mid + 1, high)
    return node


def main() -> None:
    print("=== Фибоначчи: без кэша и с кэшем ===")
    fibonacci_plain(27)
    print(f"без кэша  fib(27): {fibonacci_plain.last_time * 1000:>10.2f} мс")  # type: ignore[attr-defined]
    with Timer() as t:
        fibonacci_cached(27)
    print(f"с кэшем   fib(27): {t.elapsed * 1000:>10.2f} мс")

    print("\n=== Сначала измерь, потом оптимизируй: числа в отрезке ===")
    values = list(range(1_000_000))
    count_naive(values, 10, 999_990)
    count_fast(values, 10, 999_990)
    naive_ms = count_naive.last_time * 1000  # type: ignore[attr-defined]
    fast_ms = count_fast.last_time * 1000  # type: ignore[attr-defined]
    print(f"перебор  : {naive_ms:>10.3f} мс")
    print(f"bisect   : {fast_ms:>10.3f} мс  (быстрее в {naive_ms / max(fast_ms, 1e-9):,.0f} раз)")

    print("\n=== Генератор ленив: берём первые три значения из 100 000 ===")
    tree = build_balanced(1, 100_000)
    with Timer() as t_first:
        generator = inorder_iter(tree)
        first_three = [next(generator) for _ in range(3)]
    with Timer() as t_all:
        everything = list(inorder_iter(tree))
    print(first_three, "← остальные значения даже не вычислялись")
    first_ms = t_first.elapsed * 1000
    all_ms = t_all.elapsed * 1000
    print(f"первые 3: {first_ms:.3f} мс, все {len(everything)}: {all_ms:.1f} мс")

    print("\n=== heapq: 5 наименьших из 200 000 ===")
    rng = random.Random(1)
    big = [rng.randint(0, 10**9) for _ in range(200_000)]
    with Timer() as t_heap:
        small = k_smallest(big, 5)
    with Timer() as t_sort:
        sorted(big)[:5]
    print(f"результат: {small}")
    print(
        f"куча: {t_heap.elapsed * 1000:.2f} мс, полная сортировка: {t_sort.elapsed * 1000:.2f} мс"
    )


if __name__ == "__main__":
    main()
