"""Проверка, что каждый модуль соответствует шаблону.

Основные модули ``mNN-name`` (в корне) и бонус-модули ``bonus/bNN-name``.

Основной модуль: обязательные файлы, ≥ 3 подсказки на задание, раздел «А знаете?» с источником.
Бонус-модуль дополнительно: баннер ``[!IMPORTANT]``, метки навыков (🛠, а также 🧠 или 🤝),
для заданий с меткой 🤝 (без автопроверки) — «Образец ответа» вместо подсказок.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAIN_NAME = re.compile(r"m\d{2}-[a-z0-9-]+")
BONUS_NAME = re.compile(r"b\d{2}-[a-z0-9-]+")
REQUIRED = ["README.md", "exercises.py", "test_exercises.py", "demo.py"]
HINTS_PER_TASK = 3


def find_modules(root: Path = ROOT) -> tuple[list[Path], list[Path]]:
    """Вернуть (основные модули, бонус-модули)."""
    main = sorted(p for p in root.iterdir() if p.is_dir() and MAIN_NAME.fullmatch(p.name))
    bonus_dir = root / "bonus"
    bonus: list[Path] = []
    if bonus_dir.is_dir():
        bonus = sorted(
            p for p in bonus_dir.iterdir() if p.is_dir() and BONUS_NAME.fullmatch(p.name)
        )
    return main, bonus


def check_module(module: Path, bonus: bool = False) -> list[str]:
    errors: list[str] = []
    name = f"bonus/{module.name}" if bonus else module.name
    for required in REQUIRED:
        if not (module / required).is_file():
            errors.append(f"{name}: нет файла {required}")
    solution = module / "solutions" / f"{module.name.replace('-', '_')}.py"
    if not solution.is_file():
        errors.append(f"{name}: нет эталона {solution.relative_to(module)}")

    readme = module / "README.md"
    if not readme.is_file():
        return errors
    text = readme.read_text(encoding="utf-8")

    task_lines = re.findall(r"^\*\*Задание.*$", text, flags=re.MULTILINE)
    if not task_lines:
        errors.append(f"{name}: в README нет заданий («**Задание N. …**»)")
    # «Предскажи вывод» без запуска подсказок не требует (ответ в <details>);
    # задания 🤝 (практика без автопроверки) требуют «Образец ответа».
    soft = [line for line in task_lines if "🤝" in line and "Предскажи вывод" not in line]
    auto = [line for line in task_lines if "Предскажи вывод" not in line and "🤝" not in line]
    hints = len(re.findall(r"<summary>💡", text))
    if hints < HINTS_PER_TASK * len(auto):
        errors.append(
            f"{name}: подсказок {hints}, нужно ≥ {HINTS_PER_TASK * len(auto)} "
            f"({HINTS_PER_TASK} на задание с автопроверкой)"
        )
    samples = len(re.findall(r"<summary>Образец", text))
    if samples < len(soft):
        errors.append(f"{name}: «Образец ответа» у {samples} из {len(soft)} заданий 🤝")

    if "А знаете?" not in text:
        errors.append(f"{name}: нет раздела «А знаете?»")
    elif not re.search(r"А знаете\?.*?https?://", text, flags=re.DOTALL):
        errors.append(f"{name}: у факта нет ссылки на источник")

    if bonus:
        if "[!IMPORTANT]" not in text:
            errors.append(f"{name}: нет баннера бонус-уровня (> [!IMPORTANT])")
        if "🛠" not in text:
            errors.append(f"{name}: нет заданий с меткой 🛠 (Hard skill)")
        if "🧠" not in text and "🤝" not in text:
            errors.append(f"{name}: нет заданий с меткой 🧠 (мышление) или 🤝 (с людьми)")
    return errors


def main() -> int:
    main_modules, bonus_modules = find_modules()
    errors = [e for m in main_modules for e in check_module(m)]
    errors += [e for m in bonus_modules for e in check_module(m, bonus=True)]
    for error in errors:
        print("ОШИБКА:", error)
    print(
        f"Проверено модулей: {len(main_modules)} основных и {len(bonus_modules)} бонусных, "
        f"ошибок: {len(errors)}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
