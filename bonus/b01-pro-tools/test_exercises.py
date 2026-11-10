"""Проверка бонус-модуля b01. Запуск: pytest bonus/b01-pro-tools"""

from __future__ import annotations

import inspect
import random
import time
from collections.abc import Callable
from types import ModuleType
from typing import Any

import pytest

# ---------- Задание 1: @timer ----------


def test_timer_returns_result_with_args(target: ModuleType) -> None:
    @target.timer
    def add(a: int, b: int = 0) -> int:
        return a + b

    assert add(2, b=3) == 5


def test_timer_keeps_function_name_and_doc(target: ModuleType) -> None:
    @target.timer
    def greet() -> str:
        """Говорит привет."""
        return "hi"

    assert greet.__name__ == "greet", "Подсказка: functools.wraps сохраняет имя функции"
    assert greet.__doc__ == "Говорит привет."


def test_timer_records_last_time(target: ModuleType) -> None:
    @target.timer
    def slow() -> None:
        time.sleep(0.02)

    slow()
    assert slow.last_time >= 0.015, "last_time должен хранить секунды последнего вызова"
    assert slow.last_time < 1.0


def test_timer_updates_on_every_call(target: ModuleType) -> None:
    @target.timer
    def maybe_slow(pause: float) -> None:
        time.sleep(pause)

    maybe_slow(0.03)
    first = maybe_slow.last_time
    maybe_slow(0.0)
    assert maybe_slow.last_time < first, "last_time хранит время ПОСЛЕДНЕГО вызова"


def test_timer_records_time_even_if_function_raises(target: ModuleType) -> None:
    @target.timer
    def broken() -> None:
        time.sleep(0.01)
        raise ValueError("ошибка")

    with pytest.raises(ValueError):
        broken()
    assert broken.last_time >= 0.005


# ---------- Задание 2: Timer ----------


def test_timer_context_measures_block(target: ModuleType) -> None:
    with target.Timer() as t:
        time.sleep(0.02)
    assert t.elapsed >= 0.015
    assert t.elapsed < 1.0


def test_timer_context_returns_itself(target: ModuleType) -> None:
    timer = target.Timer()
    with timer as entered:
        pass
    assert entered is timer


def test_timer_context_does_not_swallow_exceptions(target: ModuleType) -> None:
    timer = target.Timer()
    with pytest.raises(ValueError):
        with timer:
            time.sleep(0.01)
            raise ValueError("ошибка внутри with")
    assert timer.elapsed >= 0.005, "elapsed нужно записать и при исключении"


# ---------- Задание 3: генератор ----------


def make_tree(target: ModuleType) -> Any:
    """Дерево:    4
                 / \\
                2   6
               / \\ / \\
              1  3 5  7
    """
    nodes = {v: target.Node(v) for v in range(1, 8)}
    nodes[4].left, nodes[4].right = nodes[2], nodes[6]
    nodes[2].left, nodes[2].right = nodes[1], nodes[3]
    nodes[6].left, nodes[6].right = nodes[5], nodes[7]
    return nodes[4]


def test_inorder_iter_gives_sorted_values(target: ModuleType) -> None:
    assert list(target.inorder_iter(make_tree(target))) == [1, 2, 3, 4, 5, 6, 7]


def test_inorder_iter_empty_tree(target: ModuleType) -> None:
    assert list(target.inorder_iter(None)) == []


def test_inorder_iter_is_a_generator(target: ModuleType) -> None:
    list(target.inorder_iter(make_tree(target)))  # сначала убеждаемся, что функция написана
    assert inspect.isgeneratorfunction(target.inorder_iter), "Нужен yield: это генератор"


def test_inorder_iter_is_lazy(target: ModuleType) -> None:
    """Первое значение должно отдаваться, пока правое поддерево ещё не тронуто."""

    class Trap(target.Node):  # type: ignore[name-defined, misc]
        @property
        def right(self) -> Any:
            raise AssertionError("правый потомок прочитан слишком рано")

        @right.setter
        def right(self, value: Any) -> None:
            pass

    root = target.Node(2)
    root.left = Trap(1)
    generator = target.inorder_iter(root)
    try:
        first = next(generator)
    except AssertionError:
        pytest.fail("Не собирайте все значения заранее: генератор должен отдавать их по одному")
    assert first == 1


