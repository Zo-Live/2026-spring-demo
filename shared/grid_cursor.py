from __future__ import annotations

import curses
from collections.abc import Callable


CellRenderer = Callable[[int, int], str]
Selectable = Callable[[int, int], bool]


def _draw_lines(stdscr: curses.window, lines: list[str], selected_row: int) -> None:
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    for index, line in enumerate(lines[: height - 1]):
        text = line[: max(1, width - 1)]
        if index == selected_row:
            stdscr.addstr(index, 0, text, curses.A_REVERSE)
        else:
            stdscr.addstr(index, 0, text)
    stdscr.refresh()


def select_menu_curses(title: str, options: list[str], initial_index: int = 0) -> int | None:
    def _inner(stdscr: curses.window) -> int | None:
        curses.curs_set(0)
        index = max(0, min(initial_index, len(options) - 1))
        while True:
            lines = [title, "", *[f" {option}" for option in options], "", "Use arrows, Enter to confirm, q to cancel."]
            _draw_lines(stdscr, lines, index + 2)
            key = stdscr.getch()
            if key in (curses.KEY_UP, ord("k")):
                index = (index - 1) % len(options)
            elif key in (curses.KEY_DOWN, ord("j")):
                index = (index + 1) % len(options)
            elif key in (curses.KEY_ENTER, 10, 13):
                return index
            elif key in (ord("q"), 27):
                return None

    return curses.wrapper(_inner)


def select_grid_curses(
    title: str,
    width: int,
    height: int,
    renderer: CellRenderer,
    selectable: Selectable,
    initial: tuple[int, int] = (0, 0),
    footer_lines: list[str] | None = None,
) -> tuple[int, int] | None:
    footer_lines = footer_lines or []

    def _inner(stdscr: curses.window) -> tuple[int, int] | None:
        curses.curs_set(0)
        x, y = initial
        while not selectable(x, y):
            x = (x + 1) % width
            if x == 0:
                y = (y + 1) % height
            if (x, y) == initial:
                return None

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, title)
            stdscr.addstr(1, 0, "Use arrows, Enter to confirm, q to cancel.")
            for row in range(height):
                parts: list[str] = []
                for col in range(width):
                    cell = renderer(col, row)
                    if col == x and row == y:
                        parts.append(f"[{cell}]")
                    elif selectable(col, row):
                        parts.append(f" {cell} ")
                    else:
                        parts.append(f"({cell})")
                stdscr.addstr(3 + row, 0, " ".join(parts))
            for offset, line in enumerate(footer_lines):
                stdscr.addstr(4 + height + offset, 0, line)
            stdscr.refresh()
            key = stdscr.getch()
            if key in (curses.KEY_LEFT, ord("h")):
                x = (x - 1) % width
            elif key in (curses.KEY_RIGHT, ord("l")):
                x = (x + 1) % width
            elif key in (curses.KEY_UP, ord("k")):
                y = (y - 1) % height
            elif key in (curses.KEY_DOWN, ord("j")):
                y = (y + 1) % height
            elif key in (curses.KEY_ENTER, 10, 13):
                if selectable(x, y):
                    return (x, y)
            elif key in (ord("q"), 27):
                return None

    return curses.wrapper(_inner)
