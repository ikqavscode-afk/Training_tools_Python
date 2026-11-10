"""Проверка модуля 7. Запуск: pytest m07-trees"""

from __future__ import annotations

from types import ModuleType
from typing import Any

import pytest


def make(target: ModuleType, value: int, left: Any = None, right: Any = None) -> Any:
    """Собрать узел вручную и честно проставить высоту (не зависит от ваших функций)."""
    node = target.Node(value)
    node.left = left
    node.right = right
    node.height = 1 + max(left.height if left else 0, right.height if right else 0)
    return node


def sample_tree(target: ModuleType) -> Any:
    """Дерево:        50
                     /  \\
                   30    70
                  / \\   / \\
                20  40 60  80
    """
    return make(
        target,
        50,
        make(target, 30, make(target, 20), make(target, 40)),
        make(target, 70, make(target, 60), make(target, 80)),
    )


def values_in_order(node: Any) -> list[int]:
    """Свой обход для проверок (чтобы тесты не зависели от ваших функций)."""
    if node is None:
        return []
    return [*values_in_order(node.left), node.value, *values_in_order(node.right)]


def real_height(node: Any) -> int:
    if node is None:
        return 0
    return 1 + max(real_height(node.left), real_height(node.right))


def check_balanced(node: Any) -> None:
    """Проверить, что у каждого узла баланс в [-1, 1], а сохранённая высота верна."""
    if node is None:
        return
    assert abs(real_height(node.left) - real_height(node.right)) <= 1, (
        f"Узел {node.value} не сбалансирован"
    )
    assert node.height == real_height(node), (
        f"У узла {node.value} высота {node.height}, а должна быть {real_height(node)}"
    )
    check_balanced(node.left)
    check_balanced(node.right)


# ---------- Задание 1: BST ----------


def test_bst_insert_builds_correct_shape(target: ModuleType) -> None:
    tree = target.BST()
    for value in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(value)
    root = tree.root
    assert root.value == 50
    assert (root.left.value, root.right.value) == (30, 70)
    assert (root.left.left.value, root.left.right.value) == (20, 40)
    assert (root.right.left.value, root.right.right.value) == (60, 80)


def test_bst_insert_ignores_duplicates(target: ModuleType) -> None:
    tree = target.BST()
    for value in [5, 3, 5, 3, 8]:
        tree.insert(value)
    assert values_in_order(tree.root) == [3, 5, 8]


@pytest.mark.parametrize(
    ("value", "expected"),
    [(30, True), (70, True), (85, False), (144, False), (50, True)],
    ids=["30", "70", "нет 85", "нет 144", "корень"],
)
def test_bst_search(target: ModuleType, value: int, expected: bool) -> None:
    tree = target.BST()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(v)
    assert tree.search(value) is expected


def test_bst_search_empty(target: ModuleType) -> None:
    assert target.BST().search(1) is False


# ---------- Задание 2–3: обходы ----------


def test_preorder(target: ModuleType) -> None:
    assert target.preorder(sample_tree(target)) == [50, 30, 20, 40, 70, 60, 80]


def test_inorder_is_sorted(target: ModuleType) -> None:
    assert target.inorder(sample_tree(target)) == [20, 30, 40, 50, 60, 70, 80]


def test_postorder(target: ModuleType) -> None:
    assert target.postorder(sample_tree(target)) == [20, 40, 30, 60, 80, 70, 50]


def test_bfs_goes_level_by_level(target: ModuleType) -> None:
    assert target.bfs(sample_tree(target)) == [50, 30, 70, 20, 40, 60, 80]


@pytest.mark.parametrize("name", ["preorder", "inorder", "postorder", "bfs"])
def test_traversals_of_empty_tree(target: ModuleType, name: str) -> None:
    assert getattr(target, name)(None) == []


@pytest.mark.parametrize("name", ["preorder", "inorder", "postorder", "bfs"])
def test_traversals_of_chain(target: ModuleType, name: str) -> None:
    chain = make(target, 1, None, make(target, 2, None, make(target, 3)))
    assert getattr(target, name)(chain) == ([3, 2, 1] if name == "postorder" else [1, 2, 3])


# ---------- Задание 4: высота и баланс ----------


def test_height_of_none_is_zero(target: ModuleType) -> None:
    assert target.height(None) == 0


def test_height_reads_node_field(target: ModuleType) -> None:
    node = target.Node(1)
    node.height = 3
    assert target.height(node) == 3


def test_update_height(target: ModuleType) -> None:
    node = target.Node(10)
    node.left = make(target, 5, make(target, 3), None)  # высота 2
    node.right = make(target, 20)  # высота 1
    target.update_height(node)
    assert node.height == 3, "Высота = 1 + большая из высот потомков"


def test_update_height_of_leaf(target: ModuleType) -> None:
    node = target.Node(10)
    node.height = 99
    target.update_height(node)
    assert node.height == 1


@pytest.mark.parametrize(
    ("left_depth", "right_depth", "expected"),
    [(2, 0, 2), (0, 2, -2), (1, 1, 0), (3, 1, 2)],
    ids=["слева тяжелее", "справа тяжелее", "ровно", "перекос на 2"],
)
def test_balance_factor(
    target: ModuleType, left_depth: int, right_depth: int, expected: int
) -> None:
    def chain(depth: int) -> Any:
        node = None
        for i in range(depth):
            node = make(target, i, node, None)
        return node

    node = make(target, 100, chain(left_depth), chain(right_depth))
    assert target.balance_factor(node) == expected


