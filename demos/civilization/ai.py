from __future__ import annotations

from demos.civilization.config import BUILDINGS
from demos.civilization.models import Action, GameState
from demos.civilization.rules import (
    can_build_building,
    can_research,
    legal_city_locations,
    projected_output,
    score_city_location,
)


RESOURCE_PRIORITIES = [
    ("food", "farm", "agriculture"),
    ("wood", "lumberyard", "logging"),
    ("science", "library", "education"),
    ("ore", "mine", "mining"),
]


def choose_action(state: GameState) -> Action:
    output = projected_output(state)
    for resource_name, building_name, tech_name in RESOURCE_PRIORITIES:
        threshold = max(1, len(state.cities))
        if output[resource_name] < threshold:
            for city_id in state.cities:
                allowed, _ = can_build_building(state, city_id, building_name)
                if allowed:
                    return Action(kind="build_building", city_id=city_id, name=building_name)
            allowed, _ = can_research(state, tech_name)
            if allowed:
                return Action(kind="research", name=tech_name)

    locations = legal_city_locations(state)
    if locations:
        best_coord = max(locations, key=lambda coord: score_city_location(state, coord[0], coord[1]))
        return Action(kind="build_city", coord=best_coord)

    for tech_name in ("agriculture", "logging", "mining", "education"):
        allowed, _ = can_research(state, tech_name)
        if allowed:
            return Action(kind="research", name=tech_name)

    for city_id in state.cities:
        for building_name in BUILDINGS:
            allowed, _ = can_build_building(state, city_id, building_name)
            if allowed:
                return Action(kind="build_building", city_id=city_id, name=building_name)

    return Action(kind="skip")
