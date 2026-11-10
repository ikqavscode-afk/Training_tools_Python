"""Демо модуля 8: граф-метро, BFS, кратчайший путь и матрица смежности.

Запуск: python m08-graphs/demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "solutions"))
from m08_graphs import (  # noqa: E402
    AdjacencyMatrixGraph,
    DirectedGraph,
    bfs,
    edges_to_adjacency_matrix,
    shortest_path_length,
)

# Линии метро: по каждой можно ехать в обе стороны, поэтому добавляем рёбра парами.
LINES = [
    ("Север", "Парк"),
    ("Парк", "Центр"),
    ("Север", "Рынок"),
    ("Рынок", "Центр"),
    ("Центр", "Порт"),
    ("Порт", "Остров"),
]


def print_matrix(graph: AdjacencyMatrixGraph) -> None:
    width = max(len(v) for v in graph.vertices) + 1
    print(" " * width + "".join(f"{v:>{width}}" for v in graph.vertices))
    for vertex, row in zip(graph.vertices, graph.matrix, strict=True):
        print(f"{vertex:>{width}}" + "".join(f"{cell:>{width}}" for cell in row))


def main() -> None:
    metro = DirectedGraph()
    for a, b in LINES:
        metro.add_edge(a, b)
        metro.add_edge(b, a)

    print("=== Карта метро (список смежности) ===")
    print(metro)

    print("\n=== BFS от станции «Север» ===")
    print(" → ".join(bfs(metro, "Север")))

    print("\n=== Сколько пересадок до станции ===")
    for goal in ["Парк", "Центр", "Порт", "Остров"]:
        print(f"Север → {goal}: {shortest_path_length(metro, 'Север', goal)}")

    print("\n=== Матрица смежности ===")
    edges = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "A"), ("C", "D")]
    matrix = edges_to_adjacency_matrix(edges)
    print_matrix(matrix)
    print(f"\nЕсть ребро A→B? {matrix.has_edge('A', 'B')}. Ребро B→A? {matrix.has_edge('B', 'A')}.")


if __name__ == "__main__":
    main()
