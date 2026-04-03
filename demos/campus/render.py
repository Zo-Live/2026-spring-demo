from __future__ import annotations

from demos.campus.config import BUILDINGS, GRID_SIZE
from demos.campus.models import GameState
from demos.campus.rules import current_day_hour, team_score
from shared.text_render import render_grid


def render_map(state: GameState) -> str:
    rows = [[" ." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for building in BUILDINGS.values():
        rows[building.y][building.x] = f" {building.name[0].upper()}"
    for index, student in enumerate(state.students, start=1):
        building = BUILDINGS[student.location]
        rows[building.y][building.x] = f"S{index}"
    return render_grid(rows)


def render_summary(state: GameState) -> str:
    day, hour = current_day_hour(state.hour_index)
    lines = [f"Day {day}, Hour {hour:02d}:00", f"Team score: {team_score(state):.1f}"]
    for student in state.students:
        lines.append(
            f"{student.name} trait={student.trait} loc={student.location} target={student.target} "
            f"travel={student.travel_remaining} action={student.last_action} energy={student.energy}/{student.max_energy} "
            f"satiety={student.satiety} credits={student.credits} health={student.health} mood={student.mood} "
            f"debuffs={sorted(student.debuffs)} achievements={sorted(student.achievements)}"
        )
    return "\n".join(lines)
