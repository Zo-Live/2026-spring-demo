from __future__ import annotations

TERRAINS = {
    "P": {"name": "Plain", "yield": {"food": 1}},
    "F": {"name": "Forest", "yield": {"wood": 1}},
    "M": {"name": "Mountain", "yield": {"ore": 1}},
    "R": {"name": "River", "yield": {"food": 1, "science": 1}},
    "X": {"name": "Wasteland", "yield": {}},
}

BUILDINGS = {
    "farm": {"cost": {"wood": 2}, "yield": {"food": 2}, "tech": "agriculture"},
    "lumberyard": {"cost": {"wood": 2}, "yield": {"wood": 2}, "tech": "logging"},
    "mine": {"cost": {"wood": 2, "ore": 1}, "yield": {"ore": 2}, "tech": "mining"},
    "library": {"cost": {"wood": 2, "ore": 2}, "yield": {"science": 2}, "tech": "education"},
}

TECH_COSTS = {
    "agriculture": 6,
    "logging": 6,
    "mining": 8,
    "education": 10,
}

DEFAULT_MAP_SIZE = 10
DEFAULT_MAX_TURNS = 30
