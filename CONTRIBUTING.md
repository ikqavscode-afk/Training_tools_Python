# Как внести вклад

Спасибо, что хотите помочь! Идеи и исправления приветствуются.

## Быстрый старт

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,demo]"
pre-commit install
```

## Правила

- Ветки: `feat/…`, `content/…`, `fix/…`, `docs/…`; изменения — через Pull Request.
- Коммиты в стиле Conventional Commits: `feat(m01): add binary search exercises`.
- Новый модуль создаётся копированием `_template/` (см. [ARCHITECTURE](docs/ARCHITECTURE.md)).
- В каждом задании: ≥ 3 подсказки, тест, эталон в `solutions/`, понятные сообщения.
- Факты проверяем и даём ссылку на источник.
- Объяснения — простые, короткие, без лишнего жаргона.

## Проверки перед PR

```bash
ruff check . && ruff format --check .
PRACTICUM_TARGET=solutions pytest
python tools/check_template.py
python tools/check_exercises_unsolved.py
```
