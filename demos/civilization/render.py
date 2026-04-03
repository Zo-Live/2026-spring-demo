from __future__ import annotations

from demos.civilization.models import GameState
from demos.civilization.rules import projected_output, score


TERRAIN_EMOJI = {
    "P": "🌾",
    "F": "🌲",
    "M": "⛰️",
    "R": "🌊",
    "X": "🪨",
}


def render_map(state: GameState) -> str:
    header = "    " + "".join(f"{x:^5}" for x in range(state.width))
    lines = [header]
    for y in range(state.height):
        cells: list[str] = []
        for x in range(state.width):
            cell = state.terrain[y][x]
            city_here = next((city.city_id for city in state.cities.values() if city.x == x and city.y == y), None)
            if city_here is not None:
                cells.append(" 🏠 ")
            else:
                cells.append(f" {TERRAIN_EMOJI[cell]} ")
        lines.append(f"{y:>2} |" + "|".join(cells) + "|")
    return "\n".join(lines)


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
    rules = [
        "Rules:",
        "  City output = all tiles in the surrounding 3x3 area, including the city tile.",
        "  Terrain: 🌾 plain=food, 🌲 forest=wood, ⛰️ mountain=ore, 🌊 river=food+science, 🪨 wasteland=none.",
        "  Tech unlocks buildings only: agriculture->farm, logging->lumberyard, mining->mine, education->library.",
        "  Buildings then add extra per-turn output in the chosen city.",
    ]
    parts = [render_summary(state), "", render_map(state), "", *rules]
    if footer:
        parts.extend(["", *footer])
    return "\n".join(parts)


def render_compact_status(state: GameState) -> str:
    output = projected_output(state)
    return "\n".join(
        [
            f"Turn {state.turn}/{state.max_turns}  Score {score(state)}",
            f"🍞 {state.resources['food']}  🪵 {state.resources['wood']}  ⛏️ {state.resources['ore']}  🔬 {state.resources['science']}",
            f"+  🍞 {output['food']}  🪵 {output['wood']}  ⛏️ {output['ore']}  🔬 {output['science']}",
            f"Techs: {','.join(sorted(state.techs)) if state.techs else 'none'}",
        ]
    )
