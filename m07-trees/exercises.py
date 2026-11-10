"""Модуль 7 · Деревья. Допишите код и запустите: pytest m07-trees"""

from __future__ import annotations


class Node:
    """Узел дерева: значение, левый и правый потомки и высота (нужна для AVL). Уже готов."""

    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None
        self.height = 1


class BST:
    """Задание 1. Бинарное дерево поиска: слева меньше, справа больше. Дубликаты игнорируем."""

    def __init__(self) -> None:
        self.root: Node | None = None

    def insert(self, value: int) -> None:
        """Добавить значение. Подсказка: удобно написать рекурсивную помощницу _insert."""
        # TODO: пустое место — новый Node; меньше — идём влево; больше — вправо
        raise NotImplementedError

    def search(self, value: int) -> bool:
        """Есть ли значение в дереве."""
        # TODO: сравнивайте с текущим узлом и идите влево или вправо
        raise NotImplementedError


def preorder(root: Node | None) -> list[int]:
    """Задание 2а. Прямой обход (DFS): корень → левое → правое."""
    raise NotImplementedError


def inorder(root: Node | None) -> list[int]:
    """Задание 2б. Симметричный обход (DFS): левое → корень → правое."""
    raise NotImplementedError


def postorder(root: Node | None) -> list[int]:
    """Задание 2в. Обратный обход (DFS): левое → правое → корень."""
    raise NotImplementedError


def bfs(root: Node | None) -> list[int]:
    """Задание 3. Обход в ширину: по уровням, слева направо. Используйте очередь (deque)."""
    raise NotImplementedError


def height(node: Node | None) -> int:
    """Задание 4а. Высота узла: у пустого места 0, иначе значение node.height."""
    raise NotImplementedError


def update_height(node: Node) -> None:
    """Задание 4б. Пересчитать node.height: 1 + большая из высот потомков."""
    raise NotImplementedError


def balance_factor(node: Node | None) -> int:
    """Задание 4в. Баланс: высота левого поддерева минус высота правого (для None — 0)."""
    raise NotImplementedError


def right_rotate(z: Node) -> Node:
    """Задание 5а. Правый поворот вокруг z. Верните НОВЫЙ корень поддерева.

    Левый потомок y становится корнем, а правое поддерево y переезжает к z слева.
    Высоты обновите: сначала z, потом y.
    """
    raise NotImplementedError


def left_rotate(z: Node) -> Node:
    """Задание 5б. Левый поворот вокруг z (зеркально правому). Верните НОВЫЙ корень."""
    raise NotImplementedError


def rebalance(node: Node) -> Node:
    """Задание 6а. Обновить высоту node и при необходимости выполнить повороты.

    Баланс > 1: левое поддерево тяжелее (если у левого потомка баланс < 0 — сначала
    левый поворот у него). Баланс < -1: зеркально. Верните корень поддерева.
    """
    raise NotImplementedError


class AVLTree(BST):
    """Задание 6б. Самобалансирующееся дерево: после каждой вставки вызывайте rebalance."""

    def insert(self, value: int) -> None:
        """Добавить значение (дубликаты игнорируем) и сохранить баланс."""
        raise NotImplementedError


def contains_value(root: Node | None, target: int) -> bool:
    """Задание 7 («найди ошибку»). Есть ли target в дереве поиска.

    Функция написана, но иногда не находит существующие значения.
    Найдите ошибку и исправьте её.
    """
    if root is None:
        return False
    if root.value == target:
        return True
    if target < root.value:
        return contains_value(root.right, target)
    return contains_value(root.left, target)
