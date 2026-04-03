from __future__ import annotations

import math

from demos.campus.config import ACTION_BY_BUILDING, ACTION_EFFECTS, BUILDINGS
from demos.campus.models import GameState, Student


def current_day_hour(hour_index: int) -> tuple[int, int]:
    return (hour_index // 24 + 1, hour_index % 24)


def is_open(building_name: str, hour: int) -> bool:
    if building_name == "dorm":
        return True
    if building_name == "teaching":
        return 8 <= hour < 18
    if building_name == "canteen":
        return (7 <= hour < 9) or (11 <= hour < 13) or (17 <= hour < 19)
    if building_name == "library":
        return 8 <= hour < 22
    if building_name == "gym":
        return 10 <= hour < 21
    return False


def distance_hours(start: str, end: str, fatigued: bool) -> int:
    if start == end:
        return 0
    a = BUILDINGS[start]
    b = BUILDINGS[end]
    distance = abs(a.x - b.x) + abs(a.y - b.y)
    hours = max(1, math.ceil(distance / 3))
    if fatigued:
        hours += 1
    return hours


def has_debuff(student: Student, name: str) -> bool:
    return name in student.debuffs


def _energy_multiplier(student: Student) -> float:
    return 0.8 if "time_manager" in student.achievements else 1.0


def apply_energy_cost(student: Student, energy_cost: int) -> int:
    scaled = int(math.ceil(energy_cost * _energy_multiplier(student)))
    return scaled


def apply_effect(student: Student, action_name: str, hour: int) -> None:
    effect = ACTION_EFFECTS[action_name].copy()
    if action_name == "eat" and student.trait == "big_eater":
        effect["satiety"] += 10
    if action_name == "study" and "involution_king" in student.achievements:
        effect["credits"] += 5
    effect["energy"] = int(effect["energy"] * _energy_multiplier(student)) if effect["energy"] < 0 else effect["energy"]

    student.energy += effect["energy"]
    student.satiety += effect["satiety"]
    student.credits += effect["credits"]
    student.health += effect["health"]
    student.mood += effect["mood"]

    if action_name == "study":
        student.study_hours += 1
    elif action_name == "exercise":
        student.exercise_hours += 1

    if action_name not in {"sleep", "wait"} and hour in {22, 23, 0, 1}:
        if student.trait == "night_owl":
            student.mood += 1
        else:
            student.mood -= 1

    if action_name == "sleep":
        student.debuffs.discard("fatigue")
    if action_name == "eat":
        student.debuffs.discard("hunger")


def update_debuffs_and_achievements(student: Student) -> None:
    if student.energy <= 0:
        student.debuffs.add("fatigue")
        student.mood -= 2
    else:
        student.debuffs.discard("fatigue")

    if student.satiety <= 0:
        student.debuffs.add("hunger")
        student.health -= 2
    else:
        student.debuffs.discard("hunger")

    if student.energy > student.max_energy:
        student.energy = student.max_energy
    if student.satiety > 100:
        student.satiety = 100

    if not student.debuffs:
        student.no_debuff_streak += 1
    else:
        student.no_debuff_streak = 0

    if student.study_hours >= 30:
        student.achievements.add("involution_king")
    if student.exercise_hours >= 15:
        student.achievements.add("athlete")
        if student.max_energy < 150:
            student.max_energy = 150
    if student.no_debuff_streak >= 48:
        student.achievements.add("time_manager")


def team_score(state: GameState) -> float:
    total = 0.0
    for student in state.students:
        total += student.credits * 2.0 + student.health * 1.5 + student.mood * 1.0 + len(student.achievements) * 100
    return total


def can_execute_here(student: Student, target_building: str, hour: int, occupied: dict[str, int]) -> tuple[bool, str]:
    if student.location != target_building:
        return False, "Student is not at the target building yet."
    if not is_open(target_building, hour):
        return False, "Target building is closed."
    capacity = BUILDINGS[target_building].capacity
    if capacity is not None and occupied.get(target_building, 0) >= capacity:
        return False, "Target building is full."
    action = ACTION_BY_BUILDING[target_building]
    if has_debuff(student, "fatigue") and action in {"study", "class", "exercise"}:
        return False, "Fatigue prevents this high-cost action."
    return True, ""
