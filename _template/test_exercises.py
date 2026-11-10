"""Проверка модуля N. Фикстура `target` подставляет exercises.py или эталон."""

from __future__ import annotations

from types import ModuleType

import pytest


@pytest.mark.parametrize(("value", "expected"), [(1, 1), (0, 0)], ids=["единица", "ноль"])
def test_function_name(target: ModuleType, value: int, expected: int) -> None:
    assert target.function_name(value) == expected, "подсказка: что вернуть для такого входа?"