def test_balance_factor_of_none(target: ModuleType) -> None:
    assert target.balance_factor(None) == 0


# ---------- Задание 5: повороты ----------


def test_right_rotate_simple(target: ModuleType) -> None:
    z = make(target, 30, make(target, 20, make(target, 10), None), None)
    root = target.right_rotate(z)
    assert (root.value, root.left.value, root.right.value) == (20, 10, 30)
    assert (root.height, root.left.height, root.right.height) == (2, 1, 1)


def test_right_rotate_moves_middle_subtree(target: ModuleType) -> None:
    y = make(target, 30, make(target, 20), make(target, 40))
    z = make(target, 50, y, None)
    root = target.right_rotate(z)
    assert root.value == 30
    assert root.right.value == 50
    assert root.right.left.value == 40, "Правое поддерево y должно переехать к z слева"
    assert (root.height, root.right.height) == (3, 2)


def test_left_rotate_simple(target: ModuleType) -> None:
    z = make(target, 10, None, make(target, 20, None, make(target, 30)))
    root = target.left_rotate(z)
    assert (root.value, root.left.value, root.right.value) == (20, 10, 30)
    assert (root.height, root.left.height, root.right.height) == (2, 1, 1)


def test_left_rotate_moves_middle_subtree(target: ModuleType) -> None:
    y = make(target, 30, make(target, 20), make(target, 40))
    z = make(target, 10, None, y)
    root = target.left_rotate(z)
    assert root.value == 30
    assert root.left.value == 10
    assert root.left.right.value == 20, "Левое поддерево y должно переехать к z справа"
    assert (root.height, root.left.height) == (3, 2)


# ---------- Задание 6: AVL ----------


def test_rebalance_keeps_balanced_node(target: ModuleType) -> None:
    node = make(target, 20, make(target, 10), make(target, 30))
    assert target.rebalance(node) is node


def test_rebalance_left_left(target: ModuleType) -> None:
    node = make(target, 30, make(target, 20, make(target, 10), None), None)
    root = target.rebalance(node)
    assert (root.value, root.left.value, root.right.value) == (20, 10, 30)


def test_rebalance_right_right(target: ModuleType) -> None:
    node = make(target, 10, None, make(target, 20, None, make(target, 30)))
    root = target.rebalance(node)
    assert (root.value, root.left.value, root.right.value) == (20, 10, 30)


def test_rebalance_left_right(target: ModuleType) -> None:
    node = make(target, 30, make(target, 10, None, make(target, 20)), None)
    root = target.rebalance(node)
    assert (root.value, root.left.value, root.right.value) == (20, 10, 30)


def test_rebalance_right_left(target: ModuleType) -> None:
    node = make(target, 10, None, make(target, 30, make(target, 20), None))
    root = target.rebalance(node)
    assert (root.value, root.left.value, root.right.value) == (20, 10, 30)


@pytest.mark.parametrize(
    ("order", "root_value"),
    [([30, 10, 20], 20), ([10, 30, 20], 20), ([1, 2, 3], 2), ([3, 2, 1], 2)],
    ids=["лево-право", "право-лево", "по возрастанию", "по убыванию"],
)
def test_avl_three_nodes_become_a_triangle(
    target: ModuleType, order: list[int], root_value: int
) -> None:
    tree = target.AVLTree()
    for value in order:
        tree.insert(value)
    assert tree.root.value == root_value
    assert tree.root.height == 2
    assert values_in_order(tree.root) == sorted(order)


def test_avl_ascending_insert_stays_balanced(target: ModuleType) -> None:
    tree = target.AVLTree()
    for value in range(1, 16):
        tree.insert(value)
    check_balanced(tree.root)
    assert tree.root.height == 4, "15 узлов в сбалансированном дереве — высота 4"
    assert values_in_order(tree.root) == list(range(1, 16))


def test_avl_shape_for_seven_ascending(target: ModuleType) -> None:
    tree = target.AVLTree()
    for value in range(1, 8):
        tree.insert(value)
    assert target.preorder(tree.root) == [4, 2, 1, 3, 6, 5, 7]


def test_avl_ignores_duplicates(target: ModuleType) -> None:
    tree = target.AVLTree()
    for value in [5, 5, 5]:
        tree.insert(value)
    assert values_in_order(tree.root) == [5]


# ---------- Задание 7: найди ошибку ----------


@pytest.mark.bugfix
def test_contains_value(target: ModuleType) -> None:
    """Задание «найди ошибку»: засчитывается, только когда верны ВСЕ случаи."""
    root = sample_tree(target)
    for value in [50, 30, 70, 20, 40, 60, 80]:
        assert target.contains_value(root, value) is True, (
            f"contains_value не нашла {value}, а он есть в дереве. "
            "Подсказка: в какую сторону надо идти, если искомое меньше текущего?"
        )
    for value in [10, 45, 55, 100]:
        assert target.contains_value(root, value) is False
    assert target.contains_value(None, 1) is False
