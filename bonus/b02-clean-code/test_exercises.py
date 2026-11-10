"""Проверка бонус-модуля b02. Запуск: pytest bonus/b02-clean-code"""

from __future__ import annotations

import ast
import dataclasses
import inspect
import textwrap
from types import ModuleType

import pytest

# ---------- Задание 1: @dataclass ----------


@pytest.mark.refactor
def test_student_is_a_dataclass(target: ModuleType) -> None:
    """Рефакторинг: засчитывается, когда класс стал dataclass и ничего не сломалось."""
    student = target.Student
    assert dataclasses.is_dataclass(student), "Поставьте над классом декоратор @dataclass"
    assert "def __init__" not in inspect.getsource(student), (
        "__init__ писать вручную не нужно: его создаст @dataclass"
    )
    assert [f.name for f in dataclasses.fields(student)] == ["name", "course", "grades"]

    anna = student("Аня", 3)
    assert anna.grades == []
    boris = student("Борис", 1)
    assert anna.grades is not boris.grades, "У каждого студента свой список (default_factory=list)"
    assert repr(student("Аня", 3, [5])) == "Student(name='Аня', course=3, grades=[5])"
    assert student("Аня", 3, [5]) == student("Аня", 3, [5])
    assert student("Аня", 3, [5]) != student("Аня", 3, [4])
    assert student("Аня", 3, [5, 4, 3]).average() == 4.0
    assert student("Аня", 3).average() == 0.0


# ---------- Задание 2: @property ----------


def test_temperature_fahrenheit(target: ModuleType) -> None:
    assert target.Temperature(100).fahrenheit == pytest.approx(212)
    assert target.Temperature(0).fahrenheit == pytest.approx(32)
    assert target.Temperature(-40).fahrenheit == pytest.approx(-40)


def test_temperature_set_fahrenheit_updates_celsius(target: ModuleType) -> None:
    temperature = target.Temperature(0)
    temperature.fahrenheit = 212
    assert temperature.celsius == pytest.approx(100)


def test_temperature_rejects_below_absolute_zero(target: ModuleType) -> None:
    with pytest.raises(ValueError):
        target.Temperature(-300)


def test_temperature_setter_validates_and_keeps_old_value(target: ModuleType) -> None:
    temperature = target.Temperature(20)
    with pytest.raises(ValueError):
        temperature.celsius = -274
    assert temperature.celsius == 20, "Неверное значение не должно портить старое"


def test_temperature_uses_properties(target: ModuleType) -> None:
    target.Temperature(1)  # убедиться, что класс написан
    assert isinstance(vars(target.Temperature).get("celsius"), property)
    assert isinstance(vars(target.Temperature).get("fahrenheit"), property)


# ---------- Задание 3: мини-линтер ----------


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        (
            "def add(a, b):\n    return a + b\n",
            [
                "add: нет типа у аргумента a",
                "add: нет типа у аргумента b",
                "add: нет типа результата",
                "add: нет docstring",
            ],
        ),
        ('def add(a: int, b: int) -> int:\n    """Сумма."""\n    return a + b\n', []),
        (
            'class C:\n    def m(self, x: int):\n        """Док."""\n        return x\n',
            ["m: нет типа результата"],
        ),
        (
            'class C:\n    @classmethod\n    def make(cls, x: int) -> "C":\n        return cls()\n',
            ["make: нет docstring"],
        ),
        (
            'def f(*args, key=1) -> None:\n    """Док."""\n',
            ["f: нет типа у аргумента args", "f: нет типа у аргумента key"],
        ),
        (
            'def f(a: int, /, b: int, *, c, **extra) -> None:\n    """Док."""\n',
            ["f: нет типа у аргумента c", "f: нет типа у аргумента extra"],
        ),
        (
            "def first() -> None:\n    pass\n\n\nasync def second(x):\n    pass\n",
            [
                "first: нет docstring",
                "second: нет типа у аргумента x",
                "second: нет типа результата",
                "second: нет docstring",
            ],
        ),
        ("x = 1\n", []),
        ("", []),
    ],
    ids=[
        "всё плохо",
        "всё хорошо",
        "метод без результата",
        "classmethod",
        "args и kwonly",
        "positional-only и kwargs",
        "порядок и async",
        "нет функций",
        "пустой текст",
    ],
)
def test_find_style_problems(target: ModuleType, source: str, expected: list[str]) -> None:
    assert target.find_style_problems(source) == expected


