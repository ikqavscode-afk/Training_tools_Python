"""Бонус b02 · Качество кода. Эталонные решения (спойлеры!)."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field


# ---------- Задание 1: dataclass ----------
@dataclass
class Student:
    """Студент: имя, курс и оценки."""

    name: str
    course: int
    grades: list[int] = field(default_factory=list)

    def average(self) -> float:
        """Средний балл; для пустого списка оценок — 0.0."""
        return sum(self.grades) / len(self.grades) if self.grades else 0.0


# ---------- Задание 2: property ----------
ABSOLUTE_ZERO = -273.15


class Temperature:
    """Температура: Цельсий с проверкой и пересчёт в Фаренгейты."""

    def __init__(self, celsius: float) -> None:
        self.celsius = celsius  # сработает сеттер с проверкой

    @property
    def celsius(self) -> float:
        """Температура в градусах Цельсия."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < ABSOLUTE_ZERO:
            raise ValueError("Температура не может быть ниже абсолютного нуля (-273.15 °C)")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        """Температура в градусах Фаренгейта."""
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = (value - 32) * 5 / 9


# ---------- Задание 3: мини-линтер ----------
def find_style_problems(source: str) -> list[str]:
    """Функции без type hints и docstring, в порядке появления в тексте."""
    functions = [
        node
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
    ]
    functions.sort(key=lambda node: (node.lineno, node.col_offset))
    problems: list[str] = []
    for func in functions:
        spec = func.args
        arguments = [
            *spec.posonlyargs,
            *spec.args,
            *([spec.vararg] if spec.vararg else []),
            *spec.kwonlyargs,
            *([spec.kwarg] if spec.kwarg else []),
        ]
        for arg in arguments:
            if arg.arg not in {"self", "cls"} and arg.annotation is None:
                problems.append(f"{func.name}: нет типа у аргумента {arg.arg}")
        if func.returns is None:
            problems.append(f"{func.name}: нет типа результата")
        if ast.get_docstring(func) is None:
            problems.append(f"{func.name}: нет docstring")
    return problems


# ---------- Задание 4: рефакторинг ----------
# страна: (базовая цена, цена за кг от 1 до 5 кг, цена за кг свыше 5 кг)
_RATES = {
    "RU": (100.0, 30.0, 20.0),
    "BY": (150.0, 45.0, 30.0),
    "KZ": (200.0, 60.0, 40.0),
}


def shipping_cost(weight: float, country: str) -> float:
    """Стоимость доставки по тарифной таблице."""
    if country not in _RATES:
        raise ValueError("Неизвестная страна")
    base, mid, high = _RATES[country]
    return base + max(0.0, min(weight, 5) - 1) * mid + max(0.0, weight - 5) * high


# ---------- Задание 5: три ловушки ----------
def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    """Добавляет тег в список (новый, если список не передан)."""
    if tags is None:
        tags = []
    tags.append(tag)
    return tags


def make_grid(rows: int, cols: int) -> list[list[int]]:
    """Таблица rows × cols из нулей с независимыми строками."""
    return [[0] * cols for _ in range(rows)]


def average(numbers: list[float]) -> float:
    """Среднее арифметическое; для пустого списка — 0.0."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


# ---------- Задание 6: формат коммита ----------
_COMMIT_TYPES = "feat|fix|docs|style|refactor|perf|test|chore|build|ci"
_COMMIT_LINE = re.compile(rf"^(?:{_COMMIT_TYPES})(?:\([a-z0-9-]+\))?!?: \S.*$")


def is_valid_commit_message(message: str) -> bool:
    """Соответствует ли сообщение формату Conventional Commits."""
    lines = message.split("\n")
    first = lines[0]
    if len(first) > 72 or first.endswith("."):
        return False
    if not _COMMIT_LINE.match(first):
        return False
    return len(lines) == 1 or lines[1] == ""
