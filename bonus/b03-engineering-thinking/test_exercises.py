"""Проверка бонус-модуля b03. Запуск: pytest bonus/b03-engineering-thinking"""

from __future__ import annotations

import ast
import inspect
import math
import random
import textwrap
from collections import Counter
from types import ModuleType
from typing import Any

import pytest

# ---------- Задание 1: выбери структуру данных ----------

SCENARIOS = [
    (1, "dict", "Нужен быстрый поиск значения по ключу (имя → номер): это словарь."),
    (2, "set", "Нужны уникальные элементы и быстрая проверка «встречался ли»: это множество."),
    (3, "deque", "Снимаем с начала и добавляем в конец: list.pop(0) медленный, нужен deque."),
    (4, "heapq", "Всё время нужен наименьший элемент из потока: это куча (heapq)."),
    (5, "list", "Важны порядок и доступ по номеру: подойдёт обычный список."),
    (6, "dict", "Счётчик «слово → сколько раз»: словарь (или Counter на его основе)."),
]


@pytest.mark.parametrize(
    ("scenario", "expected", "reason"),
    SCENARIOS,
    ids=[f"сценарий {n}" for n, _, _ in SCENARIOS],
)
def test_choose_structure(target: ModuleType, scenario: int, expected: str, reason: str) -> None:
    got = target.choose_structure(scenario)
    assert got == expected, f"Для сценария {scenario} выбрано {got!r}. {reason}"


# ---------- Задание 2: прочитай замеры ----------

SIZES = [1000, 2000, 4000, 8000, 16000]
MODELS = {
    "O(1)": lambda n: 5.0,
    "O(log n)": lambda n: math.log2(n),
    "O(n)": lambda n: float(n),
    "O(n log n)": lambda n: n * math.log2(n),
    "O(n^2)": lambda n: float(n * n),
}


@pytest.mark.parametrize("name", list(MODELS))
def test_pipeline_classifies_each_model(target: ModuleType, name: str) -> None:
    times = [MODELS[name](n) for n in SIZES]
    factor = target.growth_factor(SIZES, times)
    assert target.classify_growth(factor) == name, (
        f"Для замеров вида {name} множитель роста {factor:.3f} классифицирован неверно"
    )


@pytest.mark.parametrize("name", list(MODELS))
def test_pipeline_is_robust_to_small_noise(target: ModuleType, name: str) -> None:
    """Замеры шумят: каждое второе значение завышено на 2 %, остальные занижены."""
    times = [MODELS[name](n) * (1.02 if i % 2 == 0 else 0.98) for i, n in enumerate(SIZES)]
    factor = target.growth_factor(SIZES, times)
    assert target.classify_growth(factor) == name


@pytest.mark.parametrize(
    ("sizes", "times", "expected"),
    [
        ([1000, 2000], [1.0, 4.0], 4.0),
        ([100, 200], [1.0, 2.0], 2.0),
        ([10, 1000], [3.0, 300.0], 2.0),
        ([1000, 2000, 4000], [7.0, 7.0, 7.0], 1.0),
    ],
    ids=["квадрат", "линейно", "размер выше чем вдвое", "константа"],
)
def test_growth_factor(
    target: ModuleType, sizes: list[int], times: list[float], expected: float
) -> None:
    assert target.growth_factor(sizes, times) == pytest.approx(expected, rel=1e-6)


@pytest.mark.parametrize(
    ("sizes", "times"),
    [([1000], [1.0]), ([], []), ([1000, 2000], [1.0])],
    ids=["один замер", "пусто", "разная длина"],
)
def test_growth_factor_rejects_bad_input(
    target: ModuleType, sizes: list[int], times: list[float]
) -> None:
    with pytest.raises(ValueError):
        target.growth_factor(sizes, times)


@pytest.mark.parametrize(
    ("factor", "expected"),
    [
        (1.0, "O(1)"),
        (1.04, "O(1)"),
        (1.09, "O(log n)"),
        (1.4, "O(log n)"),
        (1.8, "O(n)"),
        (2.0, "O(n)"),
        (2.09, "O(n)"),
        (2.17, "O(n log n)"),
        (2.9, "O(n log n)"),
        (4.0, "O(n^2)"),
        (8.0, "O(n^2)"),
    ],
)
def test_classify_growth(target: ModuleType, factor: float, expected: str) -> None:
    assert target.classify_growth(factor) == expected


# ---------- Задание 3: найди причину ----------


def test_find_breaking_inputs(target: ModuleType) -> None:
    inputs = target.find_breaking_inputs()
    assert len(inputs) >= 3, "Нужно не меньше трёх входных строк"
    assert len(set(inputs)) == len(inputs), "Строки должны быть разными"
    kinds: set[type] = set()
    for text in inputs:
        try:
            target.average_speed(10, text)
        except Exception as error:
            kinds.add(type(error))
        else:
            pytest.fail(f"average_speed(10, {text!r}) не упала: эта строка не подходит")
    assert len(kinds) >= 2, (
        f"Все сбои одного вида ({kinds}). Подумайте, какие ещё бывают: деление на ноль, "
        "неверный формат строки, не числа."
    )


# ---------- Задание 4: что будет при росте ×100 ----------


