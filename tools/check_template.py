"""Проверка, что каждый модуль соответствует шаблону.

Требования к модулю ``mNN-name``: обязательные файлы, ≥ 3 подсказки на задание,
раздел «А знаете?» со ссылкой на источник.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ["README.md", "exercises.py", "test_exercises.py", "demo.py"]


def check_module(module: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED:
        if not (module / name).is_file():
            errors.append(f"{module.name}: нет файла {name}")
    solution = module / "solutions" / f"{module.name.replace('-', '_')}.py"
    if not solution.is_file():
        errors.append(f"{module.name}: нет эталона {solution.relative_to(module)}")

    readme = module / "README.md"
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        # задания «Предскажи вывод» без запуска подсказок не требуют (ответ в <details>)
        task_lines = re.findall(r"^\*\*Задание.*$", text, flags=re.MULTILINE)
        tasks = sum("Предскажи вывод" not in line for line in task_lines)
        hints = len(re.findall(r"<summary>💡", text))
        if tasks == 0:
            errors.append(f"{module.name}: в README нет заданий («**Задание N. …**»)")
        if hints < 3 * tasks:
            errors.append(f"{module.name}: подсказок {hints}, нужно ≥ {3 * tasks} (3 на задание)")
        if "А знаете?" not in text:
            errors.append(f"{module.name}: нет раздела «А знаете?»")
        elif not re.search(r"А знаете\?.*?https?://", text, flags=re.DOTALL):
            errors.append(f"{module.name}: у факта нет ссылки на источник")
    return errors


def main() -> int:
    modules = sorted(p for p in ROOT.iterdir() if re.fullmatch(r"m\d{2}-[a-z0-9-]+", p.name))
    errors = [e for m in modules for e in check_module(m)]
    for e in errors:
        print("ОШИБКА:", e)
    print(f"Проверено модулей: {len(modules)}, ошибок: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
