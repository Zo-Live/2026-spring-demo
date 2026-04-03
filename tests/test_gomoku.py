from __future__ import annotations

import unittest

from demos.gomoku.ai import choose_move
from demos.gomoku.board import BLACK, WHITE, Board
from demos.gomoku.engine import GomokuGame
from demos.gomoku.rules import is_legal_move, move_wins, winner


class GomokuTests(unittest.TestCase):
    def test_illegal_repeat_move(self) -> None:
        game = GomokuGame(size=5, win_length=5)
        game.apply_move(0, 0)
        with self.assertRaises(ValueError):
            game.apply_move(0, 0)

    def test_horizontal_win(self) -> None:
        board = Board.create(5)
        for x in range(5):
            board.place(x, 0, BLACK)
        self.assertEqual(winner(board, 5), BLACK)
        self.assertTrue(move_wins(board, 2, 0, BLACK, 5))

    def test_ai_blocks_win(self) -> None:
        board = Board.create(7)
        for x in range(4):
            board.place(x, 0, BLACK)
        move = choose_move(board, WHITE, 5)
        self.assertEqual(move, (4, 0))

    def test_auto_game_terminates(self) -> None:
        game = GomokuGame(size=5, win_length=4)
        while not game.state.is_terminal:
            move = choose_move(game.state.board, game.state.current_player, game.win_length)
            self.assertTrue(is_legal_move(game.state.board, *move))
            game.apply_move(*move)
        self.assertTrue(game.state.winner is not None or game.state.draw)


if __name__ == "__main__":
    unittest.main()
