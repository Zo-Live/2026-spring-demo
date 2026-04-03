from __future__ import annotations

import unicodedata

from demos.bomberman.models import GameState


TILE = {
    "wall": "🧱",
    "box": "📦",
    "monster": "👾",
    "p1": "🙂",
    "p2": "🤖",
    "dead": "💀",
    "empty": "·",
    "bomb": "💣",
}


def _cell_width(text: str) -> int:
    return sum(2 if unicodedata.east_asian_width(ch) in "FWW" else 1 for ch in text)


def _pad_cell(text: str, width: int) -> str:
    w = _cell_width(text)
    if w >= width:
        return text
    return text + " " * (width - w)


def render_board(state: GameState) -> str:
    rows = [[TILE["empty"] for _ in range(state.width)] for _ in range(state.height)]
    for x, y in state.walls:
        rows[y][x] = TILE["wall"]
    for x, y in state.boxes:
        rows[y][x] = TILE["box"]
    for x, y in state.monsters:
        rows[y][x] = TILE["monster"]
    for bomb in state.bombs:
        rows[bomb.y][bomb.x] = f"{TILE['bomb']}{bomb.timer}"
    for player in state.players.values():
        rows[player.y][player.x] = TILE["p1"] if player.player_id == "P1" and player.alive else TILE["p2"] if player.alive else TILE["dead"]
    header = "    " + " ".join(_pad_cell(str(i), 4) for i in range(state.width))
    lines = [header]
    for y, row in enumerate(rows):
        padded = [_pad_cell(cell, 4) for cell in row]
        lines.append(f"{y:>2}  " + " ".join(padded))
    return "\n".join(lines)


def render_summary(state: GameState) -> str:
    lines = [f"Round {state.round_index}/{state.max_rounds}", f"Monsters: {len(state.monsters)}", f"Bombs: {[(bomb.x, bomb.y, bomb.timer) for bomb in state.bombs]}"]
    for player in state.players.values():
        icon = TILE["p1"] if player.player_id == "P1" else TILE["p2"]
        lines.append(f"{icon} {player.player_id}: pos=({player.x},{player.y}) alive={player.alive} last_action={player.last_action}")
    if state.log:
        lines.append("Events:")
        lines.extend(state.log)
    return "\n".join(lines)


def render_compact_status(state: GameState) -> str:
    lines = [f"Round {state.round_index}/{state.max_rounds}  Monsters {len(state.monsters)}  Bombs {[(b.x, b.y, b.timer) for b in state.bombs]}"]
    for player in state.players.values():
        icon = TILE["p1"] if player.player_id == "P1" else TILE["p2"]
        lines.append(f"{icon} {player.player_id} ({player.x},{player.y}) alive={player.alive} last={player.last_action}")
    if state.log:
        lines.append(f"Latest: {state.log[-1]}")
    return "\n".join(lines)
