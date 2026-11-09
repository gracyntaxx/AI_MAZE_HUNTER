"""Grid search algorithms with a shared result format."""

from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count
from typing import Callable, Iterable, Sequence

Position = tuple[int, int]
Grid = Sequence[Sequence[str]]


@dataclass(frozen=True)
class SearchResult:
    path: list[Position]
    explored: int

    @property
    def found(self) -> bool:
        return bool(self.path)

    @property
    def path_length(self) -> int:
        return max(0, len(self.path) - 1)


def valid_neighbors(grid: Grid, position: Position) -> Iterable[Position]:
    rows, cols = len(grid), len(grid[0])
    row, col = position
    for next_position in (
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    ):
        next_row, next_col = next_position
        if (
            0 <= next_row < rows
            and 0 <= next_col < cols
            and grid[next_row][next_col] != "#"
        ):
            yield next_position


def _reconstruct(
    parents: dict[Position, Position],
    source: Position,
    target: Position,
) -> list[Position]:
    if target != source and target not in parents:
        return []
    path = [target]
    while path[-1] != source:
        path.append(parents[path[-1]])
    path.reverse()
    return path


def _validate(grid: Grid, source: Position, target: Position) -> None:
    if not grid or not grid[0] or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("Grid must be a non-empty rectangle.")
    rows, cols = len(grid), len(grid[0])
    for position in (source, target):
        row, col = position
        if not (0 <= row < rows and 0 <= col < cols):
            raise ValueError(f"Position {position} is outside the grid.")
        if grid[row][col] == "#":
            raise ValueError(f"Position {position} is a wall.")


def bfs(grid: Grid, source: Position, target: Position) -> SearchResult:
    """Find a shortest path in an unweighted grid using a FIFO queue."""
    _validate(grid, source, target)
    queue = deque([source])
    visited = {source}
    parents: dict[Position, Position] = {}
    while queue:
        current = queue.popleft()
        if current == target:
            break
        for neighbor in valid_neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parents[neighbor] = current
                queue.append(neighbor)
    return SearchResult(_reconstruct(parents, source, target), len(visited))


def dfs(grid: Grid, source: Position, target: Position) -> SearchResult:
    """Find a path using a stack; the returned route is not guaranteed shortest."""
    _validate(grid, source, target)
    stack = [source]
    visited = {source}
    parents: dict[Position, Position] = {}
    while stack:
        current = stack.pop()
        if current == target:
            break
        for neighbor in valid_neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parents[neighbor] = current
                stack.append(neighbor)
    return SearchResult(_reconstruct(parents, source, target), len(visited))


def manhattan_distance(first: Position, second: Position) -> int:
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


def astar(grid: Grid, source: Position, target: Position) -> SearchResult:
    """Find an optimal four-directional route using A* and Manhattan distance."""
    _validate(grid, source, target)
    tie_breaker = count()
    frontier: list[tuple[int, int, int, Position]] = []
    heappush(frontier, (manhattan_distance(source, target), 0, next(tie_breaker), source))
    parents: dict[Position, Position] = {}
    costs = {source: 0}
    closed: set[Position] = set()

    while frontier:
        _, current_cost, _, current = heappop(frontier)
        if current in closed:
            continue
        if current == target:
            break
        closed.add(current)
        for neighbor in valid_neighbors(grid, current):
            new_cost = current_cost + 1
            if new_cost < costs.get(neighbor, float("inf")):
                costs[neighbor] = new_cost
                parents[neighbor] = current
                priority = new_cost + manhattan_distance(neighbor, target)
                heappush(frontier, (priority, new_cost, next(tie_breaker), neighbor))
    return SearchResult(_reconstruct(parents, source, target), len(closed) + int(source == target))
