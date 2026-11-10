"""Модуль 6 · Хэш-таблицы. Эталонные решения (спойлеры!)."""

from __future__ import annotations

from typing import Any


def string_hash(text: str) -> int:
    """Хэш строки — сумма кодов символов."""
    total = 0
    for char in text:
        total += ord(char)
    return total


def find_collisions(keys: list[str], capacity: int) -> dict[int, list[str]]:
    """Корзины, в которые попало два и более ключей."""
    buckets: dict[int, list[str]] = {}
    for key in keys:
        buckets.setdefault(string_hash(key) % capacity, []).append(key)
    return {index: group for index, group in buckets.items() if len(group) > 1}


class HashTable:
    """Хэш-таблица с цепочками."""

    def __init__(self, capacity: int = 5) -> None:
        self.capacity = capacity
        self.size = 0
        self.table: list[list[tuple[str, Any]]] = [[] for _ in range(capacity)]

    def _index(self, key: str) -> int:
        return string_hash(key) % self.capacity

    def insert(self, key: str, value: Any) -> None:
        """Добавить пару или обновить значение существующего ключа."""
        bucket = self.table[self._index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1

    def search(self, key: str) -> Any:
        """Значение по ключу или None."""
        for existing_key, value in self.table[self._index(key)]:
            if existing_key == key:
                return value
        return None

    def delete(self, key: str) -> bool:
        """Удалить пару; True, если она была."""
        bucket = self.table[self._index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                del bucket[i]
                self.size -= 1
                return True
        return False

    def resize(self) -> None:
        """Удвоить число корзин и пересчитать положение каждой пары."""
        old_table = self.table
        self.capacity *= 2
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)

    def __repr__(self) -> str:
        rows = [f"[{i}]: {bucket}" for i, bucket in enumerate(self.table) if bucket]
        return "HashTable(\n  " + "\n  ".join(rows) + "\n)" if rows else "HashTable(пустая)"


def put(buckets: list[list[tuple[str, int]]], key: str, value: int) -> None:
    """Положить пару или обновить (исправлено: после обновления нужен `return`)."""
    bucket = buckets[len(key) % len(buckets)]
    for i, (existing_key, _) in enumerate(bucket):
        if existing_key == key:
            bucket[i] = (key, value)
            return
    bucket.append((key, value))
