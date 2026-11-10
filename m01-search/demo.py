"""Демо модуля 1: сравниваем линейный и бинарный поиск по времени.

Запуск: python m01-search/demo.py
Если установлен matplotlib (pip install -e ".[demo]"), график сохранится в assets/.
"""

from __future__ import annotations

import sys
import time
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "solutions"))
from m01_search import binary_search, linear_search  # noqa: E402

SIZES = [10, 100, 1_000, 10_000, 100_000]


def measure(func: Callable[[list[int], int], int], data: list[int], repeats: int) -> float:
    """Среднее время одного вызова в микросекундах (ищем последний элемент — худший случай)."""
    target = data[-1]
    start = time.perf_counter()
    for _ in range(repeats):
        func(data, target)
    return (time.perf_counter() - start) / repeats * 1e6


def main() -> None:
    print(f"{'Размер':>8} | {'Линейный, мкс':>14} | {'Бинарный, мкс':>14} | {'Во сколько раз':>14}")
    print("-" * 60)
    linear_times: list[float] = []
    binary_times: list[float] = []
    for size in SIZES:
        data = list(range(size))
        repeats = max(1, 200_000 // size)
        t_lin = measure(linear_search, data, repeats)
        t_bin = measure(binary_search, data, repeats)
        linear_times.append(t_lin)
        binary_times.append(t_bin)
        print(f"{size:>8} | {t_lin:>14.3f} | {t_bin:>14.3f} | {t_lin / t_bin:>13.1f}x")

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n(matplotlib не установлен — график пропущен)")
        return

    plt.figure(figsize=(7, 4))
    plt.semilogy(SIZES, linear_times, "s-", label="Линейный O(n)")
    plt.semilogy(SIZES, binary_times, "o-", label="Бинарный O(log n)")
    plt.xlabel("Размер списка")
    plt.ylabel("Время, мкс (лог. шкала)")
    plt.title("Линейный и бинарный поиск")
    plt.legend()
    plt.grid(alpha=0.3)
    out = Path(__file__).parent.parent / "assets" / "m01_search.png"
    plt.savefig(out, dpi=120, bbox_inches="tight")
    print(f"\nГрафик сохранён: {out}")


if __name__ == "__main__":
    main()
