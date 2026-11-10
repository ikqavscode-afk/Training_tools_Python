"""Бонус b02 · Качество кода. Допишите код и запустите: pytest bonus/b02-clean-code"""

from __future__ import annotations


# ---------- Задание 1 🛠: @dataclass ----------
class Student:
    """Задание 1 🛠. Перепишите класс через @dataclass: код станет в разы короче.

    Что должно остаться: поля name, course, grades (по умолчанию пустой список, свой у каждого
    студента), красивый repr, сравнение по значению и метод average(). Руками __init__,
    __repr__ и __eq__ писать не нужно.
    """

    def __init__(self, name: str, course: int, grades: list[int] | None = None) -> None:
        self.name = name
        self.course = course
        self.grades = grades if grades is not None else []

    def __repr__(self) -> str:
        return f"Student(name={self.name!r}, course={self.course!r}, grades={self.grades!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return (self.name, self.course, self.grades) == (other.name, other.course, other.grades)

    def average(self) -> float:
        """Средний балл; для пустого списка оценок — 0.0."""
        return sum(self.grades) / len(self.grades) if self.grades else 0.0


# ---------- Задание 2 🛠: @property ----------
class Temperature:
    """Задание 2 🛠. Температура в градусах Цельсия с проверкой и пересчётом в Фаренгейты.

    * Temperature(celsius): значение хранится в «защищённом» поле.
    * celsius — свойство: нельзя ниже -273.15 (абсолютный нуль), иначе ValueError
      (и при создании, и при присваивании позже).
    * fahrenheit — свойство: читается как C * 9 / 5 + 32; при присваивании пересчитывает celsius.
    """

    def __init__(self, celsius: float) -> None:
        # TODO: присвойте self.celsius = celsius (пусть сработает сеттер) и объявите свойства
        raise NotImplementedError


# ---------- Задание 3 🛠: мини-линтер ----------
def find_style_problems(source: str) -> list[str]:
    """Задание 3 🛠. Мини-линтер: найти функции без type hints и docstring.

    Разберите текст программы модулем ast и для каждой функции (def и async def, в том числе
    методы) в порядке появления в тексте верните сообщения такого вида:
      "имя: нет типа у аргумента x"   (по каждому аргументу; self и cls пропускаем)
      "имя: нет типа результата"
      "имя: нет docstring"
    Порядок аргументов: позиционные, обычные, *args, только именованные, **kwargs.
    При синтаксической ошибке в source пусть ast сам выбросит SyntaxError.
    """
    # TODO: ast.parse, ast.walk, проверки node.args, node.returns, ast.get_docstring
    raise NotImplementedError


# ---------- Задание 4 🧠: рефакторинг ----------
def shipping_cost(weight: float, country: str) -> float:
    """Задание 4 🧠. Стоимость доставки. ПЕРЕПИШИТЕ, НЕ МЕНЯЯ ПОВЕДЕНИЕ.

    Сейчас код дублируется по странам (нарушен принцип DRY) и перегружен условиями (KISS).
    Цель: вынести тарифы в таблицу и оставить в функции не больше двух условий if.
    Измерьте себя: результат для любых веса и страны должен остаться прежним.
    """
    if country == "RU":
        if weight <= 1:
            return 100.0
        elif weight <= 5:
            return 100.0 + (weight - 1) * 30.0
        else:
            return 100.0 + 4 * 30.0 + (weight - 5) * 20.0
    elif country == "BY":
        if weight <= 1:
            return 150.0
        elif weight <= 5:
            return 150.0 + (weight - 1) * 45.0
        else:
            return 150.0 + 4 * 45.0 + (weight - 5) * 30.0
    elif country == "KZ":
        if weight <= 1:
            return 200.0
        elif weight <= 5:
            return 200.0 + (weight - 1) * 60.0
        else:
            return 200.0 + 4 * 60.0 + (weight - 5) * 40.0
    else:
        raise ValueError("Неизвестная страна")


# ---------- Задание 5 🧠: три ловушки ----------
def add_tag(tag: str, tags: list[str] = []) -> list[str]:  # noqa: B006  (ловушка №1: так нельзя)
    """Ловушка 1. Добавляет тег в список и возвращает его. Каждый вызов должен быть независим."""
    tags.append(tag)
    return tags


def make_grid(rows: int, cols: int) -> list[list[int]]:
    """Ловушка 2. Таблица rows × cols из нулей. Строки должны быть независимыми."""
    return [[0] * cols] * rows


def average(numbers: list[float]) -> float:
    """Ловушка 3. Среднее арифметическое; для пустого списка должно быть 0.0."""
    return sum(numbers) / len(numbers)


# ---------- Задание 6 🛠: формат сообщения коммита ----------
def is_valid_commit_message(message: str) -> bool:
    """Задание 6 🛠. Проверка сообщения по Conventional Commits.

    Первая строка: ``тип(область): описание``, где
      * тип — один из feat, fix, docs, style, refactor, perf, test, chore, build, ci;
      * область в скобках необязательна, строчные латинские буквы, цифры и дефис, не пустая;
      * после типа/области возможен знак ``!`` (ломающее изменение);
      * затем двоеточие, пробел и непустое описание без точки в конце;
      * вся первая строка — не длиннее 72 символов.
    Если есть тело сообщения, оно отделено от первой строки пустой строкой.
    """
    # TODO: регулярное выражение (модуль re) для первой строки и проверка пустой второй строки
    raise NotImplementedError
