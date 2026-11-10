"""Собирает таблицу прогресса: сколько заданий выполнено в каждом модуле.

Запуск: ``python tools/progress.py``. В GitHub Actions таблица пишется в Summary.
"""

from __future__ import annotations

import os
import sys
from collections import defaultdict
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


class Collector:
    def __init__(self) -> None:
        self.stats: dict[str, dict[str, int]] = defaultdict(
            lambda: {"passed": 0, "skipped": 0, "failed": 0}
        )

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        module = report.nodeid.split("/")[0]
        if report.when == "call" or (report.when == "setup" and report.skipped):
            self.stats[module][report.outcome] += 1


def render(stats: dict[str, dict[str, int]]) -> str:
    lines = [
        "| Модуль | Выполнено | Не сделано | Падает |",
        "|---|---|---|---|",
    ]
    for module in sorted(stats):
        s = stats[module]
        total = s["passed"] + s["skipped"] + s["failed"]
        lines.append(f"| {module} | {s['passed']} / {total} | {s['skipped']} | {s['failed']} |")
    return "\n".join(lines)


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
