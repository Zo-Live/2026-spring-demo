from __future__ import annotations

import math

from demos.civilization.config import BUILDINGS, TECH_COSTS, TERRAINS
from demos.civilization.models import Action, City, GameState, RESOURCE_KEYS


def resource_template() -> dict[str, int]:
    return {key: 0 for key in RESOURCE_KEYS}


def add_resources(target: dict[str, int], delta: dict[str, int]) -> None:
    for key, value in delta.items():
        target[key] = target.get(key, 0) + value


def terrain_yield(terrain: str) -> dict[str, int]:
    return dict(TERRAINS[terrain]["yield"])


def city_zone_tiles(state: GameState, city: City) -> list[tuple[int, int]]:
    tiles: list[tuple[int, int]] = []
    for y in range(max(0, city.y - 1), min(state.height, city.y + 2)):
        for x in range(max(0, city.x - 1), min(state.width, city.x + 2)):
            tiles.append((x, y))
    return tiles


def city_base_output(state: GameState, city: City) -> dict[str, int]:
    total = resource_template()
    for x, y in city_zone_tiles(state, city):
        add_resources(total, terrain_yield(state.terrain[y][x]))
    return total


def city_total_output(state: GameState, city: City) -> dict[str, int]:
    total = city_base_output(state, city)
    for building_name in city.buildings:
        add_resources(total, BUILDINGS[building_name]["yield"])
    return total


def projected_output(state: GameState) -> dict[str, int]:
    total = resource_template()
    for city in state.cities.values():
        add_resources(total, city_total_output(state, city))
    return total


def score_city_location(state: GameState, x: int, y: int) -> int:
    tmp_city = City(city_id=-1, x=x, y=y)
    output = city_base_output(state, tmp_city)
    return output["food"] * 3 + output["wood"] * 2 + output["ore"] * 2 + output["science"] * 4


def score(state: GameState) -> int:
    resource_part = math.floor(
        (
            state.resources["food"]
            + state.resources["wood"]
            + 4 * state.resources["ore"]
            + state.resources["science"]
        )
        / 4
    )
    building_count = sum(len(city.buildings) for city in state.cities.values())
    return 20 * len(state.cities) + 5 * building_count + 8 * len(state.techs) + resource_part


def city_at(state: GameState, x: int, y: int) -> City | None:
    for city in state.cities.values():
        if city.x == x and city.y == y:
            return city
    return None


def can_build_city(state: GameState, x: int, y: int) -> tuple[bool, str]:
    if not (0 <= x < state.width and 0 <= y < state.height):
        return False, "Out of map bounds."
    if city_at(state, x, y) is not None:
        return False, "A city already exists there."
    if state.terrain[y][x] not in {"P", "F", "R"}:
        return False, "Cities can only be built on plain, forest, or river."
    for city in state.cities.values():
        if abs(city.x - x) + abs(city.y - y) < 3:
            return False, "Cities must be at least 3 tiles apart by Manhattan distance."
    return True, ""


def can_build_building(state: GameState, city_id: int, building_name: str) -> tuple[bool, str]:
    city = state.cities.get(city_id)
    if city is None:
        return False, "City does not exist."
    if building_name not in BUILDINGS:
        return False, "Unknown building."
    if building_name in city.buildings:
        return False, "Building already exists in this city."
    tech = BUILDINGS[building_name]["tech"]
    if tech not in state.techs:
        return False, f"Research {tech} first."
    for key, value in BUILDINGS[building_name]["cost"].items():
        if state.resources[key] < value:
            return False, "Not enough resources."
    return True, ""


def can_research(state: GameState, tech_name: str) -> tuple[bool, str]:
    if tech_name not in TECH_COSTS:
        return False, "Unknown technology."
    if tech_name in state.techs:
        return False, "Technology already researched."
    if state.resources["science"] < TECH_COSTS[tech_name]:
        return False, "Not enough science."
    return True, ""


def legal_city_locations(state: GameState) -> list[tuple[int, int]]:
    locations: list[tuple[int, int]] = []
    for y in range(state.height):
        for x in range(state.width):
            allowed, _ = can_build_city(state, x, y)
            if allowed:
                locations.append((x, y))
    return locations


def apply_action(state: GameState, action: Action) -> None:
    if state.is_terminal:
        raise ValueError("game already finished")
    messages: list[str] = []
    if action.kind == "build_city":
        if action.coord is None:
            raise ValueError("build_city requires coord")
        allowed, reason = can_build_city(state, action.coord[0], action.coord[1])
        if not allowed:
            raise ValueError(reason)
        city = City(city_id=state.next_city_id, x=action.coord[0], y=action.coord[1])
        state.cities[city.city_id] = city
        state.next_city_id += 1
        messages.append(f"Built city {city.city_id} at {action.coord}.")
    elif action.kind == "build_building":
        if action.city_id is None or action.name is None:
            raise ValueError("build_building requires city_id and name")
        allowed, reason = can_build_building(state, action.city_id, action.name)
        if not allowed:
            raise ValueError(reason)
        city = state.cities[action.city_id]
        city.buildings.add(action.name)
        for key, value in BUILDINGS[action.name]["cost"].items():
            state.resources[key] -= value
        messages.append(f"Built {action.name} in city {action.city_id}.")
    elif action.kind == "research":
        if action.name is None:
            raise ValueError("research requires name")
        allowed, reason = can_research(state, action.name)
        if not allowed:
            raise ValueError(reason)
        state.resources["science"] -= TECH_COSTS[action.name]
        state.techs.add(action.name)
        messages.append(f"Researched {action.name}.")
    elif action.kind == "skip":
        messages.append("Skipped turn.")
    else:
        raise ValueError("Unknown action kind.")

    total_output = projected_output(state)
    add_resources(state.resources, total_output)
    state.turn += 1
    messages.append(f"Collected {total_output}.")
    messages.append(f"Score is now {score(state)}.")
    state.log.extend(messages)
