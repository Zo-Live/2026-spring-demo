from __future__ import annotations

import unittest

from demos.bomberman.ai import choose_action
from demos.bomberman.engine import BombermanGame
from demos.bomberman.models import Bomb
from demos.bomberman.rules import blast_cells, is_legal_action
from shared.random_utils import make_rng


class BombermanTests(unittest.TestCase):
    def test_wall_blocks_move(self) -> None:
        game = BombermanGame(make_rng(0), size=7, max_rounds=5, monster_count=0)
        game.state.boxes.add((1, 0))
        self.assertFalse(is_legal_action(game.state, "P1", "right"))
        self.assertTrue(is_legal_action(game.state, "P1", "down"))

    def test_blast_destroys_box(self) -> None:
        game = BombermanGame(make_rng(1), size=7, max_rounds=5, monster_count=0)
        game.state.boxes.add((1, 0))
        bomb = Bomb(0, 0, 0, "P1")
        self.assertIn((1, 0), blast_cells(game.state, bomb))

    def test_ai_returns_legal_action(self) -> None:
        game = BombermanGame(make_rng(2), size=7, max_rounds=5, monster_count=0)
        action = choose_action(game.state, "P1")
        self.assertTrue(is_legal_action(game.state, "P1", action))

    def test_auto_game_terminates(self) -> None:
        game = BombermanGame(make_rng(3), size=7, max_rounds=20, monster_count=1)
        while not game.state.is_terminal:
            game.step({"P1": choose_action(game.state, "P1"), "P2": choose_action(game.state, "P2")})
        self.assertTrue(game.state.winner is not None or game.state.draw)


if __name__ == "__main__":
    unittest.main()
