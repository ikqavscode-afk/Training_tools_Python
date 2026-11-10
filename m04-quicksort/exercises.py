"""Модуль 4 · Рекурсия глубже и QuickSort. Допишите код и запустите: pytest m04-quicksort"""

from __future__ import annotations


def fibonacci(n: int) -> int:
    """Задание 1а. Число Фибоначчи рекурсивно: F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2)."""
    # TODO: два базовых случая и два рекурсивных вызова
    raise NotImplementedError


def count_fib_calls(n: int) -> int:
    """Задание 1б. Сколько раз будет вызвана fibonacci при вычислении fibonacci(n).

    Считайте и самый первый вызов. Например, для n=5 ответ 15.
    """
    # TODO: вызов один + вызовы для n-1 и n-2 (для n <= 1 вызов только один)
    raise NotImplementedError


def find_max_rec(items: list[int], left: int = 0, right: int | None = None) -> int:
    """Задание 2. Максимум «разделяй и властвуй»: делим список пополам.

    Для пустого списка — ValueError. Функции max() и циклы использовать нельзя.
    """
    # TODO: один элемент — это и есть максимум; иначе найдите максимум в каждой половине
    raise NotImplementedError


def partition(items: list[int], low: int, high: int) -> int:
    """Задание 3. Разбиение (схема Ломуто) части списка items[low..high] НА МЕСТЕ.

    Опорный элемент — items[high]. После вызова слева от него стоят элементы <= опорного,
    справа — большие. Верните индекс, на котором оказался опорный элемент.
    """
    # TODO: pivot = items[high]; i — граница «маленьких»; пройдите j от low до high - 1
    raise NotImplementedError


def quicksort(items: list[int]) -> list[int]:
    """Задание 4. Быстрая сортировка с помощью partition. Верните НОВЫЙ список."""
    # TODO: сделайте копию, затем рекурсивно отсортируйте левую и правую части вокруг опоры
    raise NotImplementedError


def quicksort_lists(items: list[int]) -> list[int]:
    """Задание 5 («найди ошибку»). Короткий QuickSort на списковых выражениях.

    Функция написана, но иногда «теряет» элементы. Найдите ошибку и исправьте её.
    """
    if len(items) <= 1:
        return items.copy()
    pivot = items[0]
    smaller = [x for x in items[1:] if x < pivot]
    larger = [x for x in items[1:] if x > pivot]
    return quicksort_lists(smaller) + [pivot] + quicksort_lists(larger)
