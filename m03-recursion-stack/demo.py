"""Демо модуля 3: как рекурсия растёт и сворачивается, как работает стек, где предел рекурсии.

Запуск: python m03-recursion-stack/demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "solutions"))
from m03_recursion_stack import Stack, recursive_sum  # noqa: E402


def traced_factorial(n: int, depth: int = 0) -> int:
    """Факториал с печатью шагов: видно, как растёт и сворачивается стек вызовов."""
    pad = "  " * depth
    print(f"{pad}→ factorial({n})")
    if n <= 1:
        print(f"{pad}  базовый случай, возвращаем 1")
        return 1
    result = n * traced_factorial(n - 1, depth + 1)
    print(f"{pad}← factorial({n}) = {result}")
    return result


def stack_demo() -> None:
    stack = Stack()
    for item in [10, 20, 30]:
        stack.push(item)
        print(f"push({item}) -> {stack}")
    while not stack.is_empty():
        print(f"pop() = {stack.pop()} -> {stack}")


def recursion_limit_demo() -> None:
    limit = sys.getrecursionlimit()
    print(f"Предел рекурсии в Python: {limit} вложенных вызовов")
    try:
        recursive_sum(list(range(limit * 2)))
    except RecursionError:
        print("Список слишком длинный для рекурсии: получили RecursionError")


def main() -> None:
    print("=== Факториал: стек вызовов ===")
    traced_factorial(4)
    print("\n=== Стек: последним пришёл — первым ушёл ===")
    stack_demo()
    print("\n=== Где предел рекурсии ===")
    recursion_limit_demo()


if __name__ == "__main__":
    main()
