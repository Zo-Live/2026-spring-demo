from __future__ import annotations

import argparse

from demos.civilization.ai import choose_action
from demos.civilization.config import BUILDINGS, DEFAULT_MAP_SIZE, DEFAULT_MAX_TURNS, TECH_COSTS
from demos.civilization.engine import CivilizationGame
from demos.civilization.models import Action
from demos.civilization.render import render_map, render_summary
from shared.cli_app import auto_pause, build_parser
from shared.cursor_input import select_grid, select_menu
from shared.random_utils import make_rng


def build_cli_parser() -> argparse.ArgumentParser:
    parser = build_parser("Micro civilization stage-one demo")
    parser.add_argument("--size", type=int, default=DEFAULT_MAP_SIZE)
    parser.add_argument("--max-turns", type=int, default=DEFAULT_MAX_TURNS)
    return parser


def prompt_action(game: CivilizationGame) -> Action | None:
    state = game.state
    menu = ["Build city", "Build building", "Research tech", "Skip"]
    choice = select_menu("Select an action", menu)
    if choice is None:
        return None
    if choice == 0:
        coord = select_grid(
            title="Select city location",
            width=state.width,
            height=state.height,
            renderer=lambda x, y: state.terrain[y][x],
            selectable=lambda x, y: 0 <= x < state.width and 0 <= y < state.height,
            footer_lines=["Legal city tiles are plain/forest/river and far enough from existing cities."],
        )
        return None if coord is None else Action(kind="build_city", coord=coord)
    if choice == 1:
        options = [f"City {city_id}: {building}" for city_id in state.cities for building in BUILDINGS]
        index = select_menu("Select building target", options)
        if index is None:
            return None
        city_ids = list(state.cities)
        city_id = city_ids[index // len(BUILDINGS)]
        building_name = list(BUILDINGS)[index % len(BUILDINGS)]
        return Action(kind="build_building", city_id=city_id, name=building_name)
    if choice == 2:
        tech_names = list(TECH_COSTS)
        index = select_menu("Select technology", tech_names)
        if index is None:
            return None
        return Action(kind="research", name=tech_names[index])
    return Action(kind="skip")


def run_manual(game: CivilizationGame) -> None:
    while not game.state.is_terminal:
        print(render_map(game.state))
        print(render_summary(game.state))
        while True:
            action = prompt_action(game)
            if action is None:
                print("Game cancelled.")
                return
            try:
                from demos.civilization.rules import apply_action

                apply_action(game.state, action)
                print(game.state.log[-1])
                break
            except ValueError as error:
                print(f"Illegal action: {error}")
    print(render_summary(game.state))


def run_auto(game: CivilizationGame, delay: float) -> None:
    from demos.civilization.rules import apply_action

    while not game.state.is_terminal:
        print(render_map(game.state))
        print(render_summary(game.state))
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
