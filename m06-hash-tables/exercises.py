"""Модуль 6 · Хэш-таблицы. Допишите код и запустите: pytest m06-hash-tables"""

from __future__ import annotations

from typing import Any


def string_hash(text: str) -> int:
    """Задание 1. Хэш строки — сумма кодов её символов (функция ord).

    Примеры: "" -> 0, "a" -> 97, "abc" -> 97 + 98 + 99 = 294.
    """
    # TODO: пройдите по символам и сложите ord(символ)
    raise NotImplementedError


def find_collisions(keys: list[str], capacity: int) -> dict[int, list[str]]:
    """Задание 2. Найдите коллизии: ключи, попавшие в одну корзину.

    Номер корзины: string_hash(key) % capacity. Верните словарь
    {номер корзины: [ключи в порядке появления]} ТОЛЬКО для корзин с двумя и более ключами.
    """
    # TODO: разложите ключи по корзинам, затем оставьте корзины, где ключей больше одного
    raise NotImplementedError


class HashTable:
    """Задание 3–4. Хэш-таблица с цепочками: в каждой корзине список пар (ключ, значение)."""

    def __init__(self, capacity: int = 5) -> None:
        # TODO: capacity, size (сколько пар), table — список из capacity пустых списков
        raise NotImplementedError

    def _index(self, key: str) -> int:
        """Номер корзины для ключа."""
        # TODO: используйте string_hash и остаток от деления на capacity
        raise NotImplementedError

    def insert(self, key: str, value: Any) -> None:
        """Задание 3. Добавить пару. Если ключ уже есть — обновить значение (size не растёт)."""
        raise NotImplementedError

    def search(self, key: str) -> Any:
        """Задание 3. Значение по ключу или None, если ключа нет."""
        raise NotImplementedError

    def delete(self, key: str) -> bool:
        """Задание 4. Удалить пару. True — удалили, False — такого ключа не было."""
        raise NotImplementedError

    def resize(self) -> None:
        """Задание 4. Увеличить capacity вдвое и разложить все пары по корзинам заново."""
        raise NotImplementedError


def put(buckets: list[list[tuple[str, int]]], key: str, value: int) -> None:
    """Задание 5 («найди ошибку»). Положить пару в корзины или обновить, если ключ уже есть.

    Для простоты номер корзины — длина ключа. Функция иногда хранит один ключ дважды.
    Найдите ошибку и исправьте её.
    """
    bucket = buckets[len(key) % len(buckets)]
    for i, (existing_key, _) in enumerate(bucket):
        if existing_key == key:
            bucket[i] = (key, value)
    bucket.append((key, value))
