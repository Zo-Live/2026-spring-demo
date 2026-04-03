from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Player:
    player_id: str
    x: int
    y: int
    alive: bool = True
    last_action: str = "idle"


@dataclass
class Bomb:
    x: int
    y: int
    timer: int
    owner: str


@dataclass
class GameState:
    width: int
    height: int
    walls: set[tuple[int, int]]
    boxes: set[tuple[int, int]]
    monsters: set[tuple[int, int]]
    bombs: list[Bomb]
    players: dict[str, Player]
    round_index: int = 0
    max_rounds: int = 60
    winner: str | None = None
    draw: bool = False
    log: list[str] = field(default_factory=list)

    @property
    def is_terminal(self) -> bool:
        return self.winner is not None or self.draw or self.round_index >= self.max_rounds