class Tracked(int):
    """Число, которое считает, сколько раз его сравнивали на равенство."""

    comparisons = 0

    def __eq__(self, other: object) -> bool:
        Tracked.comparisons += 1
        return int(self) == int(other)  # type: ignore[call-overload]  # other всегда число

    def __hash__(self) -> int:
        return int.__hash__(self)


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([1, 2, 2, 3, 3, 3], [2, 3]),
        ([], []),
        ([1], []),
        ([5, 5], [5]),
        ([4, 3, 2, 1], []),
        ([-1, -1, 0, 0, 7], [-1, 0]),
        ([9, 1, 9, 1, 9], [1, 9]),
    ],
    ids=["несколько", "пустой", "один", "пара", "без повторов", "отрицательные", "вперемешку"],
)
def test_find_duplicates(target: ModuleType, items: list[int], expected: list[int]) -> None:
    assert target.find_duplicates(items) == expected


def test_find_duplicates_does_not_change_input(target: ModuleType) -> None:
    data = [3, 1, 3]
    target.find_duplicates(data)
    assert data == [3, 1, 3]


def test_find_duplicates_scales(target: ModuleType) -> None:
    """При списке из 2000 чисел перебор «каждый с каждым» — миллионы сравнений."""
    rng = random.Random(7)
    plain = [rng.randint(0, 1500) for _ in range(2000)]
    expected = sorted(value for value, count in Counter(plain).items() if count > 1)
    items = [Tracked(value) for value in plain]
    Tracked.comparisons = 0
    result = target.find_duplicates(items)
    assert [int(x) for x in result] == expected
    assert Tracked.comparisons <= 10 * len(items), (
        f"Сравнений: {Tracked.comparisons}. Подсказка: если для каждого элемента проходить весь "
        "список, при росте ×100 время вырастет в ×10 000 раз. Нужна структура, которая помнит, "
        "сколько раз встретилось число."
    )


# ---------- Задание 5: декомпозиция ----------

LINES_CASES = [
    ["A1;100.5;2", "B2;50;1"],
    ["A1;100.5;2", "bad", "B2;x;1", "C3;10;0", ";5;5", "D4;-1;1", "E5;2.5;4"],
    [],
    ["  A1 ; 10 ; 3  "],
    ["A1;10;2.5", "A1;10;2;extra"],
]


def test_parse_order(target: ModuleType) -> None:
    assert target.parse_order("A1; 100.5 ;2") == {"id": "A1", "price": 100.5, "qty": 2}


@pytest.mark.parametrize("raw", ["A1;100", "A1;x;2", "A1;1;2.5", "", "a;b;c;d"])
def test_parse_order_rejects_bad_lines(target: ModuleType, raw: str) -> None:
    with pytest.raises(ValueError):
        target.parse_order(raw)


@pytest.mark.parametrize(
    ("order", "expected"),
    [
        ({"id": "A", "price": 10.0, "qty": 1}, True),
        ({"id": "", "price": 10.0, "qty": 1}, False),
        ({"id": "A", "price": 0.0, "qty": 1}, False),
        ({"id": "A", "price": -5.0, "qty": 1}, False),
        ({"id": "A", "price": 10.0, "qty": 0}, False),
    ],
    ids=["верный", "пустой id", "нулевая цена", "отрицательная цена", "нулевое количество"],
)
def test_is_valid(target: ModuleType, order: dict[str, Any], expected: bool) -> None:
    assert target.is_valid(order) is expected


def test_order_total(target: ModuleType) -> None:
    assert target.order_total({"id": "A", "price": 2.5, "qty": 4}) == pytest.approx(10.0)


@pytest.mark.parametrize("lines", LINES_CASES, ids=[f"случай {i}" for i in range(5)])
def test_process_orders_matches_legacy(target: ModuleType, lines: list[str]) -> None:
    assert target.process_orders(lines) == target.process_orders_legacy(lines), (
        "Поведение изменилось: результат отличается от исходной функции"
    )


def test_process_orders_is_built_from_parts(target: ModuleType) -> None:
    target.process_orders([])  # убедиться, что функция написана
    source = textwrap.dedent(inspect.getsource(target.process_orders))
    called = {
        node.func.id
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    missing = {"parse_order", "is_valid", "order_total"} - called
    assert not missing, f"process_orders должна использовать части: не вызваны {sorted(missing)}"


# ---------- Задание 6: системное мышление ----------

SOURCE = """
def load():
    return 1

def parse():
    return load()

def report():
    return parse()

def main():
    report()
    print("done")
"""

CYCLE = """
def a():
    return b()

def b():
    return a()
"""

METHODS = """
class Repo:
    def load(self):
        return 1

    def first(self):
        return self.load()

def use(repo):
    return repo.first()
"""


@pytest.mark.parametrize(
    ("source", "name", "transitive", "expected"),
    [
        (SOURCE, "load", False, ["parse"]),
        (SOURCE, "load", True, ["main", "parse", "report"]),
        (SOURCE, "parse", False, ["report"]),
        (SOURCE, "main", True, []),
        (SOURCE, "unknown", True, []),
        (CYCLE, "a", False, ["b"]),
        (CYCLE, "a", True, ["b"]),
        ("def f():\n    return f()\n", "f", True, []),
        (METHODS, "load", False, ["first"]),
        (METHODS, "load", True, ["first", "use"]),
        ("", "x", True, []),
    ],
    ids=[
        "прямые",
        "цепочкой",
        "второй уровень",
        "никто не вызывает",
        "неизвестная",
        "цикл прямой",
        "цикл цепочкой",
        "рекурсия",
        "методы",
        "методы цепочкой",
        "пустой текст",
    ],
)
def test_find_dependents(
    target: ModuleType, source: str, name: str, transitive: bool, expected: list[str]
) -> None:
    assert target.find_dependents(source, name, transitive) == expected
