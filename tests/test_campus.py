from __future__ import annotations

import unittest

from demos.campus.engine import CampusGame
from demos.campus.rules import current_day_hour, distance_hours, is_open
from demos.campus.scheduler import choose_commands
from shared.random_utils import make_rng


class CampusTests(unittest.TestCase):
    def test_opening_hours(self) -> None:
        self.assertFalse(is_open("library", 23))
        self.assertTrue(is_open("library", 10))

    def test_distance_hours(self) -> None:
        self.assertEqual(distance_hours("dorm", "dorm", False), 0)
        self.assertGreaterEqual(distance_hours("dorm", "library", False), 1)

    def test_auto_scheduler_runs_full_horizon(self) -> None:
        game = CampusGame(make_rng(0))
        while not game.state.is_terminal:
            commands = choose_commands(game.state)
            game.step(commands)
        self.assertEqual(game.state.hour_index, 168)

    def test_fatigue_can_trigger(self) -> None:
        game = CampusGame(make_rng(1))
        student = game.state.students[0]
        student.energy = 1
        game.state.hour_index = 8
        student.location = "teaching"
        game.step({student.name: "teaching"})
        self.assertIn("fatigue", student.debuffs)


if __name__ == "__main__":
    unittest.main()
