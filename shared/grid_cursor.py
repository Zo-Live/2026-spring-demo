from __future__ import annotations

import curses
from collections.abc import Callable


CellRenderer = Callable[[int, int], str]
Selectable = Callable[[int, int], bool]


def _safe_addstr(stdscr: curses.window, y: int, x: int, text: str, attr: int = 0) -> None:
    height, width = stdscr.getmaxyx()
    if y < 0 or y >= height or x >= width:
        return
    available = max(0, width - x - 1)
    if available <= 0:
        return
    clipped = text[:available]
    try:
        if attr:
            stdscr.addstr(y, x, clipped, attr)
        else:
            stdscr.addstr(y, x, clipped)
    except curses.error:
        return


def _draw_lines(stdscr: curses.window, lines: list[str], selected_row: int) -> None:
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    for index, line in enumerate(lines[: height - 1]):
        if index == selected_row:
            _safe_addstr(stdscr, index, 0, line, curses.A_REVERSE)
        else:
            _safe_addstr(stdscr, index, 0, line)
    stdscr.refresh()


def select_menu_curses(title: str, options: list[str], initial_index: int = 0) -> int | None:
    def _inner(stdscr: curses.window) -> int | None:
        curses.curs_set(0)
        index = max(0, min(initial_index, len(options) - 1))
        title_lines = title.splitlines() or [title]
        while True:
            lines = [*title_lines, "", *[f" {option}" for option in options], "", "Use arrows, Enter to confirm, q to cancel."]
            _draw_lines(stdscr, lines, index + len(title_lines) + 1)
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
    decorate_unselectable: bool = True,
    selected_style: str = "brackets",
) -> tuple[int, int] | None:
    footer_lines = footer_lines or []

    def _inner(stdscr: curses.window) -> tuple[int, int] | None:
        curses.curs_set(0)
        title_lines = title.splitlines() or [title]
        x, y = initial
        while not selectable(x, y):
            x = (x + 1) % width
            if x == 0:
                y = (y + 1) % height
            if (x, y) == initial:
                return None

        while True:
            stdscr.clear()
            for index, line in enumerate(title_lines):
                _safe_addstr(stdscr, index, 0, line)
            _safe_addstr(stdscr, len(title_lines), 0, "Use arrows, Enter to confirm, q to cancel.")
            grid_start = len(title_lines) + 2
            for row in range(height):
                parts: list[str] = []
                for col in range(width):
                    cell = renderer(col, row)
                    if col == x and row == y:
                        if selected_style == "reverse":
                            parts.append(f" {cell} ")
                        else:
                            parts.append(f"[{cell}]")
                    elif selectable(col, row):
                        parts.append(f" {cell} ")
                    else:
                        parts.append(f"({cell})" if decorate_unselectable else f" {cell} ")
                line = " ".join(parts)
                if selected_style == "reverse" and row == y:
                    prefix_parts: list[str] = []
                    selected_text = ""
                    suffix_parts: list[str] = []
                    for col in range(width):
                        cell_text = parts[col]
                        if col < x:
                            prefix_parts.append(cell_text)
                        elif col == x:
                            selected_text = cell_text
                        else:
                            suffix_parts.append(cell_text)
                    prefix = " ".join(prefix_parts)
                    suffix = " ".join(suffix_parts)
                    xpos = 0
                    if prefix:
                        _safe_addstr(stdscr, grid_start + row, 0, prefix)
                        xpos = len(prefix) + 1
                    _safe_addstr(stdscr, grid_start + row, xpos, selected_text, curses.A_REVERSE)
                    if suffix:
                        _safe_addstr(stdscr, grid_start + row, xpos + len(selected_text) + 1, suffix)
                else:
                    _safe_addstr(stdscr, grid_start + row, 0, line)
            for offset, line in enumerate(footer_lines):
                _safe_addstr(stdscr, grid_start + height + 1 + offset, 0, line)
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