def test_find_style_problems_syntax_error(target: ModuleType) -> None:
    with pytest.raises(SyntaxError):
        target.find_style_problems("def broken(:\n")


# ---------- Задание 4: рефакторинг ----------

_TARIFFS = {"RU": (100.0, 30.0, 20.0), "BY": (150.0, 45.0, 30.0), "KZ": (200.0, 60.0, 40.0)}


def _expected_cost(weight: float, country: str) -> float:
    base, mid, high = _TARIFFS[country]
    if weight <= 1:
        return base
    if weight <= 5:
        return base + (weight - 1) * mid
    return base + 4 * mid + (weight - 5) * high


def _count_ifs(function: object) -> int:
    source = textwrap.dedent(inspect.getsource(function))  # type: ignore[arg-type]
    return sum(isinstance(node, ast.If) for node in ast.walk(ast.parse(source)))


@pytest.mark.refactor
def test_shipping_cost_is_refactored_and_still_correct(target: ModuleType) -> None:
    """Задание-рефакторинг: меньше условий и то же поведение."""
    ifs = _count_ifs(target.shipping_cost)
    assert ifs <= 2, (
        f"В функции {ifs} условий if, нужно не больше 2. Подсказка: вынесите тарифы по странам "
        "в словарь и считайте по одной формуле."
    )
    for country in _TARIFFS:
        for weight in [0.0, 0.5, 1, 2, 3.5, 5, 5.5, 8, 10, 25]:
            got = target.shipping_cost(weight, country)
            assert got == pytest.approx(_expected_cost(weight, country)), (
                f"Поведение изменилось: shipping_cost({weight}, {country!r}) = {got}, "
                f"раньше было {_expected_cost(weight, country)}"
            )
    with pytest.raises(ValueError):
        target.shipping_cost(1, "XX")


# ---------- Задание 5: три ловушки ----------


@pytest.mark.bugfix
def test_trap_mutable_default(target: ModuleType) -> None:
    assert target.add_tag("a") == ["a"]
    assert target.add_tag("b") == ["b"], (
        "Второй вызов запомнил тег из первого. Подсказка: значение по умолчанию [] создаётся "
        "один раз при определении функции. Используйте None."
    )
    mine = ["x"]
    assert target.add_tag("y", mine) == ["x", "y"]


@pytest.mark.bugfix
def test_trap_shared_rows(target: ModuleType) -> None:
    grid = target.make_grid(2, 3)
    grid[0][0] = 1
    assert grid == [[1, 0, 0], [0, 0, 0]], (
        "Изменилась не только первая строка. Подсказка: [[0] * 3] * 2 — это одна и та же "
        "строка, повторённая дважды."
    )


@pytest.mark.bugfix
def test_trap_empty_average(target: ModuleType) -> None:
    assert target.average([2, 4]) == 3.0
    assert target.average([]) == 0.0, "Для пустого списка должно быть 0.0, а не ZeroDivisionError"


# ---------- Задание 6: формат коммита ----------


@pytest.mark.parametrize(
    "message",
    [
        "feat: add login",
        "fix(parser): handle empty input",
        "docs: update README",
        "feat(api)!: remove v1 endpoint",
        "chore(deps): bump actions/checkout from 4 to 7",
        "refactor(m03-stack): simplify peek",
        "fix: handle timeout\n\nThe request hung when the server did not answer.",
    ],
)
def test_valid_commit_messages(target: ModuleType, message: str) -> None:
    assert target.is_valid_commit_message(message) is True, f"Должно быть верным: {message!r}"


@pytest.mark.parametrize(
    "message",
    [
        "",
        "Added login",
        "feat add login",
        "feat:add login",
        "feature: add login",
        "FEAT: add login",
        "fix: ",
        "fix:  extra space",
        "fix: trailing dot.",
        "feat(): empty scope",
        "feat(Parser): uppercase scope",
        "fix: bug\nno blank line before body",
        "feat: " + "x" * 80,
    ],
    ids=[
        "пустое",
        "без типа",
        "без двоеточия",
        "без пробела",
        "неизвестный тип",
        "заглавный тип",
        "пустое описание",
        "лишний пробел",
        "точка в конце",
        "пустая область",
        "заглавная область",
        "тело без пустой строки",
        "слишком длинное",
    ],
)
def test_invalid_commit_messages(target: ModuleType, message: str) -> None:
    assert target.is_valid_commit_message(message) is False, f"Должно быть неверным: {message!r}"
