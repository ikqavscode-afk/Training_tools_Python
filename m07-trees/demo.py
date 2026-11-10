"""Демо модуля 7: обходы дерева и сравнение обычного BST с AVL.

Запуск: python m07-trees/demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "solutions"))
from m07_trees import BST, AVLTree, Node, bfs, inorder, postorder, preorder  # noqa: E402

VALUES = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]


def draw(node: Node | None, depth: int = 0) -> None:
    """Печать дерева «на боку»: корень слева, правые потомки сверху."""
    if node is None:
        return
    draw(node.right, depth + 1)
    print("    " * depth + str(node.value))
    draw(node.left, depth + 1)


def real_height(node: Node | None) -> int:
    if node is None:
        return 0
    return 1 + max(real_height(node.left), real_height(node.right))


def traversals_demo() -> None:
    tree = BST()
    for value in VALUES:
        tree.insert(value)
    print("Вставляли:", VALUES)
    print("\nДерево (повёрнуто на бок):")
    draw(tree.root)
    print("\nBFS (по уровням):          ", bfs(tree.root))
    print("Прямой (корень-лево-право):", preorder(tree.root))
    print("Симметричный (лево-корень):", inorder(tree.root), "← всегда по возрастанию!")
    print("Обратный (лево-право-корень):", postorder(tree.root))
    print(f"search(75) = {tree.search(75)}, search(144) = {tree.search(144)}")


def balance_demo() -> None:
    plain = BST()
    avl = AVLTree()
    for value in range(1, 32):
        plain.insert(value)
        avl.insert(value)
    print("Вставляем числа 1, 2, 3, … 31 по возрастанию.")
    print(f"Обычное BST: высота {real_height(plain.root)} (дерево вытянулось в цепочку)")
    print(f"AVL:         высота {real_height(avl.root)} (дерево держит баланс)")
    print("\nAVL для 1..7:")
    small = AVLTree()
    for value in range(1, 8):
        small.insert(value)
    draw(small.root)


def main() -> None:
    print("=== Обходы дерева ===")
    traversals_demo()
    print("\n=== BST и AVL ===")
    balance_demo()


if __name__ == "__main__":
    main()
