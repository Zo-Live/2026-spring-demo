from __future__ import annotations

from demos.gomoku.board import EMPTY, Board
from demos.gomoku.rules import is_legal_move, move_wins, opponent


DIRECTIONS = ((1, 0), (0, 1), (1, 1), (1, -1))


def _contiguous_line_score(board: Board, x: int, y: int, player: str, win_length: int) -> int:
    total = 0
    for dx, dy in DIRECTIONS:
        left = 0
        right = 0
        lx, ly = x - dx, y - dy
        while 0 <= lx < board.size and 0 <= ly < board.size and board.get(lx, ly) == player:
            left += 1
            lx -= dx
            ly -= dy
        rx, ry = x + dx, y + dy
        while 0 <= rx < board.size and 0 <= ry < board.size and board.get(rx, ry) == player:
            right += 1
            rx += dx
            ry += dy

        run = left + 1 + right
        open_ends = 0
        if 0 <= lx < board.size and 0 <= ly < board.size and board.get(lx, ly) == EMPTY:
            open_ends += 1
        if 0 <= rx < board.size and 0 <= ry < board.size and board.get(rx, ry) == EMPTY:
            open_ends += 1

        if run >= win_length:
            total += 1_000_000
        elif run == win_length - 1 and open_ends == 2:
            total += 120_000
        elif run == win_length - 1 and open_ends == 1:
            total += 35_000
        elif run == win_length - 2 and open_ends == 2:
            total += 15_000
        elif run == win_length - 2 and open_ends == 1:
            total += 3_500
        elif run == win_length - 3 and open_ends == 2:
            total += 600
        else:
            total += run * run * 8 + open_ends * 3
    return total


def _adjacency_score(board: Board, x: int, y: int, player: str) -> int:
    nearby = 0
    owned = 0
    for dy in (-2, -1, 0, 1, 2):
        for dx in (-2, -1, 0, 1, 2):
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
    centrality = board.size * 2 - (abs(center - x) + abs(center - y))
    return nearby * 6 + owned * 10 + centrality


def _candidate_moves(board: Board) -> list[tuple[int, int]]:
    occupied = board.occupied_cells()
    if not occupied:
        center = board.size // 2
        return [(center, center)]

    candidates: set[tuple[int, int]] = set()
    for ox, oy in occupied:
        for dy in (-2, -1, 0, 1, 2):
            for dx in (-2, -1, 0, 1, 2):
                nx, ny = ox + dx, oy + dy
                if 0 <= nx < board.size and 0 <= ny < board.size and board.get(nx, ny) == EMPTY:
                    candidates.add((nx, ny))
    return sorted(candidates)


def _find_forced_move(board: Board, player: str, win_length: int) -> tuple[int, int] | None:
    for x, y in _candidate_moves(board):
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
    best_score: tuple[int, int, int] | None = None
    rival = opponent(player)
    for x, y in _candidate_moves(board):
        if not is_legal_move(board, x, y):
            continue
        offense_board = board.copy()
        offense_board.place(x, y, player)
        offense = _contiguous_line_score(offense_board, x, y, player, win_length)

        defense_board = board.copy()
        defense_board.place(x, y, rival)
        defense = _contiguous_line_score(defense_board, x, y, rival, win_length)

        score = (max(offense, defense * 2), offense + defense, _adjacency_score(board, x, y, player))
        if best_score is None or score > best_score:
            best_score = score
            best_move = (x, y)
    if best_move is None:
        raise RuntimeError("AI could not find a legal move")
    return best_move
