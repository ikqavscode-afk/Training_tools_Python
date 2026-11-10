"""Проверка модуля 8. Запуск: pytest m08-graphs"""

from __future__ import annotations

from types import ModuleType
from typing import Any

import pytest

EDGES = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "A"), ("C", "D")]


def build(target: ModuleType, edges: list[tuple[str, str]]) -> Any:
    graph = target.DirectedGraph()
    for from_vertex, to_vertex in edges:
        graph.add_edge(from_vertex, to_vertex)
    return graph


# ---------- Задание 1: список смежности ----------


def test_add_vertex_creates_empty_neighbors(target: ModuleType) -> None:
    graph = target.DirectedGraph()
    graph.add_vertex("A")
    assert graph.has_vertex("A") is True
    assert graph.get_neighbors("A") == []


def test_add_vertex_twice_keeps_neighbors(target: ModuleType) -> None:
    graph = target.DirectedGraph()
    graph.add_edge("A", "B")
    graph.add_vertex("A")
    assert graph.get_neighbors("A") == ["B"], "Повторное add_vertex не должно стирать соседей"


def test_add_edge_creates_both_vertices(target: ModuleType) -> None:
    graph = target.DirectedGraph()
    graph.add_edge("A", "B")
    assert graph.has_vertex("A") and graph.has_vertex("B")
    assert graph.get_neighbors("A") == ["B"]
    assert graph.get_neighbors("B") == [], "Ребро ориентированное: из B в A пути нет"


def test_neighbors_keep_insertion_order(target: ModuleType) -> None:
    graph = build(target, EDGES)
    assert graph.get_neighbors("A") == ["B", "C"]
    assert graph.get_neighbors("C") == ["A", "D"]


def test_duplicate_edge_is_ignored(target: ModuleType) -> None:
    graph = target.DirectedGraph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "B")
    assert graph.get_neighbors("A") == ["B"]


def test_unknown_vertex(target: ModuleType) -> None:
    graph = target.DirectedGraph()
    assert graph.has_vertex("Z") is False
    assert graph.get_neighbors("Z") == []


# ---------- Задание 2: BFS ----------


def test_bfs_order(target: ModuleType) -> None:
    graph = build(target, [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")])
    assert target.bfs(graph, "A") == ["A", "B", "C", "D", "E"]


def test_bfs_visits_each_vertex_once_on_cycle(target: ModuleType) -> None:
    graph = build(target, EDGES)
    assert target.bfs(graph, "A") == ["A", "B", "C", "D"]


def test_bfs_chain_from_middle(target: ModuleType) -> None:
    graph = build(target, [("A", "B"), ("B", "C"), ("C", "D")])
    graph.add_vertex("G")
    assert target.bfs(graph, "B") == ["B", "C", "D"]
    assert target.bfs(graph, "G") == ["G"]


def test_bfs_unknown_start(target: ModuleType) -> None:
    assert target.bfs(build(target, EDGES), "Z") == []


# ---------- Задание 3: матрица смежности ----------


def test_matrix_from_edges(target: ModuleType) -> None:
    graph = target.edges_to_adjacency_matrix(EDGES)
    assert graph.vertices == ["A", "B", "C", "D"]
    assert graph.matrix == [
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 1],
        [0, 0, 0, 0],
    ]


def test_matrix_grows_with_new_vertex(target: ModuleType) -> None:
    graph = target.edges_to_adjacency_matrix(EDGES)
    graph.add_vertex("E")
    graph.add_edge("D", "E")
    assert graph.vertices == ["A", "B", "C", "D", "E"]
    assert graph.matrix[3] == [0, 0, 0, 0, 1]
    assert graph.matrix[4] == [0, 0, 0, 0, 0]
    assert all(len(row) == 5 for row in graph.matrix), "Матрица должна остаться квадратной"


def test_matrix_add_vertex_twice(target: ModuleType) -> None:
    graph = target.AdjacencyMatrixGraph()
    graph.add_vertex("A")
    graph.add_vertex("A")
    assert graph.vertices == ["A"]
    assert graph.matrix == [[0]]


def test_matrix_empty(target: ModuleType) -> None:
    graph = target.edges_to_adjacency_matrix([])
    assert graph.vertices == [] and graph.matrix == []


def test_matrix_has_edge(target: ModuleType) -> None:
    graph = target.edges_to_adjacency_matrix(EDGES)
    assert graph.has_edge("A", "B") is True
    assert graph.has_edge("B", "A") is False
    assert graph.has_edge("A", "Z") is False


# ---------- Задание 4: кратчайший путь ----------

METRO = [
    ("Север", "Парк"),
    ("Парк", "Центр"),
    ("Север", "Рынок"),
    ("Рынок", "Центр"),
    ("Центр", "Порт"),
    ("Порт", "Остров"),
]


@pytest.mark.parametrize(
    ("start", "goal", "expected"),
    [
        ("Север", "Центр", 2),
        ("Север", "Порт", 3),
        ("Север", "Остров", 4),
        ("Север", "Север", 0),
        ("Остров", "Север", -1),
        ("Север", "Нигде", -1),
        ("Нигде", "Север", -1),
    ],
    ids=["две пересадки", "три", "четыре", "тот же", "нет пути", "нет цели", "нет старта"],
)
def test_shortest_path_length(target: ModuleType, start: str, goal: str, expected: int) -> None:
    graph = build(target, METRO)
    assert target.shortest_path_length(graph, start, goal) == expected


def test_shortest_path_prefers_shorter_route(target: ModuleType) -> None:
    graph = build(target, [("A", "B"), ("B", "C"), ("C", "D"), ("A", "D")])
    assert target.shortest_path_length(graph, "A", "D") == 1


# ---------- Задание 5: найди ошибку ----------


@pytest.mark.bugfix
def test_has_path(target: ModuleType) -> None:
    """Задание «найди ошибку»: засчитывается, только когда верны ВСЕ случаи."""
    cycle = {"A": ["B"], "B": ["A", "C"], "C": [], "Z": []}
    cases = [
        (cycle, "A", "C", True),
        (cycle, "A", "A", True),
        (cycle, "A", "Z", False),
        ({"A": ["B"], "B": ["A"]}, "A", "X", False),
        ({}, "A", "B", False),
    ]
    for graph, start, goal, expected in cases:
        try:
            got = target.has_path(graph, start, goal)
        except RecursionError:
            pytest.fail(
                f"has_path({graph}, {start!r}, {goal!r}) ушла в бесконечную рекурсию. "
                "Подсказка: что произойдёт на графе, где есть цикл A → B → A?"
            )
        assert got is expected, f"has_path({start!r}, {goal!r}) = {got}, ожидалось {expected}"
