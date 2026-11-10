# 🐍 Python: алгоритмы и структуры данных — практикум

[![CI](https://github.com/ikqavscode-afk/Training_tools_Python/actions/workflows/ci.yml/badge.svg)](https://github.com/ikqavscode-afk/Training_tools_Python/actions/workflows/ci.yml)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ikqavscode-afk/Training_tools_Python)

Набор небольших упражнений по алгоритмам и структурам данных на чистом Python: **8 модулей, 48 заданий** и бонус-уровни (пока b01, 7 заданий).
В каждом модуле короткая теория простыми словами, задания с автопроверкой, подсказки трёх уровней, готовое решение, демонстрация и «интересный факт».

Ничего устанавливать не нужно: откройте репозиторий в **GitHub Codespaces** (кнопка **Code → Codespaces**), и редактор с Python запустится в браузере.

## Для кого

| Кто | Что даёт |
|---|---|
| Новичок в Python | Закрепить циклы, функции, списки и классы на понятных задачах |
| Готовящийся к собеседованию | Быстро повторить базу: поиск, сортировки, хэши, деревья, графы |
| Автор | Показать, что пройдено и закреплено, в виде аккуратного репозитория |

## Как пользоваться

1. **Откройте** репозиторий в [Codespaces](https://codespaces.new/ikqavscode-afk/Training_tools_Python) или клонируйте его (команды ниже).
2. **Выберите модуль** и прочитайте его `README.md` (около 5–10 минут).
3. **Допишите код** в `exercises.py` и запустите проверку:

   ```bash
   pytest m01-search
   ```

Пока в заготовке стоит `raise NotImplementedError`, тест показывает «ещё не сделано» (это не ошибка). Зелёные тесты — задание выполнено.
Застряли? Откройте подсказку 1, затем 2, затем 3. Готовое решение лежит в `solutions/`, смотреть его нужно в последнюю очередь.

### Локальный запуск

```bash
git clone https://github.com/ikqavscode-afk/Training_tools_Python.git
cd Training_tools_Python
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest m01-search
```

Нужен Python 3.11 или новее. Для графиков в `demo.py` добавьте `pip install -e ".[demo]"`.

### Как увидеть свой прогресс

Сделайте **fork** репозитория, решайте задания и делайте `push`. Во вкладке **Actions** запустится «My progress» и покажет таблицу: сколько заданий выполнено в каждом модуле.
Локально то же самое: `python tools/progress.py`.

## Модули

| № | Модуль | Что тренируем | Заданий |
|---|---|---|---|
| 1 | [Поиск](m01-search/README.md) | линейный и бинарный поиск, O(n) и O(log n), счётчик обращений | 5 |
| 2 | [Простые сортировки](m02-simple-sorts/README.md) | пузырёк, выбор, вставки, копирование списка | 5 |
| 3 | [Рекурсия и стек](m03-recursion-stack/README.md) | базовый и рекурсивный случай, `Stack`, исключения | 6 |
| 4 | [Рекурсия глубже и QuickSort](m04-quicksort/README.md) | дерево вызовов Фибоначчи, `partition`, QuickSort | 6 |
| 5 | [Очередь и MergeSort](m05-queue-mergesort/README.md) | `Queue` на `deque`, симуляция задач, слияние | 6 |
| 6 | [Хэш-таблицы](m06-hash-tables/README.md) | хэш-функция, коллизии, цепочки, `resize` | 6 |
| 7 | [Деревья](m07-trees/README.md) | BST, обходы DFS и BFS, повороты, AVL | 8 |
| 8 | [Графы](m08-graphs/README.md) | список и матрица смежности, BFS, кратчайший путь | 6 |

В каждом модуле есть задание «найди ошибку»: готовый код с придуманной ошибкой, которую нужно найти и исправить.
Типы заданий: допиши · напиши с нуля · найди ошибку · предскажи вывод · сравни скорость.

## Что внутри модуля

```
m03-recursion-stack/
├─ README.md          что это и зачем · теория карточками · схема · задания и подсказки · факт
├─ exercises.py       заготовки с TODO
├─ test_exercises.py  автопроверка с понятными сообщениями
├─ solutions/         готовое решение (спойлеры!)
└─ demo.py            запуск «что получилось»: вывод шагов, таблицы времени
```

## Структура репозитория

```
├─ m01-search/ … m08-graphs/   модули
├─ _template/                  шаблон нового модуля
├─ bonus/                      бонус-уровни (b01 …)
├─ _template_bonus/            шаблон бонус-модуля
├─ conftest.py                 проверка заданий: exercises.py или solutions/
├─ tools/                      прогресс, проверка шаблона и «нерешённых» заготовок
├─ docs/                       требования, техдокументация, бэклог, план, глоссарий
├─ assets/                     графики из demo.py
├─ .github/                    CI, шаблоны Issues и PR, Dependabot
├─ .devcontainer/              окружение для Codespaces
└─ pyproject.toml              зависимости и настройки pytest, Ruff, Mypy
```

## Что здесь показано

| Навык | Где смотреть |
|---|---|
| Функции, циклы, срезы | [`m01`](m01-search/solutions/m01_search.py), [`m02`](m02-simple-sorts/solutions/m02_simple_sorts.py) |
| Рекурсия | [`m03`](m03-recursion-stack/solutions/m03_recursion_stack.py), [`m04`](m04-quicksort/solutions/m04_quicksort.py), [`m05`](m05-queue-mergesort/solutions/m05_queue_mergesort.py) |
| Классы, `__repr__`, `__len__`, инкапсуляция | [`Stack`](m03-recursion-stack/solutions/m03_recursion_stack.py), [`Queue`](m05-queue-mergesort/solutions/m05_queue_mergesort.py), [`HashTable`](m06-hash-tables/solutions/m06_hash_tables.py) |
| Наследование | `AVLTree(BST)` в [`m07`](m07-trees/solutions/m07_trees.py) |
| Исключения | `Stack.pop`, `Queue.dequeue`, `factorial` |
| Структуры данных | стек, очередь, хэш-таблица, дерево, граф |
| Алгоритмы | поиск, сортировки, обходы BFS и DFS, кратчайший путь |
| Type hints и docstrings | все [`solutions/`](m08-graphs/solutions/m08_graphs.py), проверка Mypy в strict-режиме |
| Стиль кода | Ruff ([`pyproject.toml`](pyproject.toml)), [pre-commit](.pre-commit-config.yaml) |
| Тесты как проверка заданий | [`conftest.py`](conftest.py), `test_exercises.py` в каждом модуле |
| Git и GitHub | ветки и Pull Requests, [Conventional Commits](CONTRIBUTING.md), [шаблон PR](.github/PULL_REQUEST_TEMPLATE.md) |
| CI/CD | [GitHub Actions](.github/workflows/ci.yml) |
| Окружение | [`pyproject.toml`](pyproject.toml), venv, [devcontainer](.devcontainer/devcontainer.json) |

### 🧠 Мышление и ответственность

Показано только то, что подтверждено файлами репозитория:

| Навык | Подтверждение |
|---|---|
| Инженерный подход | тесты с крайними случаями, CI, проверка эталонов, ADR в [ARCHITECTURE](docs/ARCHITECTURE.md) |
| Аналитический склад ума | замеры и выводы о сложности в `demo.py` модулей 1, 2, 4, 5, 6 |
| Стратегическое мышление | [BACKLOG](docs/BACKLOG.md), [SCRUM_PLAN](docs/SCRUM_PLAN.md), нарезка релизов, дорожная карта |
| Системное мышление | слои: движок проверки, шаблоны, модули, инструменты |
| Планирование и ответственность | [CHANGELOG](CHANGELOG.md), защита ветки, история без личных данных |

## Дорожная карта

- 🚀 **Бонус-уровни** (b01 готов, b02 и b03 в разработке, подробности в [карте бонусов](docs/BONUS_MAP.md)):

  | Модуль | 🛠 Hard | 🧠 Мышление | 🤝 С людьми |
  |---|---|---|---|
  | [b01 · Инструменты профи](bonus/b01-pro-tools/README.md) | декораторы, `Timer`, генераторы, `lru_cache`, `bisect`, `heapq` | измерять до оптимизации, читать документацию | объяснить решение коллеге |
  | b02 · Качество кода | рефакторинг, DRY, KISS, `@dataclass`, `@property`, type hints | внимание к деталям | код-ревью, сообщения коммитов |
  | b03 · Инженерное мышление | выбор структур и алгоритмов | аналитика, стратегия, декомпозиция | оценка сроков, уточняющие вопросы |

  Бонус лежит в отдельной папке `bonus/`, помечен баннером и метками навыков. Для него нужно не только знание Python: тренируются ещё мышление и работа с людьми.
- Следующие репозитории (ссылки появятся позже): базы данных и SQL · веб и API · архитектура приложений.

## Документация

[Требования](docs/REQUIREMENTS.md) · [Карта контента](docs/CONTENT_MAP.md) · [Техническая документация](docs/ARCHITECTURE.md) · [Бэклог](docs/BACKLOG.md) · [Scrum-план](docs/SCRUM_PLAN.md) · [Глоссарий](docs/GLOSSARY.md) · [Бонус-уровни](docs/BONUS_MAP.md) · [История изменений](CHANGELOG.md) · [Как внести вклад](CONTRIBUTING.md)

## Лицензия

Код — [MIT](LICENSE). Тексты и задания написаны автором; материалы курса не копируются.
Основа — практические работы учебного курса по Python.
