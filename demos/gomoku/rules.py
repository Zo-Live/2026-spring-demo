from __future__ import annotations

from demos.gomoku.board import BLACK, EMPTY, WHITE, Board


DIRECTIONS = ((1, 0), (0, 1), (1, 1), (1, -1))


def opponent(player: str) -> str:
    return WHITE if player == BLACK else BLACK


def is_on_board(board: Board, x: int, y: int) -> bool:
    return 0 <= x < board.size and 0 <= y < board.size


def is_legal_move(board: Board, x: int, y: int) -> bool:
    return is_on_board(board, x, y) and board.get(x, y) == EMPTY


def count_direction(board: Board, x: int, y: int, dx: int, dy: int, stone: str) -> int:
    total = 0
    cx, cy = x + dx, y + dy
    while is_on_board(board, cx, cy) and board.get(cx, cy) == stone:
        total += 1
        cx += dx
        cy += dy
    return total


def move_wins(board: Board, x: int, y: int, stone: str, win_length: int) -> bool:
    for dx, dy in DIRECTIONS:
        run = 1 + count_direction(board, x, y, dx, dy, stone) + count_direction(board, x, y, -dx, -dy, stone)
        if run >= win_length:
            return True
    return False


def winner(board: Board, win_length: int) -> str | None:
    for y in range(board.size):
        for x in range(board.size):
            stone = board.get(x, y)
            if stone != EMPTY and move_wins(board, x, y, stone, win_length):
                return stone
    return None


def is_draw(board: Board, win_length: int) -> bool:
    return winner(board, win_length) is None and not board.empty_cells()
