from __future__ import annotations

import argparse

from demos.campus.config import BUILDINGS
from demos.campus.engine import CampusGame
from demos.campus.render import PLACE_EMOJI, render_dashboard, render_summary
from demos.campus.scheduler import choose_commands
from shared.cli_app import auto_pause, build_parser
from shared.cursor_input import select_menu
from shared.random_utils import make_rng


def build_cli_parser() -> argparse.ArgumentParser:
    return build_parser("Campus scheduler stage-one demo")


def _message_screen(game: CampusGame, lines: list[str]) -> None:
    select_menu(render_dashboard(game.state, footer=lines), ["Continue"])


def prompt_student_command(game: CampusGame, student_name: str) -> str | None:
    options = ["⏸️ wait", *[f"{PLACE_EMOJI[name]} {name}" for name in BUILDINGS]]
    choice = select_menu(
        render_dashboard(
            game.state,
            footer=[
                f"{student_name}: choose a destination or wait.",
                "Selecting a place means: start moving there now, or perform that place's default action if already there.",
            ],
        ),
        options,
    )
    if choice is None:
        return None
    if choice == 0:
        return "wait"
    return list(BUILDINGS)[choice - 1]


def run_manual(game: CampusGame) -> None:
    while not game.state.is_terminal:
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
        _message_screen(game, ["Hour resolved.", *game.state.log[-4:]])
    print(render_summary(game.state))


def run_auto(game: CampusGame, delay: float) -> None:
    while not game.state.is_terminal:
        print(render_dashboard(game.state))
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
