from __future__ import annotations

import argparse

from demos.campus.config import BUILDINGS
from demos.campus.engine import CampusGame
from demos.campus.render import render_map, render_summary
from demos.campus.scheduler import choose_commands
from shared.cli_app import auto_pause, build_parser
from shared.cursor_input import select_grid, select_menu
from shared.random_utils import make_rng


def build_cli_parser() -> argparse.ArgumentParser:
    return build_parser("Campus scheduler stage-one demo")


def prompt_student_command(game: CampusGame, student_name: str) -> str | None:
    menu = ["Select target building", "Wait"]
    choice = select_menu(f"{student_name}: choose command", menu)
    if choice is None:
        return None
    if choice == 1:
        return "wait"
    coord = select_grid(
        title=f"{student_name}: choose target building",
        width=10,
        height=10,
        renderer=lambda x, y: next((name[0].upper() for name, building in BUILDINGS.items() if building.x == x and building.y == y), "."),
        selectable=lambda x, y: any(building.x == x and building.y == y for building in BUILDINGS.values()),
        footer_lines=["Select Dorm, Teaching, Canteen, Library, or Gym."],
    )
    if coord is None:
        return None
    for name, building in BUILDINGS.items():
        if (building.x, building.y) == coord:
            return name
    return None


def run_manual(game: CampusGame) -> None:
    while not game.state.is_terminal:
        print(render_map(game.state))
        print(render_summary(game.state))
        commands: dict[str, str] = {}
        for student in game.state.students:
            if student.travel_remaining > 0:
                commands[student.name] = "wait"
                continue
            command = prompt_student_command(game, student.name)
            if command is None:
                print("Game cancelled.")
                return
            commands[student.name] = command
        game.step(commands)
    print(render_summary(game.state))


def run_auto(game: CampusGame, delay: float) -> None:
    while not game.state.is_terminal:
        print(render_map(game.state))
        print(render_summary(game.state))
        commands = choose_commands(game.state)
        print(f"Auto commands: {commands}")
        game.step(commands)
        auto_pause(delay)
    print(render_summary(game.state))


def main() -> None:
    args = build_cli_parser().parse_args()
    game = CampusGame(make_rng(args.seed))
    if args.mode == "manual":
        run_manual(game)
    else:
        run_auto(game, args.step_delay)


if __name__ == "__main__":
    main()
