"""Модуль 8 · Графы. Допишите код и запустите: pytest m08-graphs"""

from __future__ import annotations


class DirectedGraph:
    """Задание 1. Ориентированный граф: список смежности «вершина → список соседей».

    Данные храните в словаре self.adjacency_list: {вершина: [соседи в порядке добавления]}.
    """

    def __init__(self) -> None:
        # TODO: заведите пустой словарь self.adjacency_list
        raise NotImplementedError

    def add_vertex(self, vertex: str) -> None:
        """Добавить вершину. Если она уже есть — ничего не меняется."""
        raise NotImplementedError

    def add_edge(self, from_vertex: str, to_vertex: str) -> None:
        """Добавить ребро from -> to. Недостающие вершины создаются сами. Повторы не нужны."""
        raise NotImplementedError

    def get_neighbors(self, vertex: str) -> list[str]:
        """Соседи вершины. Для неизвестной вершины — пустой список."""
        raise NotImplementedError

    def has_vertex(self, vertex: str) -> bool:
        """Есть ли вершина в графе."""
        raise NotImplementedError


def bfs(graph: DirectedGraph, start: str) -> list[str]:
    """Задание 2. Обход в ширину от start: список вершин в порядке посещения.

    Каждую вершину посещаем один раз (нужно множество visited). Если start нет в графе — [].
    """
    # TODO: очередь deque, множество visited, цикл «снять — записать — добавить новых соседей»
    raise NotImplementedError


class AdjacencyMatrixGraph:
    """Задание 3. Граф на матрице смежности.

    Атрибуты: self.vertices — список вершин в порядке добавления;
    self.matrix — квадратная таблица 0/1: matrix[i][j] == 1, если есть ребро
    из vertices[i] в vertices[j].
    """

    def __init__(self) -> None:
        raise NotImplementedError

    def add_vertex(self, vertex: str) -> None:
        """Добавить вершину (новая строка и новый столбец из нулей). Повтор — ничего не делает."""
        raise NotImplementedError

    def add_edge(self, from_vertex: str, to_vertex: str) -> None:
        """Добавить ребро; недостающие вершины создаются сами."""
        raise NotImplementedError

    def has_edge(self, from_vertex: str, to_vertex: str) -> bool:
        """Есть ли ребро. Если вершины нет — False."""
        raise NotImplementedError


def edges_to_adjacency_matrix(edges: list[tuple[str, str]]) -> AdjacencyMatrixGraph:
    """Задание 3б. Построить граф на матрице по списку рёбер [(откуда, куда), ...]."""
    raise NotImplementedError


def shortest_path_length(graph: DirectedGraph, start: str, goal: str) -> int:
    """Задание 4 («метро»). Наименьшее число рёбер (пересадок) от start до goal.

    Если пути нет или вершины неизвестны — -1. Подсказка: BFS идёт «волнами».
    """
    raise NotImplementedError


def has_path(
    graph: dict[str, list[str]], start: str, goal: str, visited: set[str] | None = None
) -> bool:
    """Задание 5 («найди ошибку»). Есть ли путь из start в goal в графе-словаре.

    Функция написана, но на графах с циклами «зависает» до RecursionError.
    Найдите ошибку и исправьте её.
    """
    if visited is None:
        visited = set()
    if start == goal:
        return True
    for neighbor in graph.get(start, []):
        if neighbor not in visited and has_path(graph, neighbor, goal, visited):
            return True
    return False
