from __future__ import annotations

from dataclasses import dataclass, field


EMPTY = "."
BLACK = "B"
WHITE = "W"


@dataclass
class Board:
    size: int
    grid: list[list[str]] = field(default_factory=list)

    @classmethod
    def create(cls, size: int) -> "Board":
        return cls(size=size, grid=[[EMPTY for _ in range(size)] for _ in range(size)])

    def copy(self) -> "Board":
        return Board(size=self.size, grid=[row[:] for row in self.grid])

    def get(self, x: int, y: int) -> str:
        return self.grid[y][x]

    def place(self, x: int, y: int, stone: str) -> None:
        self.grid[y][x] = stone

    def empty_cells(self) -> list[tuple[int, int]]:
        return [(x, y) for y in range(self.size) for x in range(self.size) if self.grid[y][x] == EMPTY]

    def occupied_cells(self) -> list[tuple[int, int]]:
        return [(x, y) for y in range(self.size) for x in range(self.size) if self.grid[y][x] != EMPTY]
