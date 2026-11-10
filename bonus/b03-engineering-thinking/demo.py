"""Демо b03: читаем замеры, ищем причину сбоя, считаем влияние изменения.

Запуск: python bonus/b03-engineering-thinking/demo.py
"""

from __future__ import annotations

import random
import sys
import time
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "solutions"))
from b03_engineering_thinking import (  # noqa: E402
    average_speed,
    choose_structure,
    classify_growth,
    find_breaking_inputs,
    find_dependents,
    find_duplicates,
    growth_factor,
    process_orders,
    process_orders_legacy,
)


def best_time(func: Callable[[], object], repeats: int = 5) -> float:
    """Лучшее из нескольких замеров: так меньше шума от других программ."""
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        func()
        best = min(best, time.perf_counter() - start)
    return best


def pairs_count(n: int) -> int:
    """Считает пары (i, j): два вложенных цикла."""
    total = 0
    for i in range(n):
        for j in range(n):
            total += i ^ j
    return total


def measure_and_classify() -> None:
    rng = random.Random(1)
    experiments: list[tuple[str, list[int], Callable[[int], Callable[[], object]]]] = [
        ("x in set", [10**5, 2 * 10**5, 4 * 10**5, 8 * 10**5], lambda n: _set_lookup(n)),
        ("sum(list)", [10**5, 2 * 10**5, 4 * 10**5, 8 * 10**5], lambda n: _list_sum(n)),
        ("sorted(list)", [10**5, 2 * 10**5, 4 * 10**5, 8 * 10**5], lambda n: _sort(n, rng)),
        ("два цикла", [200, 400, 800, 1600], lambda n: lambda: pairs_count(n)),
    ]
    print(f"{'алгоритм':<14} {'множитель при ×2':>17}   вывод")
    for name, sizes, make in experiments:
        times = [best_time(make(n)) for n in sizes]
        factor = growth_factor(sizes, times)
        print(f"{name:<14} {factor:>17.2f}   {classify_growth(factor)}")
    print("(замеры шумные: смотрите на множитель, а не на одну цифру)")


def _set_lookup(n: int) -> Callable[[], object]:
    data = set(range(n))
    return lambda: [(-1) in data for _ in range(1000)]


def _list_sum(n: int) -> Callable[[], object]:
    data = list(range(n))
    return lambda: sum(data)


def _sort(n: int, rng: random.Random) -> Callable[[], object]:
    data = [rng.random() for _ in range(n)]
    return lambda: sorted(data)


def main() -> None:
    print("=== Выбор структуры данных ===")
    for scenario in range(1, 7):
        print(f"сценарий {scenario}: {choose_structure(scenario)}")

    print("\n=== Читаем замеры ===")
    measure_and_classify()

    print("\n=== Найди причину: на чём «падает» average_speed ===")
    for text in find_breaking_inputs():
        try:
            average_speed(10, text)
        except Exception as error:
            print(f"{text!r:>16} → {type(error).__name__}: {error}")

    print("\n=== Рост ×100: поиск повторов ===")
    rng = random.Random(2)
    for n in [1000, 100_000]:
        data = [rng.randint(0, n) for _ in range(n)]
        elapsed = best_time(lambda data=data: find_duplicates(data), repeats=3)
        print(
            f"n = {n:>7}: {elapsed * 1000:8.2f} мс (в списке {len(find_duplicates(data))} повторов)"
        )

    print("\n=== Декомпозиция: результат тот же ===")
    lines = ["A1;100.5;2", "bad", "B2;50;1", "C3;10;0"]
    print("legacy:", process_orders_legacy(lines))
    print("части :", process_orders(lines))

    print("\n=== Системное мышление: что заденет изменение load() ===")
    source = (
        "def load(): return 1\n"
        "def parse(): return load()\n"
        "def report(): return parse()\n"
        "def main(): report()\n"
    )
    print("напрямую :", find_dependents(source, "load"))
    print("цепочкой :", find_dependents(source, "load", transitive=True))


if __name__ == "__main__":
    main()
