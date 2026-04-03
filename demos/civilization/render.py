from __future__ import annotations

from demos.civilization.models import GameState
from demos.civilization.rules import projected_output, score
from shared.text_render import render_grid


def render_map(state: GameState) -> str:
    rows: list[list[str]] = []
    for y in range(state.height):
        row: list[str] = []
        for x in range(state.width):
            cell = state.terrain[y][x]
            city_here = next((city.city_id for city in state.cities.values() if city.x == x and city.y == y), None)
            if city_here is not None:
                row.append(f"C{city_here}")
            else:
                row.append(f" {cell}")
        rows.append(row)
    return render_grid(rows)


def render_summary(state: GameState) -> str:
    output = projected_output(state)
    city_lines = [
        f"City {city.city_id} at ({city.x},{city.y}) buildings={sorted(city.buildings)}"
        for city in state.cities.values()
    ]
    return "\n".join(
        [
            f"Turn {state.turn}/{state.max_turns}",
            f"Resources: {state.resources}",
            f"Per-turn output: {output}",
            f"Techs: {sorted(state.techs)}",
            f"Score: {score(state)}",
            "Cities:",
            *city_lines,
        ]
    )
