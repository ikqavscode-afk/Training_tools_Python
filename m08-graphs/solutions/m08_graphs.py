"""Модуль 8 · Графы. Эталонные решения (спойлеры!)."""

from __future__ import annotations

from collections import deque


class DirectedGraph:
    """Ориентированный граф на списке смежности."""

    def __init__(self) -> None:
        self.adjacency_list: dict[str, list[str]] = {}

    def add_vertex(self, vertex: str) -> None:
        """Добавить вершину."""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, from_vertex: str, to_vertex: str) -> None:
        """Добавить ребро; вершины создаются автоматически; повтор не добавляется."""
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        if to_vertex not in self.adjacency_list[from_vertex]:
            self.adjacency_list[from_vertex].append(to_vertex)

    def get_neighbors(self, vertex: str) -> list[str]:
        """Соседи вершины (для неизвестной — пустой список)."""
        return self.adjacency_list.get(vertex, [])

    def has_vertex(self, vertex: str) -> bool:
        """Есть ли вершина."""
        return vertex in self.adjacency_list

    def __repr__(self) -> str:
        lines = ["DirectedGraph:"]
        for vertex in sorted(self.adjacency_list):
            neighbors = ", ".join(self.adjacency_list[vertex]) or "—"
            lines.append(f"  {vertex} -> [{neighbors}]")
        return "\n".join(lines)


def bfs(graph: DirectedGraph, start: str) -> list[str]:
    """Обход в ширину от start."""
    if not graph.has_vertex(start):
        return []
    visited = {start}
    queue: deque[str] = deque([start])
    order: list[str] = []
    while queue:
        current = queue.popleft()
        order.append(current)
        for neighbor in graph.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


class AdjacencyMatrixGraph:
    """Граф на матрице смежности."""

    def __init__(self) -> None:
        self.vertices: list[str] = []
        self.matrix: list[list[int]] = []

    def add_vertex(self, vertex: str) -> None:
        """Добавить вершину: новая строка и новый столбец из нулей."""
        if vertex in self.vertices:
            return
        for row in self.matrix:
            row.append(0)
        self.vertices.append(vertex)
        self.matrix.append([0] * len(self.vertices))

    def add_edge(self, from_vertex: str, to_vertex: str) -> None:
        """Добавить ребро."""
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        i = self.vertices.index(from_vertex)
        j = self.vertices.index(to_vertex)
        self.matrix[i][j] = 1

    def has_edge(self, from_vertex: str, to_vertex: str) -> bool:
        """Есть ли ребро."""
        if from_vertex not in self.vertices or to_vertex not in self.vertices:
            return False
        return self.matrix[self.vertices.index(from_vertex)][self.vertices.index(to_vertex)] == 1


def edges_to_adjacency_matrix(edges: list[tuple[str, str]]) -> AdjacencyMatrixGraph:
    """Построить граф на матрице по списку рёбер."""
    graph = AdjacencyMatrixGraph()
    for from_vertex, to_vertex in edges:
        graph.add_edge(from_vertex, to_vertex)
    return graph


def shortest_path_length(graph: DirectedGraph, start: str, goal: str) -> int:
    """Наименьшее число рёбер от start до goal или -1."""
    if not graph.has_vertex(start) or not graph.has_vertex(goal):
        return -1
    distance = {start: 0}
    queue: deque[str] = deque([start])
    while queue:
        current = queue.popleft()
        if current == goal:
            return distance[current]
        for neighbor in graph.get_neighbors(current):
            if neighbor not in distance:
                distance[neighbor] = distance[current] + 1
                queue.append(neighbor)
    return -1


def has_path(
    graph: dict[str, list[str]], start: str, goal: str, visited: set[str] | None = None
) -> bool:
    """Есть ли путь (исправлено: вершину нужно помечать посещённой)."""
    if visited is None:
        visited = set()
    if start == goal:
        return True
    visited.add(start)
    for neighbor in graph.get(start, []):
        if neighbor not in visited and has_path(graph, neighbor, goal, visited):
            return True
    return False
