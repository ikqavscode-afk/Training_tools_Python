"""Собирает таблицу прогресса: сколько заданий выполнено в каждом модуле.

Запуск: ``python tools/progress.py``. В GitHub Actions таблица пишется в Summary.
Основная программа и бонус-уровни показываются отдельными разделами.
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
BONUS_PREFIX = "bonus/"


def module_key(nodeid: str) -> str:
    """Ключ модуля по пути теста: ``m01-search`` или ``bonus/b01-name``."""
    parts = nodeid.split("/")
    return "/".join(parts[:2]) if parts[0] == "bonus" and len(parts) > 1 else parts[0]


class Collector:
    def __init__(self) -> None:
        self.stats: dict[str, dict[str, int]] = defaultdict(
            lambda: {"passed": 0, "skipped": 0, "failed": 0}
        )

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.when == "call" or (report.when == "setup" and report.skipped):
            self.stats[module_key(report.nodeid)][report.outcome] += 1


def render_table(stats: dict[str, dict[str, int]], keys: list[str]) -> str:
    lines = [
        "| Модуль | Выполнено | Не сделано | Падает |",
        "|---|---|---|---|",
    ]
    for key in keys:
        s = stats[key]
        total = s["passed"] + s["skipped"] + s["failed"]
        lines.append(f"| {key} | {s['passed']} / {total} | {s['skipped']} | {s['failed']} |")
    return "\n".join(lines)


def render(stats: dict[str, dict[str, int]]) -> str:
    main_keys = sorted(k for k in stats if not k.startswith(BONUS_PREFIX))
    bonus_keys = sorted(k for k in stats if k.startswith(BONUS_PREFIX))
    sections = ["### Основная программа", render_table(stats, main_keys)]
    if bonus_keys:
        sections += ["", "### 🚀 Бонус-уровни", render_table(stats, bonus_keys)]
    return "\n".join(sections)


def main() -> int:
    collector = Collector()
    os.chdir(ROOT)
    pytest.main(["-q", "--no-header", "-p", "no:cacheprovider"], plugins=[collector])
    table = render(collector.stats)
    print("\n" + table)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write("## Мой прогресс\n\n" + table + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
