"""Проверка модуля 6. Запуск: pytest m06-hash-tables"""

from __future__ import annotations

from types import ModuleType

import pytest

FRUITS = [
    ("apple", 10),
    ("banana", 20),
    ("cherry", 30),
    ("strawberry", 40),
    ("berry", 50),
    ("kerry", 60),
    ("marry", 70),
    ("derry", 80),
    ("kiwi", 90),
    ("lemon", 100),
]


@pytest.mark.parametrize(
    ("text", "expected"),
    [("", 0), ("a", 97), ("abc", 294), ("cba", 294), ("hello", 532), ("Python", 642)],
    ids=["пустая", "один символ", "abc", "cba (анаграмма)", "hello", "Python"],
)
def test_string_hash(target: ModuleType, text: str, expected: int) -> None:
    assert target.string_hash(text) == expected


@pytest.mark.parametrize(
    ("keys", "capacity", "expected"),
    [
        (["abc", "cba", "ab"], 5, {4: ["abc", "cba"]}),
        (["a", "b", "c"], 100, {}),
        ([], 5, {}),
        (["abc", "cba", "bca"], 7, {0: ["abc", "cba", "bca"]}),
        (["ab", "ba", "abc", "cba"], 5, {0: ["ab", "ba"], 4: ["abc", "cba"]}),
    ],
    ids=["одна коллизия", "нет коллизий", "нет ключей", "три в одной", "две корзины"],
)
def test_find_collisions(
    target: ModuleType, keys: list[str], capacity: int, expected: dict[int, list[str]]
) -> None:
    assert target.find_collisions(keys, capacity) == expected


def test_new_table_is_empty(target: ModuleType) -> None:
    table = target.HashTable(capacity=5)
    assert table.size == 0
    assert table.capacity == 5
    assert len(table.table) == 5


def test_insert_and_search(target: ModuleType) -> None:
    table = target.HashTable()
    table.insert("apple", 100)
    table.insert("banana", 200)
    assert table.search("apple") == 100
    assert table.search("banana") == 200
    assert table.size == 2


def test_search_missing_returns_none(target: ModuleType) -> None:
    table = target.HashTable()
    table.insert("apple", 1)
    assert table.search("grape") is None


def test_insert_same_key_updates_value(target: ModuleType) -> None:
    table = target.HashTable()
    table.insert("apple", 1)
    table.insert("apple", 2)
    assert table.search("apple") == 2
    assert table.size == 1, "Обновление значения не должно увеличивать size"


def test_collided_keys_are_both_found(target: ModuleType) -> None:
    """«abc» и «cba» дают один хэш: они в одной корзине, но оба находятся."""
    table = target.HashTable(capacity=5)
    table.insert("abc", 1)
    table.insert("cba", 2)
    assert table.search("abc") == 1
    assert table.search("cba") == 2
    assert table.size == 2


def test_delete_existing(target: ModuleType) -> None:
    table = target.HashTable()
    table.insert("apple", 1)
    table.insert("banana", 2)
    assert table.delete("apple") is True
    assert table.search("apple") is None
    assert table.search("banana") == 2
    assert table.size == 1


def test_delete_missing(target: ModuleType) -> None:
    table = target.HashTable()
    table.insert("apple", 1)
    assert table.delete("grape") is False
    assert table.size == 1


def test_delete_one_of_collided_keys(target: ModuleType) -> None:
    table = target.HashTable(capacity=5)
    table.insert("abc", 1)
    table.insert("cba", 2)
    assert table.delete("abc") is True
    assert table.search("cba") == 2


def test_resize_doubles_capacity_and_keeps_data(target: ModuleType) -> None:
    table = target.HashTable(capacity=5)
    for key, value in FRUITS:
        table.insert(key, value)
    table.resize()
    assert table.capacity == 10
    assert len(table.table) == 10
    assert table.size == len(FRUITS), "После resize size должен остаться прежним"
    for key, value in FRUITS:
        assert table.search(key) == value, f"После resize пропал ключ «{key}»"


@pytest.mark.bugfix
def test_put(target: ModuleType) -> None:
    """Задание «найди ошибку»: засчитывается, только когда верны ВСЕ случаи."""
    buckets: list[list[tuple[str, int]]] = [[] for _ in range(3)]
    target.put(buckets, "ab", 1)
    target.put(buckets, "xyz", 2)
    target.put(buckets, "ab", 3)
    entries = [pair for bucket in buckets for pair in bucket]
    assert sorted(entries) == [("ab", 3), ("xyz", 2)], (
        f"Хранится {entries}. Подсказка: ключ должен встречаться один раз, а значение — новое. "
        "Что происходит после обновления найденной пары?"
    )
