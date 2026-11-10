"""CI-защита: в репозитории заготовки не должны быть случайно решены или сломаны.

Запускает тесты на ``exercises.py`` и требует: ни одного пройденного и ни одного упавшего теста.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


class Counter:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0
        self.skipped = 0

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.when == "call" or (report.when == "setup" and report.skipped):
            setattr(self, report.outcome, getattr(self, report.outcome) + 1)


def main() -> int:
    os.chdir(ROOT)
    os.environ["PRACTICUM_TARGET"] = "exercises"
    counter = Counter()
    pytest.main(["-q", "--no-header", "-p", "no:cacheprovider"], plugins=[counter])
    print(
        f"\nЗаготовки: пройдено={counter.passed}, падает={counter.failed}, "
        f"не сделано={counter.skipped}"
    )
    if counter.passed or counter.failed:
        print("ОШИБКА: в заготовках не должно быть решённых или падающих тестов.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
