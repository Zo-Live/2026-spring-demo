from __future__ import annotations

import argparse

from demos.civilization.ai import choose_action
from demos.civilization.config import BUILDINGS, DEFAULT_MAP_SIZE, DEFAULT_MAX_TURNS, TECH_COSTS
from demos.civilization.engine import CivilizationGame
from demos.civilization.models import Action
from demos.civilization.render import render_dashboard, render_summary
from demos.civilization.rules import (
    apply_action,
    can_build_building,
    can_research,
    legal_city_locations,
)
from shared.cli_app import auto_pause, build_parser
from shared.cursor_input import select_grid, select_menu
from shared.random_utils import make_rng


def build_cli_parser() -> argparse.ArgumentParser:
    parser = build_parser("Micro civilization stage-one demo")
    parser.add_argument("--size", type=int, default=DEFAULT_MAP_SIZE)
    parser.add_argument("--max-turns", type=int, default=DEFAULT_MAX_TURNS)
    return parser


def _message_screen(game: CivilizationGame, lines: list[str]) -> None:
    select_menu(render_dashboard(game.state, footer=lines), ["Continue"])


def prompt_action(game: CivilizationGame) -> Action | None:
    state = game.state
    menu = ["Build city", "Build building", "Research tech", "Skip"]
    choice = select_menu(
        render_dashboard(
            state,
            footer=[
                "Choose an action.",
                "Build city: select a legal tile on the map.",
                "Build building/research: only legal options are listed.",
            ],
        ),
        menu,
    )
    if choice is None:
        return None
    if choice == 0:
        legal = set(legal_city_locations(state))
        if not legal:
            _message_screen(game, ["No legal city locations are currently available."])
            return Action(kind="skip")
        coord = select_grid(
            title=render_dashboard(
                state,
                footer=[
                    "Build city: choose a legal tile.",
                    "Selectable tiles are legal city locations.",
                ],
            ),
            width=state.width,
            height=state.height,
            renderer=lambda x, y: next(
                (f"🏙️{city.city_id}" for city in state.cities.values() if (city.x, city.y) == (x, y)),
                {"P": "🌾", "F": "🌲", "M": "⛰️", "R": "🌊", "X": "🪨"}[state.terrain[y][x]],
            ),
            selectable=lambda x, y: (x, y) in legal,
            footer_lines=["Only bracket-highlightable tiles can be selected."],
        )
        return None if coord is None else Action(kind="build_city", coord=coord)
    if choice == 1:
        legal_options = [
            (city_id, building)
            for city_id in state.cities
            for building in BUILDINGS
            if can_build_building(state, city_id, building)[0]
        ]
        if not legal_options:
            _message_screen(game, ["No buildings can currently be constructed."])
            return Action(kind="skip")
        options = [f"City {city_id}: {building}" for city_id, building in legal_options]
        index = select_menu(
            render_dashboard(
                state,
                footer=["Build building: choose one legal city/building combination."],
            ),
            options,
        )
        if index is None:
            return None
        city_id, building_name = legal_options[index]
        return Action(kind="build_building", city_id=city_id, name=building_name)
    if choice == 2:
        tech_names = [name for name in TECH_COSTS if can_research(state, name)[0]]
        if not tech_names:
            _message_screen(game, ["No technologies can currently be researched."])
            return Action(kind="skip")
        index = select_menu(
            render_dashboard(
                state,
                footer=["Research: choose one legal technology."],
            ),
            tech_names,
        )
        if index is None:
            return None
        return Action(kind="research", name=tech_names[index])
    return Action(kind="skip")


def run_manual(game: CivilizationGame) -> None:
    while not game.state.is_terminal:
        while True:
            action = prompt_action(game)
            if action is None:
                print("Game cancelled.")
                return
            try:
                apply_action(game.state, action)
                _message_screen(game, ["Action resolved.", *game.state.log[-3:]])
                break
            except ValueError as error:
                _message_screen(game, [f"Illegal action: {error}"])
    print(render_summary(game.state))


def run_auto(game: CivilizationGame, delay: float) -> None:
    while not game.state.is_terminal:
        print(render_dashboard(game.state))
        action = choose_action(game.state)
        print(f"Auto action: {action}")
        apply_action(game.state, action)
        auto_pause(delay)
    print(render_summary(game.state))


def main() -> None:
    args = build_cli_parser().parse_args()
    game = CivilizationGame(rng=make_rng(args.seed), size=args.size, max_turns=args.max_turns)
    if args.mode == "manual":
        run_manual(game)
    else:
        run_auto(game, args.step_delay)


if __name__ == "__main__":
    main()
