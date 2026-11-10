"""Бонус b03 · Инженерное мышление. Эталонные решения (спойлеры!)."""

from __future__ import annotations

import ast
import math
from collections import Counter
from typing import Any

# ---------- Задание 1 ----------
_CHOICES = {
    1: "dict",  # по имени быстро найти номер: поиск по ключу
    2: "set",  # убрать повторы и быстро проверять «видели ли»
    3: "deque",  # очередь: снимаем с начала
    4: "heapq",  # всегда нужен минимум из потока
    5: "list",  # порядок важен, доступ по номеру
    6: "dict",  # счётчик «слово → сколько раз»
}


def choose_structure(scenario: int) -> str:
    """Структура данных для сценария из README."""
    return _CHOICES[scenario]


# ---------- Задание 2 ----------
_TYPICAL_FACTORS = {
    "O(1)": 1.0,
    "O(log n)": 1.1,
    "O(n)": 2.0,
    "O(n log n)": 2.2,
    "O(n^2)": 4.0,
}


def growth_factor(sizes: list[int], times: list[float]) -> float:
    """Средний множитель роста времени при удвоении размера."""
    if len(sizes) != len(times) or len(sizes) < 2:
        raise ValueError("Нужно не меньше двух замеров, и списков одной длины")
    doublings = math.log2(sizes[-1] / sizes[0])
    return float((times[-1] / times[0]) ** (1 / doublings))


def classify_growth(factor: float) -> str:
    """Ближайший по типичному множителю класс сложности."""
    return min(_TYPICAL_FACTORS, key=lambda name: abs(_TYPICAL_FACTORS[name] - factor))


# ---------- Задание 3 ----------
def average_speed(distance_km: float, time_text: str) -> float:
    """Средняя скорость км/ч: время задано строкой «ЧЧ:ММ»."""
    hours, minutes = time_text.split(":")
    total_hours = int(hours) + int(minutes) / 60
    return distance_km / total_hours


def find_breaking_inputs() -> list[str]:
    """Строки времени, на которых average_speed падает (разных видов)."""
    return [
        "0:00",  # деление на ноль
        "",  # нет двоеточия, нечего распаковать
        "1:30:15",  # слишком много частей
        "час:минута",  # не числа
    ]


# ---------- Задание 4 ----------
def find_duplicates(items: list[int]) -> list[int]:
    """Повторяющиеся числа по возрастанию: счётчик на словаре, один проход."""
    counts = Counter(items)
    return sorted(value for value, count in counts.items() if count > 1)


# ---------- Задание 5 ----------
def process_orders_legacy(lines: list[str]) -> dict[str, float]:
    """Исходная монолитная функция (не менять)."""
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
    """Строка "id;цена;количество" в словарь; ValueError при неверном формате."""
    parts = [part.strip() for part in raw.split(";")]
    if len(parts) != 3:
        raise ValueError("Нужно три части: id;цена;количество")
    order_id, price_text, qty_text = parts
    return {"id": order_id, "price": float(price_text), "qty": int(qty_text)}


def is_valid(order: dict[str, Any]) -> bool:
    """Заказ корректен: id не пустой, цена и количество положительные."""
    return bool(order["id"]) and order["price"] > 0 and order["qty"] > 0


def order_total(order: dict[str, Any]) -> float:
    """Сумма заказа."""
    return float(order["price"] * order["qty"])


def process_orders(lines: list[str]) -> dict[str, float]:
    """Те же результаты, что у legacy, но собрано из частей."""
    count = 0
    skipped = 0
    revenue = 0.0
    for raw in lines:
        try:
            order = parse_order(raw)
        except ValueError:
            skipped += 1
            continue
        if not is_valid(order):
            skipped += 1
            continue
        count += 1
        revenue += order_total(order)
    return {"orders": count, "skipped": skipped, "revenue": revenue}


# ---------- Задание 6 ----------
def _called_names(node: ast.AST) -> set[str]:
    names: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            func = child.func
            if isinstance(func, ast.Name):
                names.add(func.id)
            elif isinstance(func, ast.Attribute):
                names.add(func.attr)
    return names


def find_dependents(source: str, name: str, transitive: bool = False) -> list[str]:
    """Функции, которые вызывают name (напрямую или, при transitive, цепочкой)."""
    calls: dict[str, set[str]] = {}
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            calls.setdefault(node.name, set()).update(_called_names(node))
    found: set[str] = set()
    frontier = {name}
    while frontier:
        new = {
            func
            for func, called in calls.items()
            if called & frontier and func != name and func not in found
        }
        found |= new
        frontier = new if transitive else set()
    return sorted(found)
