from __future__ import annotations

import unittest

from demos.civilization.ai import choose_action
from demos.civilization.config import BUILDINGS
from demos.civilization.engine import CivilizationGame
from demos.civilization.models import Action
from demos.civilization.rules import apply_action, can_build_building, can_build_city, score
from shared.random_utils import make_rng


class CivilizationTests(unittest.TestCase):
    def test_illegal_city_on_mountain(self) -> None:
        game = CivilizationGame(make_rng(0), size=5, max_turns=2)
        game.state.terrain[0][0] = "M"
        allowed, _ = can_build_city(game.state, 0, 0)
        self.assertFalse(allowed)

    def test_repeat_building_is_illegal(self) -> None:
        game = CivilizationGame(make_rng(1), size=5, max_turns=3)
        city_id = next(iter(game.state.cities))
        game.state.techs.add("agriculture")
        game.state.resources["wood"] = 10
        apply_action(game.state, Action(kind="build_building", city_id=city_id, name="farm"))
        allowed, _ = can_build_building(game.state, city_id, "farm")
        self.assertFalse(allowed)

    def test_auto_game_reaches_terminal(self) -> None:
        game = CivilizationGame(make_rng(2), size=6, max_turns=10)
        while not game.state.is_terminal:
            action = choose_action(game.state)
            apply_action(game.state, action)
        self.assertEqual(game.state.turn, 10)
        self.assertIsInstance(score(game.state), int)


if __name__ == "__main__":
    unittest.main()
