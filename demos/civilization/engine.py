from __future__ import annotations

from random import Random

from demos.civilization.config import DEFAULT_MAP_SIZE, DEFAULT_MAX_TURNS, TERRAINS
from demos.civilization.models import Action, City, GameState
from demos.civilization.rules import legal_city_locations, resource_template, score_city_location


class CivilizationGame:
    def __init__(self, rng: Random, size: int = DEFAULT_MAP_SIZE, max_turns: int = DEFAULT_MAX_TURNS) -> None:
        self.rng = rng
        terrain = self._generate_map(size, size)
        state = GameState(
            width=size,
            height=size,
            terrain=terrain,
            resources=resource_template(),
            techs=set(),
            cities={},
            turn=0,
            max_turns=max_turns,
            next_city_id=1,
            log=[],
        )
        capital_x, capital_y = self._pick_capital(state)
        state.cities[0] = City(city_id=0, x=capital_x, y=capital_y)
        self.state = state

    def _generate_map(self, width: int, height: int) -> list[list[str]]:
        terrain_types = ["P", "F", "M", "R", "X"]
        weights = [0.32, 0.24, 0.18, 0.16, 0.10]
        terrain = [self.rng.choices(terrain_types, weights=weights, k=width) for _ in range(height)]
        return terrain

    def _pick_capital(self, state: GameState) -> tuple[int, int]:
        best = None
        best_score = None
        for y in range(state.height):
            for x in range(state.width):
                if state.terrain[y][x] not in {"P", "F", "R"}:
                    continue
                score = score_city_location(state, x, y)
                if best_score is None or score > best_score:
                    best = (x, y)
                    best_score = score
        if best is None:
            state.terrain[0][0] = "P"
            best = (0, 0)
        return best

    def legal_actions(self) -> list[Action]:
        actions = [Action(kind="skip")]
        for coord in legal_city_locations(self.state):
            actions.append(Action(kind="build_city", coord=coord))
        from demos.civilization.config import BUILDINGS, TECH_COSTS
        from demos.civilization.rules import can_build_building, can_research

        for city_id in self.state.cities:
            for building_name in BUILDINGS:
                allowed, _ = can_build_building(self.state, city_id, building_name)
                if allowed:
                    actions.append(Action(kind="build_building", city_id=city_id, name=building_name))
        for tech_name in TECH_COSTS:
            allowed, _ = can_research(self.state, tech_name)
            if allowed:
                actions.append(Action(kind="research", name=tech_name))
        return actions
