"""Демо модуля 2: сравниваем три простые сортировки по времени.

Запуск: python m02-simple-sorts/demo.py
Если установлен matplotlib (pip install -e ".[demo]"), график сохранится в assets/.
"""

from __future__ import annotations

import random
import sys
import time
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "solutions"))
from m02_simple_sorts import bubble_sort, insertion_sort, selection_sort  # noqa: E402

SIZES = [100, 200, 400, 800]
SORTS: dict[str, Callable[[list[int]], list[int]]] = {
    "Пузырёк": bubble_sort,
    "Выбор": selection_sort,
    "Вставки": insertion_sort,
}


def measure(func: Callable[[list[int]], list[int]], data: list[int]) -> float:
    """Время одной сортировки в миллисекундах."""
    start = time.perf_counter()
    func(data)
    return (time.perf_counter() - start) * 1000


def main() -> None:
    random.seed(1)
    results: dict[str, list[float]] = {name: [] for name in SORTS}
    print(f"{'Размер':>8} | " + " | ".join(f"{name + ', мс':>12}" for name in SORTS))
    print("-" * 56)
    for size in SIZES:
        data = [random.randint(0, 1000) for _ in range(size)]
        row = []
        for name, func in SORTS.items():
            t = measure(func, data)
            results[name].append(t)
            row.append(f"{t:>12.3f}")
        print(f"{size:>8} | " + " | ".join(row))
    print("\nУдвоили размер — время выросло примерно в 4 раза: это и есть O(n²).")

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("(matplotlib не установлен — график пропущен)")
        return

    plt.figure(figsize=(7, 4))
    for name, times in results.items():
        plt.plot(SIZES, times, "o-", label=name)
    plt.xlabel("Размер списка")
    plt.ylabel("Время, мс")
    plt.title("Простые сортировки")
    plt.legend()
    plt.grid(alpha=0.3)
    out = Path(__file__).parent.parent / "assets" / "m02_simple_sorts.png"
    plt.savefig(out, dpi=120, bbox_inches="tight")
    print(f"График сохранён: {out}")


if __name__ == "__main__":
    main()
