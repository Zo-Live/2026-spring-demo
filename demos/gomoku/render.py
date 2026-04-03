from __future__ import annotations

from demos.gomoku.board import Board
from shared.text_render import render_grid


def render_board(board: Board, last_move: tuple[int, int] | None = None) -> str:
    rows: list[list[str]] = []
    for y in range(board.size):
        row: list[str] = []
        for x in range(board.size):
            cell = board.get(x, y)
            if last_move == (x, y):
                row.append(f"*{cell}")
            else:
                row.append(f" {cell}")
        rows.append(row)
    return render_grid(rows)
