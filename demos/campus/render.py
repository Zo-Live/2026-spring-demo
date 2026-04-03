from __future__ import annotations

from demos.campus.config import BUILDINGS
from demos.campus.models import GameState
from demos.campus.rules import current_day_hour, is_open, team_score


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
            "  🛏️ dorm 24h cap=∞",
            "  🏫 teaching 08-18 cap=∞",
            "  🍚 canteen 07-09 / 11-13 / 17-19 cap=∞",
            "  📚 library 08-22 cap=2",
            "  🏃 gym 10-21 cap=1",
        ]
    )


def render_summary(state: GameState) -> str:
    day, hour = current_day_hour(state.hour_index)
    lines = [f"Day {day}, Hour {hour:02d}:00", f"Team score: {team_score(state):.1f}"]
    for student in state.students:
        status_emoji = "🚶" if student.travel_remaining > 0 else "🧍"
        open_marker = "🟢" if is_open(student.location, hour) else "🔴"
        lines.append(
            f"{status_emoji} {student.name} {TRAIT_LABEL[student.trait]}  "
            f"📍 {PLACE_EMOJI[student.location]} {student.location}{open_marker}  "
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
    rules = [
        "Rules:",
        "  ⚡ <= 0 -> fatigue: no study/class/exercise, move +1h, mood -2/h",
        "  🍚 <= 0 -> hunger: study/class credits halved, health -2/h",
        "  🏅 study 30h -> involution_king, exercise 15h -> athlete, no debuff 48h -> time_manager",
    ]
    parts = [render_summary(state), "", render_destinations(), "", *rules]
    if state.log:
        parts.extend(["", "Latest log:", *state.log[-5:]])
    if footer:
        parts.extend(["", *footer])
    return "\n".join(parts)


def render_compact_dashboard(state: GameState, current_student: str | None = None, footer: list[str] | None = None) -> str:
    footer = footer or []
    day, hour = current_day_hour(state.hour_index)
    lines = [f"Day {day} {hour:02d}:00  Team {team_score(state):.1f}"]
    for student in state.students:
        prefix = "👉" if student.name == current_student else "  "
        open_marker = "🟢" if is_open(student.location, hour) else "🔴"
        lines.append(
            f"{prefix} {student.name} {PLACE_EMOJI[student.location]} {student.location}{open_marker} "
            f"⚡{student.energy}/{student.max_energy} 🍚{student.satiety} 📘{student.credits} "
            f"💪{student.health} 🙂{student.mood} ⏳{student.travel_remaining} 📝{student.last_action}"
        )
    lines.extend(
        [
            "Destinations: 🛏️ dorm  🏫 teaching  🍚 canteen  📚 library  🏃 gym",
            "Hours: dorm 24h | teaching 08-18 | canteen 07-09/11-13/17-19 | library 08-22 | gym 10-21",
            "Fatigue: ⚡<=0, no study/class/exercise, move +1h. Hunger: 🍚<=0, credits halved in study/class.",
            "Achievements: study30 / exercise15 / no-debuff48.",
        ]
    )
    if footer:
        lines.extend(footer)
    return "\n".join(lines)
