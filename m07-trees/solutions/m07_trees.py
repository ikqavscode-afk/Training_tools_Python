"""Модуль 7 · Деревья. Эталонные решения (спойлеры!)."""

from __future__ import annotations

from collections import deque


class Node:
    """Узел дерева."""

    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None
        self.height = 1


class BST:
    """Бинарное дерево поиска."""

    def __init__(self) -> None:
        self.root: Node | None = None

    def insert(self, value: int) -> None:
        """Добавить значение (дубликаты игнорируются)."""
        self.root = self._insert(self.root, value)

    def _insert(self, node: Node | None, value: int) -> Node:
        if node is None:
            return Node(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        return node

    def search(self, value: int) -> bool:
        """Есть ли значение в дереве."""
        node = self.root
        while node is not None:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False


def preorder(root: Node | None) -> list[int]:
    """Корень → левое → правое."""
    if root is None:
        return []
    return [root.value, *preorder(root.left), *preorder(root.right)]


def inorder(root: Node | None) -> list[int]:
    """Левое → корень → правое."""
    if root is None:
        return []
    return [*inorder(root.left), root.value, *inorder(root.right)]


def postorder(root: Node | None) -> list[int]:
    """Левое → правое → корень."""
    if root is None:
        return []
    return [*postorder(root.left), *postorder(root.right), root.value]


def bfs(root: Node | None) -> list[int]:
    """Обход в ширину."""
    if root is None:
        return []
    result: list[int] = []
    queue: deque[Node] = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.value)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result


def height(node: Node | None) -> int:
    """Высота узла (у пустого места 0)."""
    return node.height if node else 0


def update_height(node: Node) -> None:
    """Пересчитать высоту узла по высотам потомков."""
    node.height = 1 + max(height(node.left), height(node.right))


def balance_factor(node: Node | None) -> int:
    """Высота левого поддерева минус высота правого."""
    if node is None:
        return 0
    return height(node.left) - height(node.right)


def right_rotate(z: Node) -> Node:
    """Правый поворот; возвращает новый корень поддерева."""
    y = z.left
    assert y is not None, "правый поворот требует левого потомка"
    t3 = y.right
    y.right = z
    z.left = t3
    update_height(z)
    update_height(y)
    return y


def left_rotate(z: Node) -> Node:
    """Левый поворот; возвращает новый корень поддерева."""
    y = z.right
    assert y is not None, "левый поворот требует правого потомка"
    t2 = y.left
    y.left = z
    z.right = t2
    update_height(z)
    update_height(y)
    return y


def rebalance(node: Node) -> Node:
    """Обновить высоту и при необходимости повернуть; вернуть корень поддерева."""
    update_height(node)
    balance = balance_factor(node)
    if balance > 1:
        assert node.left is not None
        if balance_factor(node.left) < 0:
            node.left = left_rotate(node.left)
        return right_rotate(node)
    if balance < -1:
        assert node.right is not None
        if balance_factor(node.right) > 0:
            node.right = right_rotate(node.right)
        return left_rotate(node)
    return node


class AVLTree(BST):
    """АВЛ-дерево: высоты потомков любого узла отличаются не больше чем на 1."""

    def insert(self, value: int) -> None:
        """Добавить значение и сохранить баланс."""
        self.root = self._insert_avl(self.root, value)

    def _insert_avl(self, node: Node | None, value: int) -> Node:
        if node is None:
            return Node(value)
        if value < node.value:
            node.left = self._insert_avl(node.left, value)
        elif value > node.value:
            node.right = self._insert_avl(node.right, value)
        else:
            return node
        return rebalance(node)


def contains_value(root: Node | None, target: int) -> bool:
    """Есть ли target в дереве поиска (исправлено: меньше — идём ВЛЕВО)."""
    if root is None:
        return False
    if root.value == target:
        return True
    if target < root.value:
        return contains_value(root.left, target)
    return contains_value(root.right, target)
