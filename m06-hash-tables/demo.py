"""Демо модуля 6: корзины, коллизии, resize и скорость поиска в словаре.

Запуск: python m06-hash-tables/demo.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "solutions"))
from m06_hash_tables import HashTable, find_collisions, string_hash  # noqa: E402

FRUITS = [
    ("apple", 10),
    ("banana", 20),
    ("cherry", 30),
    ("strawberry", 40),
    ("berry", 50),
    ("kerry", 60),
    ("marry", 70),
    ("derry", 80),
    ("kiwi", 90),
    ("lemon", 100),
]


def hash_demo() -> None:
    for word in ["hello", "abc", "cba", "bca"]:
        letters = " + ".join(f"{c}({ord(c)})" for c in word)
        print(f"string_hash('{word}') = {letters} = {string_hash(word)}")
    print("Анаграммы дают один хэш — это коллизия.")


def table_demo() -> None:
    table = HashTable(capacity=5)
    for key, value in FRUITS:
        table.insert(key, value)
    print(table)
    print(f"size={table.size}, capacity={table.capacity}")
    print("Коллизии при capacity=5:", find_collisions([k for k, _ in FRUITS], 5))
    table.resize()
    print("\nПосле resize:")
    print(table)
    print(f"size={table.size}, capacity={table.capacity}")
    print("Коллизии при capacity=10:", find_collisions([k for k, _ in FRUITS], 10))


def speed_demo() -> None:
    n = 100_000
    as_list = list(range(n))
    as_dict = dict.fromkeys(range(n))
    target = n - 1
    repeats = 200

    start = time.perf_counter()
    for _ in range(repeats):
        _ = target in as_list
    t_list = (time.perf_counter() - start) / repeats * 1e6

    start = time.perf_counter()
    for _ in range(repeats):
        _ = target in as_dict
    t_dict = (time.perf_counter() - start) / repeats * 1e6

    print(f"Поиск в списке из {n}: {t_list:>9.2f} мкс (перебор)")
    print(f"Поиск в dict из {n}:   {t_dict:>9.2f} мкс (хэш-таблица)")


def main() -> None:
    print("=== Хэш строки ===")
    hash_demo()
    print("\n=== Хэш-таблица ===")
    table_demo()
    print("\n=== Список против dict ===")
    speed_demo()
    print(f"\nВстроенный hash('abc') = {hash('abc')}: запустите демо ещё раз, число будет другим.")


if __name__ == "__main__":
    main()
