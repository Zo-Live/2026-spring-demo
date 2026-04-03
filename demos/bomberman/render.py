from __future__ import annotations

from demos.bomberman.models import GameState
from shared.text_render import render_grid


def render_board(state: GameState) -> str:
    rows = [[" ." for _ in range(state.width)] for _ in range(state.height)]
    for x, y in state.walls:
        rows[y][x] = " #"
    for x, y in state.boxes:
        rows[y][x] = " +"
    for x, y in state.monsters:
        rows[y][x] = " M"
    for bomb in state.bombs:
        rows[bomb.y][bomb.x] = f" {bomb.timer}"
    for player in state.players.values():
        marker = player.player_id[-1] if player.alive else "x"
        rows[player.y][player.x] = f" {marker}"
    return render_grid(rows)


def render_summary(state: GameState) -> str:
    lines = [f"Round {state.round_index}/{state.max_rounds}", f"Monsters: {len(state.monsters)}", f"Bombs: {[(bomb.x, bomb.y, bomb.timer) for bomb in state.bombs]}"]
    for player in state.players.values():
        lines.append(f"{player.player_id}: pos=({player.x},{player.y}) alive={player.alive} last_action={player.last_action}")
    if state.log:
        lines.append("Events:")
        lines.extend(state.log)
    return "\n".join(lines)
