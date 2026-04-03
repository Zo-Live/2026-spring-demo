from __future__ import annotations

from dataclasses import dataclass, field


RESOURCE_KEYS = ("food", "wood", "ore", "science")


@dataclass
class City:
    city_id: int
    x: int
    y: int
    buildings: set[str] = field(default_factory=set)


@dataclass
class Action:
    kind: str
    coord: tuple[int, int] | None = None
    city_id: int | None = None
    name: str | None = None


@dataclass
class GameState:
    width: int
    height: int
    terrain: list[list[str]]
    resources: dict[str, int]
    techs: set[str]
    cities: dict[int, City]
    turn: int
    max_turns: int
    next_city_id: int
    log: list[str] = field(default_factory=list)

    @property
    def is_terminal(self) -> bool:
        return self.turn >= self.max_turns
