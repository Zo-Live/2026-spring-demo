from __future__ import annotations

from demos.campus.config import BUILDINGS
from demos.campus.models import GameState
from demos.campus.rules import current_day_hour, team_score


PLACE_EMOJI = {
    "dorm": "🛏️",
    "teaching": "🏫",
    "canteen": "🍚",
    "library": "📚",
    "gym": "🏃",
}

TRAIT_LABEL = {
    "night_owl": "🦉 night_owl",
    "big_eater": "🍜 big_eater",
    "frail": "🩹 frail",
}


def render_destinations() -> str:
    return "\n".join(
        [
            "Destinations:",
            *[
                f"  {PLACE_EMOJI[name]} {name} (cap={building.capacity if building.capacity is not None else '∞'}, pos=({building.x},{building.y}))"
                for name, building in BUILDINGS.items()
            ],
        ]
    )


def render_summary(state: GameState) -> str:
    day, hour = current_day_hour(state.hour_index)
    lines = [f"Day {day}, Hour {hour:02d}:00", f"Team score: {team_score(state):.1f}"]
    for student in state.students:
        status_emoji = "🚶" if student.travel_remaining > 0 else "🧍"
        lines.append(
            f"{status_emoji} {student.name} {TRAIT_LABEL[student.trait]}  "
            f"📍 {PLACE_EMOJI[student.location]} {student.location}  "
            f"🎯 {student.target or '-'}  ⏳ {student.travel_remaining}  "
            f"📝 {student.last_action}"
        )
        lines.append(
            f"   ⚡ {student.energy}/{student.max_energy}  🍚 {student.satiety}  📘 {student.credits}  "
            f"💪 {student.health}  🙂 {student.mood}  "
            f"⚠️ {sorted(student.debuffs) if student.debuffs else ['none']}  "
            f"🏅 {sorted(student.achievements) if student.achievements else ['none']}"
        )
    return "\n".join(lines)


def render_dashboard(state: GameState, footer: list[str] | None = None) -> str:
    footer = footer or []
    parts = [render_summary(state), "", render_destinations()]
    if state.log:
        parts.extend(["", "Latest log:", *state.log[-5:]])
    if footer:
        parts.extend(["", *footer])
    return "\n".join(parts)
