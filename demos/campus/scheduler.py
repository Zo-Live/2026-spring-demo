from __future__ import annotations

from demos.campus.config import ACTION_BY_BUILDING, BUILDINGS
from demos.campus.models import GameState, Student
from demos.campus.rules import current_day_hour, distance_hours, is_open


def _target_score(student: Student, building_name: str, hour_index: int, reserved: dict[tuple[int, str], int]) -> int:
    hour = hour_index % 24
    if student.location == building_name:
        if not is_open(building_name, hour):
            return -10_000
        base = {
            "dorm": 15 if student.energy < 35 or "fatigue" in student.debuffs else 2,
            "canteen": 14 if student.satiety < 35 or "hunger" in student.debuffs else 3,
            "library": 12,
            "teaching": 13,
            "gym": 8,
        }[building_name]
        return base

    travel = distance_hours(student.location, building_name, "fatigue" in student.debuffs)
    action_hour = (hour_index + travel) % 24
    if not is_open(building_name, action_hour):
        return -10_000
    capacity = BUILDINGS[building_name].capacity
    if capacity is not None and reserved.get((action_hour, building_name), 0) >= capacity:
        return -10_000
    base = {
        "dorm": 30 if student.energy < 30 or "fatigue" in student.debuffs else 1,
        "canteen": 28 if student.satiety < 30 or "hunger" in student.debuffs else 2,
        "library": 18,
        "teaching": 20,
        "gym": 10,
    }[building_name]
    return base - travel * 3


def choose_commands(state: GameState) -> dict[str, str]:
    commands: dict[str, str] = {}
    reserved: dict[tuple[int, str], int] = {}
    for student in state.students:
        if student.travel_remaining > 0:
            commands[student.name] = "wait"
            continue
        ranked = sorted(BUILDINGS, key=lambda name: _target_score(student, name, state.hour_index, reserved), reverse=True)
        choice = ranked[0]
        if student.location != choice and BUILDINGS[choice].capacity is not None:
            travel = distance_hours(student.location, choice, "fatigue" in student.debuffs)
            action_hour = (state.hour_index + travel) % 24
            reserved[(action_hour, choice)] = reserved.get((action_hour, choice), 0) + 1
        elif student.location == choice and BUILDINGS[choice].capacity is not None:
            reserved[(state.hour_index % 24, choice)] = reserved.get((state.hour_index % 24, choice), 0) + 1
        commands[student.name] = choice
    return commands
