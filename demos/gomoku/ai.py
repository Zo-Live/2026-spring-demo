from __future__ import annotations

from demos.gomoku.board import EMPTY, Board
from demos.gomoku.rules import is_legal_move, move_wins, opponent


def _adjacency_score(board: Board, x: int, y: int, player: str) -> tuple[int, int]:
    nearby = 0
    owned = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < board.size and 0 <= ny < board.size:
                stone = board.get(nx, ny)
                if stone != EMPTY:
                    nearby += 1
                if stone == player:
                    owned += 1
    center = board.size // 2
    centrality = -(abs(center - x) + abs(center - y))
    return (nearby + owned * 2, centrality)


def _find_forced_move(board: Board, player: str, win_length: int) -> tuple[int, int] | None:
    for x, y in board.empty_cells():
        trial = board.copy()
        trial.place(x, y, player)
        if move_wins(trial, x, y, player, win_length):
            return (x, y)
    return None


def choose_move(board: Board, player: str, win_length: int) -> tuple[int, int]:
    winning = _find_forced_move(board, player, win_length)
    if winning is not None:
        return winning

    blocking = _find_forced_move(board, opponent(player), win_length)
    if blocking is not None:
        return blocking

    best_move: tuple[int, int] | None = None
    best_score: tuple[int, int] | None = None
    for x, y in board.empty_cells():
        if not is_legal_move(board, x, y):
            continue
        score = _adjacency_score(board, x, y, player)
        if best_score is None or score > best_score:
            best_score = score
            best_move = (x, y)
    if best_move is None:
        raise RuntimeError("AI could not find a legal move")
    return best_move
