"""Общие настройки проверки заданий.

Переменная окружения ``PRACTICUM_TARGET`` выбирает, что проверяют тесты:

* ``exercises`` (по умолчанию) — ваш файл ``exercises.py``;
* ``solutions`` — готовое решение из папки ``solutions/`` (для CI автора).

Если в заготовке остался ``raise NotImplementedError``, тест получает статус
«ещё не сделано» (skip), а не красное падение.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

TARGET = os.environ.get("PRACTICUM_TARGET", "exercises")
if TARGET not in {"exercises", "solutions"}:
    raise pytest.UsageError("PRACTICUM_TARGET должен быть 'exercises' или 'solutions'")


def _load(path: Path) -> ModuleType:
    """Загрузить модуль по пути к файлу (папки с дефисом нельзя импортировать обычным способом)."""
    name = f"practicum_{TARGET}_{path.parent.name}_{path.stem}".replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Не удалось загрузить {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def target(request: pytest.FixtureRequest) -> ModuleType:
    """Модуль с вашими функциями (или с эталоном, если TARGET=solutions)."""
    module_dir: Path = request.path.parent
    if TARGET == "solutions":
        path = module_dir / "solutions" / f"{module_dir.name.replace('-', '_')}.py"
    else:
        path = module_dir / "exercises.py"
    return _load(path)


class CountingList(list[int]):
    """Список, который считает обращения к элементам (для проверки эффективности)."""

    accesses: int

    def __init__(self, items: Any = ()) -> None:
        super().__init__(items)
        self.accesses = 0

    def __getitem__(self, index: Any) -> Any:
        self.accesses += 1
        return super().__getitem__(index)

    def __iter__(self) -> Any:
        for i in range(len(self)):
            yield self[i]


@pytest.fixture
def counting_list() -> Callable[[Any], CountingList]:
    return CountingList


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]) -> Any:
    outcome = yield
    report = outcome.get_result()
    if call.when != "call" or call.excinfo is None:
        return
    reason: str | None = None
    if call.excinfo.errisinstance(NotImplementedError):
        reason = "ещё не сделано"
    elif TARGET == "exercises" and item.get_closest_marker("bugfix"):
        reason = "ошибка ещё не исправлена"
    if reason:
        report.outcome = "skipped"
        report.longrepr = (str(item.path), item.location[1] or 0, reason)
