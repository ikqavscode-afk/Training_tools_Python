"""Бонус b03 · Инженерное мышление. Допишите код, затем: pytest bonus/b03-engineering-thinking"""

from __future__ import annotations

from typing import Any


# ---------- Задание 1 🧠: выбери структуру данных ----------
def choose_structure(scenario: int) -> str:
    """Задание 1 🧠. Для каждого сценария из README (номера 1–6) выберите структуру данных.

    Верните одну из строк: "list", "dict", "set", "deque", "heapq".
    Подумайте, какая операция в сценарии самая частая и должна быть быстрой.
    """
    # TODO: верните выбор для каждого номера сценария
    raise NotImplementedError


# ---------- Задание 2 🧠: прочитай замеры ----------
def growth_factor(sizes: list[int], times: list[float]) -> float:
    """Задание 2а 🧠. Во сколько раз растёт время при удвоении размера данных (в среднем).

    sizes — размеры входа по возрастанию, times — замеры времени для них.
    Формула: (times[-1] / times[0]) ** (1 / log2(sizes[-1] / sizes[0])).
    Если замеров меньше двух или списки разной длины — ValueError.
    """
    raise NotImplementedError


def classify_growth(factor: float) -> str:
    """Задание 2б 🧠. По множителю роста при удвоении выберите сложность.

    Типичные множители: "O(1)" ≈ 1.0, "O(log n)" ≈ 1.1, "O(n)" = 2.0,
    "O(n log n)" ≈ 2.2, "O(n^2)" = 4.0. Верните ближайший класс по модулю разности.
    """
    raise NotImplementedError


# ---------- Задание 3 🧠: найди причину ----------
def average_speed(distance_km: float, time_text: str) -> float:
    """Средняя скорость км/ч: время задано строкой «ЧЧ:ММ». Уже готова, но «хрупкая»."""
    hours, minutes = time_text.split(":")
    total_hours = int(hours) + int(minutes) / 60
    return distance_km / total_hours


def find_breaking_inputs() -> list[str]:
    """Задание 3 🧠. Верните не меньше 3 РАЗНЫХ строк времени, на которых average_speed падает.

    Среди них должны быть сбои хотя бы двух разных видов (разные типы исключений).
    Работайте как исследователь: выдвиньте гипотезу, проверьте, сделайте вывод.
    """
    # TODO: проверьте average_speed(10, "...") на странных входных данных
    raise NotImplementedError


# ---------- Задание 4 🧠: что будет при росте ×100 ----------
def find_duplicates(items: list[int]) -> list[int]:
    """Задание 4 🧠. Числа, которые встречаются в списке больше одного раза (по возрастанию).

    Каждое число в ответе один раз. Решение должно выдерживать список в 100 раз длиннее:
    тест считает сравнения, и «для каждого элемента пройти весь список» не пройдёт.
    """
    # TODO: подумайте, какая структура данных помнит «сколько раз видели»
    raise NotImplementedError


# ---------- Задание 5 🛠: декомпозиция ----------
def process_orders_legacy(lines: list[str]) -> dict[str, float]:
    """Исходная «монолитная» функция. РАБОТАЕТ ВЕРНО, но делает всё сразу. Не меняйте её.

    Строка заказа: "id;цена;количество". Неверные строки пропускаются и считаются.
    """
    count = 0
    skipped = 0
    revenue = 0.0
    for raw in lines:
        parts = raw.split(";")
        if len(parts) != 3:
            skipped += 1
            continue
        order_id, price_text, qty_text = (part.strip() for part in parts)
        try:
            price = float(price_text)
            qty = int(qty_text)
        except ValueError:
            skipped += 1
            continue
        if not order_id or price <= 0 or qty <= 0:
            skipped += 1
            continue
        count += 1
        revenue += price * qty
    return {"orders": count, "skipped": skipped, "revenue": revenue}


def parse_order(raw: str) -> dict[str, Any]:
    """Задание 5а 🛠. Разобрать строку "id;цена;количество" в словарь.

    Результат: {"id": str, "price": float, "qty": int}, пробелы вокруг частей убираются.
    Если частей не три или числа записаны неверно — ValueError.
    """
    raise NotImplementedError


def is_valid(order: dict[str, Any]) -> bool:
    """Задание 5б 🛠. Заказ корректен: id не пустой, цена и количество больше нуля."""
    raise NotImplementedError


def order_total(order: dict[str, Any]) -> float:
    """Задание 5в 🛠. Сумма заказа: цена * количество."""
    raise NotImplementedError


def process_orders(lines: list[str]) -> dict[str, float]:
    """Задание 5г 🛠. То же, что process_orders_legacy, но собранное из частей выше.

    В теле должны вызываться parse_order, is_valid и order_total.
    """
    raise NotImplementedError


# ---------- Задание 6 🧠: системное мышление ----------
def find_dependents(source: str, name: str, transitive: bool = False) -> list[str]:
    """Задание 6 🧠. Анализ влияния: какие функции заденет изменение функции name?

    По тексту программы (модуль ast) верните отсортированный список функций, которые вызывают
    name напрямую. При transitive=True добавьте и тех, кто вызывает вызывающих (и так далее).
    Саму name в ответ не включайте. Вызовы вида obj.name() тоже считаются вызовами name.
    Учтите циклы вызовов: функция a вызывает b, а b вызывает a.
    """
    raise NotImplementedError
