"""Демо b02: dataclass, property, мини-линтер, ловушки и проверка сообщений коммитов.

Запуск: python bonus/b02-clean-code/demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "solutions"))
from b02_clean_code import (  # noqa: E402
    Student,
    Temperature,
    add_tag,
    find_style_problems,
    is_valid_commit_message,
    make_grid,
    shipping_cost,
)

BAD_CODE = """
def calc(l):
    r = []
    for i in range(len(l)):
        if l[i] % 2 == 0:
            r.append(l[i] * 2)
    return r
"""


def main() -> None:
    print("=== @dataclass: repr и сравнение «из коробки» ===")
    anna = Student("Аня", 3, [5, 4, 5])
    print(anna, f"→ средний балл {anna.average():.2f}")
    print("Равны ли два одинаковых студента:", Student("Б", 1) == Student("Б", 1))

    print("\n=== @property: защита от неверных значений ===")
    t = Temperature(100)
    print(f"{t.celsius} °C = {t.fahrenheit} °F")
    t.fahrenheit = 32
    print(f"после присваивания 32 °F: {t.celsius} °C")
    try:
        t.celsius = -300
    except ValueError as error:
        print("Ошибка:", error)

    print("\n=== Мини-линтер на чужом коде ===")
    print(BAD_CODE.strip())
    for problem in find_style_problems(BAD_CODE):
        print(" •", problem)

    print("\n=== Рефакторинг: тарифная таблица вместо кучи if ===")
    for weight in [0.5, 3, 10]:
        print(f"RU, {weight:>4} кг: {shipping_cost(weight, 'RU'):>7.2f}")

    print("\n=== Ловушки (в эталоне исправлены) ===")
    print("add_tag('a'), add_tag('b'):", add_tag("a"), add_tag("b"))
    grid = make_grid(2, 3)
    grid[0][0] = 1
    print("make_grid(2, 3) после grid[0][0] = 1:", grid)

    print("\n=== Сообщения коммитов ===")
    for message in [
        "feat(m09): add graphs module",
        "fix: handle empty input",
        "Added some stuff.",
        "docs update readme",
    ]:
        mark = "✓" if is_valid_commit_message(message) else "✗"
        print(f"{mark} {message}")


if __name__ == "__main__":
    main()