# ---------- Задание 4: lru_cache ----------


def test_fibonacci_cached_small_values(target: ModuleType) -> None:
    results = [target.fibonacci_cached(n) for n in range(0, 11)]
    assert results == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]


def test_fibonacci_cached_is_fast(target: ModuleType) -> None:
    target.fibonacci_cached(1)  # убедиться, что функция написана
    assert hasattr(target.fibonacci_cached, "cache_info"), (
        "Нужен декоратор @lru_cache(maxsize=None) (или короткий @cache) над fibonacci_cached"
    )
    start = time.perf_counter()
    assert target.fibonacci_cached(80) == 23416728348467685
    assert time.perf_counter() - start < 1.0
    assert target.fibonacci_cached.cache_info().hits > 0


# ---------- Задание 5а: bisect ----------


@pytest.mark.parametrize(
    ("values", "low", "high", "expected"),
    [
        ([1, 3, 5, 7, 9], 3, 7, 3),
        ([1, 3, 5, 7, 9], 4, 6, 1),
        ([1, 3, 5, 7, 9], 10, 20, 0),
        ([1, 3, 5, 7, 9], 0, 100, 5),
        ([1, 3, 5, 7, 9], 7, 3, 0),
        ([2, 2, 2, 3], 2, 2, 3),
        ([], 1, 5, 0),
    ],
    ids=["включая границы", "между", "правее всех", "все", "low > high", "дубликаты", "пустой"],
)
def test_count_in_range(
    target: ModuleType, values: list[int], low: int, high: int, expected: int
) -> None:
    assert target.count_in_range(values, low, high) == expected


def test_count_in_range_is_fast(target: ModuleType, counting_list: Callable[[Any], Any]) -> None:
    """Не больше ~40 обращений к списку из 100 000 чисел: перебор тут не подойдёт."""
    data = counting_list(range(100_000))
    assert target.count_in_range(data, 10, 99_990) == 99_981
    assert data.accesses <= 40, (
        f"Обращений к списку: {data.accesses}. Подсказка: список отсортирован, "
        "значит, границы отрезка можно найти бинарным поиском."
    )


# ---------- Задание 5б: heapq ----------


class Tracked(int):
    """Число, которое считает, сколько раз его сравнили."""

    comparisons = 0

    def __lt__(self, other: Any) -> bool:
        Tracked.comparisons += 1
        return int(self) < int(other)

    def __gt__(self, other: Any) -> bool:
        Tracked.comparisons += 1
        return int(self) > int(other)


@pytest.mark.parametrize(
    ("items", "k", "expected"),
    [
        ([5, 1, 4, 2, 3], 3, [1, 2, 3]),
        ([5, 1, 4, 2, 3], 0, []),
        ([5, 1, 4, 2, 3], -2, []),
        ([5, 1, 4, 2, 3], 10, [1, 2, 3, 4, 5]),
        ([], 3, []),
        ([2, 2, 1], 2, [1, 2]),
    ],
    ids=["три", "ноль", "отрицательное k", "k больше длины", "пустой", "дубликаты"],
)
def test_k_smallest(target: ModuleType, items: list[int], k: int, expected: list[int]) -> None:
    assert target.k_smallest(items, k) == expected


def test_k_smallest_does_not_change_input(target: ModuleType) -> None:
    data = [3, 1, 2]
    target.k_smallest(data, 2)
    assert data == [3, 1, 2]


def test_k_smallest_does_not_sort_everything(target: ModuleType) -> None:
    """Полная сортировка 2000 чисел — около 20 000 сравнений; куча для k=5 — около 2 000."""
    rng = random.Random(1)
    items = [Tracked(rng.randint(0, 10**6)) for _ in range(2000)]
    Tracked.comparisons = 0
    result = target.k_smallest(items, 5)
    assert [int(x) for x in result] == sorted(int(x) for x in items)[:5]
    assert Tracked.comparisons <= 3 * len(items), (
        f"Сравнений: {Tracked.comparisons}. Подсказка: для небольшого k не нужно "
        "сортировать весь список — посмотрите на модуль heapq."
    )
