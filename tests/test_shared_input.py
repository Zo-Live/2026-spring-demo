from __future__ import annotations

import unittest

from shared.cursor_input import select_grid, select_menu


class SharedInputSmokeTests(unittest.TestCase):
    def test_module_exports(self) -> None:
        self.assertTrue(callable(select_menu))
        self.assertTrue(callable(select_grid))


if __name__ == "__main__":
    unittest.main()
