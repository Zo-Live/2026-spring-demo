from __future__ import annotations

from demos.civilization.models import GameState
from demos.civilization.rules import projected_output, score
from shared.text_render import render_grid


TERRAIN_EMOJI = {
    "P": "🌾",
    "F": "🌲",
    "M": "⛰️",
    "R": "🌊",
    "X": "🪨",
}


def render_map(state: GameState) -> str:
    rows: list[list[str]] = []
    for y in range(state.height):
        row: list[str] = []
        for x in range(state.width):
            cell = state.terrain[y][x]
            city_here = next((city.city_id for city in state.cities.values() if city.x == x and city.y == y), None)
            if city_here is not None:
                row.append(f"🏙️{city_here}")
            else:
                row.append(TERRAIN_EMOJI[cell])
        rows.append(row)
    return render_grid(rows)


def render_summary(state: GameState) -> str:
    output = projected_output(state)
    city_lines = [
        f"🏙️ City {city.city_id} at ({city.x},{city.y}) buildings={sorted(city.buildings) if city.buildings else ['none']}"
        for city in state.cities.values()
    ]
    return "\n".join(
        [
            f"Turn {state.turn}/{state.max_turns}   Score {score(state)}",
            (
                f"Resources  🍞 {state.resources['food']}  🪵 {state.resources['wood']}  "
                f"⛏️ {state.resources['ore']}  🔬 {state.resources['science']}"
            ),
            (
                f"Per turn   🍞 {output['food']}  🪵 {output['wood']}  "
                f"⛏️ {output['ore']}  🔬 {output['science']}"
            ),
            f"Techs: {sorted(state.techs) if state.techs else ['none']}",
            "Cities:",
            *city_lines,
        ]
    )


def render_dashboard(state: GameState, footer: list[str] | None = None) -> str:
    footer = footer or []
    parts = [render_summary(state), "", render_map(state)]
    if footer:
        parts.extend(["", *footer])
    return "\n".join(parts)
