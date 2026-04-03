from __future__ import annotations

import sys
from collections.abc import Callable

from shared.grid_cursor import select_grid_curses, select_menu_curses


def _supports_curses() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def select_menu(title: str, options: list[str], initial_index: int = 0) -> int | None:
    if not options:
        return None
    if _supports_curses():
        return select_menu_curses(title, options, initial_index)
    print(title)
    for index, option in enumerate(options):
        print(f"{index}: {option}")
    raw = input("Select option index (blank to cancel): ").strip()
    if not raw:
        return None
    return int(raw)


def select_grid(
    title: str,
    width: int,
    height: int,
    renderer: Callable[[int, int], str],
    selectable: Callable[[int, int], bool],
    initial: tuple[int, int] = (0, 0),
    footer_lines: list[str] | None = None,
    decorate_unselectable: bool = True,
    selected_style: str = "brackets",
) -> tuple[int, int] | None:
    if _supports_curses():
        return select_grid_curses(title, width, height, renderer, selectable, initial, footer_lines, decorate_unselectable, selected_style)
    print(title)
    if footer_lines:
        for line in footer_lines:
            print(line)
    while True:
        raw = input("Enter x,y (blank to cancel): ").strip()
        if not raw:
            return None
        x_str, y_str = raw.split(",", 1)
        coord = (int(x_str), int(y_str))
        if selectable(*coord):
            return coord
        print("Invalid selection.")
