from __future__ import annotations

from demos.bomberman.config import BLAST_RADIUS
from demos.bomberman.models import Bomb, GameState, Player


DIRECTIONS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}


def in_bounds(state: GameState, x: int, y: int) -> bool:
    return 0 <= x < state.width and 0 <= y < state.height


def bomb_positions(state: GameState) -> set[tuple[int, int]]:
    return {(bomb.x, bomb.y) for bomb in state.bombs}


def is_blocked(state: GameState, x: int, y: int) -> bool:
    return (x, y) in state.walls or (x, y) in state.boxes or (x, y) in bomb_positions(state)


def is_legal_action(state: GameState, player_id: str, action: str) -> bool:
    player = state.players[player_id]
    if not player.alive:
        return False
    if action in DIRECTIONS:
        dx, dy = DIRECTIONS[action]
        nx, ny = player.x + dx, player.y + dy
        if not in_bounds(state, nx, ny):
            return False
        if is_blocked(state, nx, ny):
            return False
        if any(other.alive and other.player_id != player_id and (other.x, other.y) == (nx, ny) for other in state.players.values()):
            return False
        return True
    if action == "bomb":
        return (player.x, player.y) not in bomb_positions(state)
    if action == "wait":
        return True
    return False


def blast_cells(state: GameState, bomb: Bomb) -> set[tuple[int, int]]:
    cells = {(bomb.x, bomb.y)}
    for dx, dy in DIRECTIONS.values():
        for step in range(1, BLAST_RADIUS + 1):
            nx = bomb.x + dx * step
            ny = bomb.y + dy * step
            if not in_bounds(state, nx, ny):
                break
            if (nx, ny) in state.walls:
                break
            cells.add((nx, ny))
            if (nx, ny) in state.boxes:
                break
    return cells


def danger_cells(state: GameState, timers: set[int] | None = None) -> set[tuple[int, int]]:
    timers = timers or {1}
    cells: set[tuple[int, int]] = set()
    for bomb in state.bombs:
        if bomb.timer in timers:
            cells |= blast_cells(state, bomb)
    return cells
