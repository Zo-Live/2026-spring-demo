from __future__ import annotations

import argparse

from demos.bomberman.ai import choose_action
from demos.bomberman.config import DEFAULT_SIZE, MAX_ROUNDS
from demos.bomberman.engine import BombermanGame
from demos.bomberman.render import render_board, render_summary
from shared.cli_app import auto_pause, build_parser
from shared.cursor_input import select_grid, select_menu
from shared.random_utils import make_rng


def build_cli_parser() -> argparse.ArgumentParser:
    parser = build_parser("Bomberman stage-one demo")
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE)
    parser.add_argument("--max-rounds", type=int, default=MAX_ROUNDS)
    return parser


def prompt_player_action(game: BombermanGame) -> str | None:
    player = game.state.players["P1"]
    coord = select_grid(
        title="Select an adjacent tile to move, or your current tile for bomb/wait",
        width=game.state.width,
        height=game.state.height,
        renderer=lambda x, y: (
            "1"
            if (x, y) == (player.x, player.y)
            else "2"
            if (x, y) == (game.state.players["P2"].x, game.state.players["P2"].y)
            else str(next((bomb.timer for bomb in game.state.bombs if (bomb.x, bomb.y) == (x, y)), "M" if (x, y) in game.state.monsters else "#" if (x, y) in game.state.walls else "+" if (x, y) in game.state.boxes else "."))
        ),
        selectable=lambda x, y: abs(player.x - x) + abs(player.y - y) <= 1,
        initial=(player.x, player.y),
        footer_lines=["Select current tile to choose bomb or wait."],
    )
    if coord is None:
        return None
    if coord == (player.x, player.y):
        index = select_menu("Current tile selected", ["Place bomb", "Wait"])
        if index is None:
            return None
        return "bomb" if index == 0 else "wait"
    dx = coord[0] - player.x
    dy = coord[1] - player.y
    mapping = {(0, -1): "up", (0, 1): "down", (-1, 0): "left", (1, 0): "right"}
    return mapping.get((dx, dy))


def run_manual(game: BombermanGame) -> None:
    while not game.state.is_terminal:
        print(render_board(game.state))
        print(render_summary(game.state))
        while True:
            action = prompt_player_action(game)
            if action is None:
                print("Game cancelled.")
                return
            ai_action = choose_action(game.state, "P2")
            try:
                game.step({"P1": action, "P2": ai_action})
                break
            except ValueError as error:
                print(f"Illegal action: {error}")
    print(render_board(game.state))
    print(render_summary(game.state))


def run_auto(game: BombermanGame, delay: float) -> None:
    while not game.state.is_terminal:
        print(render_board(game.state))
        print(render_summary(game.state))
        actions = {"P1": choose_action(game.state, "P1"), "P2": choose_action(game.state, "P2")}
        print(f"Auto actions: {actions}")
        game.step(actions)
        auto_pause(delay)
    print(render_board(game.state))
    print(render_summary(game.state))


def main() -> None:
    args = build_cli_parser().parse_args()
    game = BombermanGame(make_rng(args.seed), size=args.size, max_rounds=args.max_rounds)
    if args.mode == "manual":
        run_manual(game)
    else:
        run_auto(game, args.step_delay)


if __name__ == "__main__":
    main()
