from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Building:
    name: str
    x: int
    y: int
    capacity: int | None


BUILDINGS = {
    "dorm": Building("dorm", 1, 1, None),
    "teaching": Building("teaching", 2, 7, None),
    "canteen": Building("canteen", 5, 3, None),
    "library": Building("library", 8, 8, 2),
    "gym": Building("gym", 9, 2, 1),
}

TRAITS = ("night_owl", "big_eater", "frail")

ACTION_BY_BUILDING = {
    "dorm": "sleep",
    "canteen": "eat",
    "library": "study",
    "teaching": "class",
    "gym": "exercise",
}

ACTION_EFFECTS = {
    "sleep": {"energy": 15, "satiety": -2, "credits": 0, "health": 0, "mood": 0},
    "eat": {"energy": 0, "satiety": 30, "credits": 0, "health": 0, "mood": 5},
    "study": {"energy": -8, "satiety": -5, "credits": 10, "health": 0, "mood": 0},
    "class": {"energy": -10, "satiety": -5, "credits": 15, "health": 0, "mood": -2},
    "exercise": {"energy": -15, "satiety": -10, "credits": 0, "health": 10, "mood": 5},
    "wait": {"energy": 0, "satiety": -1, "credits": 0, "health": 0, "mood": 0},
}

GRID_SIZE = 10
MAX_HOURS = 168
