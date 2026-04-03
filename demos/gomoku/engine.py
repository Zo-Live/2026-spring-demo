from __future__ import annotations

from dataclasses import dataclass

from demos.gomoku.board import BLACK, Board
from demos.gomoku.rules import is_draw, is_legal_move, move_wins, opponent


@dataclass
class GomokuState:
    board: Board
    current_player: str = BLACK
    winner: str | None = None
    draw: bool = False
    move_count: int = 0
    last_move: tuple[int, int] | None = None

    @property
    def is_terminal(self) -> bool:
        return self.winner is not None or self.draw


class GomokuGame:
    def __init__(self, size: int, win_length: int) -> None:
        self.win_length = win_length
        self.state = GomokuState(board=Board.create(size))

    def legal_moves(self) -> list[tuple[int, int]]:
        return self.state.board.empty_cells()

    def apply_move(self, x: int, y: int) -> None:
        if self.state.is_terminal:
            raise ValueError("game already finished")
        if not is_legal_move(self.state.board, x, y):
            raise ValueError("illegal move")
        player = self.state.current_player
        self.state.board.place(x, y, player)
        self.state.move_count += 1
        self.state.last_move = (x, y)
        if move_wins(self.state.board, x, y, player, self.win_length):
            self.state.winner = player
        elif is_draw(self.state.board, self.win_length):
            self.state.draw = True
        else:
            self.state.current_player = opponent(player)
