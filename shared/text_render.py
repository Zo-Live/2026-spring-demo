from __future__ import annotations

from collections.abc import Iterable


def render_table(lines: Iterable[str]) -> str:
    return "\n".join(lines)


def render_grid(rows: list[list[str]], row_labels: bool = True, col_labels: bool = True) -> str:
    if not rows:
        return ""
    width = max(len(cell) for row in rows for cell in row)
    formatted: list[str] = []
    if col_labels:
        header = [" " * (3 if row_labels else 0)]
        header.extend(f"{index:>{width}}" for index in range(len(rows[0])))
        formatted.append(" ".join(header))
    for y, row in enumerate(rows):
        cells = [f"{cell:>{width}}" for cell in row]
        if row_labels:
            formatted.append(f"{y:>2} " + " ".join(cells))
        else:
            formatted.append(" ".join(cells))
    return "\n".join(formatted)
