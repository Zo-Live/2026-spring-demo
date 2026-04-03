from __future__ import annotations

from demos.bomberman.models import GameState
from shared.text_render import render_grid


TILE = {
    "wall": "🧱",
    "box": "📦",
    "monster": "👾",
    "p1": "🙂",
    "p2": "🤖",
    "dead": "💀",
    "empty": "·",
}


def render_board(state: GameState) -> str:
    rows = [[TILE["empty"] for _ in range(state.width)] for _ in range(state.height)]
    for x, y in state.walls:
        rows[y][x] = TILE["wall"]
    for x, y in state.boxes:
        rows[y][x] = TILE["box"]
    for x, y in state.monsters:
        rows[y][x] = TILE["monster"]
    for bomb in state.bombs:
        rows[bomb.y][bomb.x] = f"💣{bomb.timer}"
    for player in state.players.values():
        rows[player.y][player.x] = TILE["p1"] if player.player_id == "P1" and player.alive else TILE["p2"] if player.alive else TILE["dead"]
    return render_grid(rows)


def render_summary(state: GameState) -> str:
    lines = [f"Round {state.round_index}/{state.max_rounds}", f"Monsters: {len(state.monsters)}", f"Bombs: {[(bomb.x, bomb.y, bomb.timer) for bomb in state.bombs]}"]
    for player in state.players.values():
        icon = TILE["p1"] if player.player_id == "P1" else TILE["p2"]
        lines.append(f"{icon} {player.player_id}: pos=({player.x},{player.y}) alive={player.alive} last_action={player.last_action}")
    if state.log:
        lines.append("Events:")
        lines.extend(state.log)
    return "\n".join(lines)
