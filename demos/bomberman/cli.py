from __future__ import annotations

import argparse

from demos.bomberman.ai import choose_action
from demos.bomberman.config import DEFAULT_SIZE, MAX_ROUNDS
from demos.bomberman.engine import BombermanGame
from demos.bomberman.render import TILE, _pad_cell, render_board, render_compact_status, render_summary
from demos.bomberman.rules import is_legal_action
from shared.cli_app import auto_pause, build_parser
from shared.cursor_input import select_grid, select_menu
from shared.random_utils import make_rng


def build_cli_parser() -> argparse.ArgumentParser:
    parser = build_parser("Bomberman stage-one demo")
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE)
    parser.add_argument("--max-rounds", type=int, default=MAX_ROUNDS)
    return parser


def _dashboard(game: BombermanGame, footer: list[str] | None = None) -> str:
    footer = footer or []
    parts = [render_summary(game.state), "", render_board(game.state)]
    if footer:
        parts.extend(["", *footer])
    return "\n".join(parts)


def _compact_header(game: BombermanGame, footer: list[str] | None = None) -> str:
    footer = footer or []
    return "\n".join([render_compact_status(game.state), *footer])


def _message_screen(game: BombermanGame, lines: list[str]) -> None:
    select_menu(_dashboard(game, lines), ["Continue"])


def prompt_player_action(game: BombermanGame) -> str | None:
    player = game.state.players["P1"]
    coord = select_grid(
        title=_compact_header(
            game,
            [
                "Select an adjacent tile to move.",
                "Select your current tile to open the action menu for bomb or wait.",
            ],
        ),
        width=game.state.width,
        height=game.state.height,
        renderer=lambda x, y: _pad_cell(
            (
                TILE["p1"]
                if (x, y) == (player.x, player.y)
                else TILE["p2"]
                if (x, y) == (game.state.players["P2"].x, game.state.players["P2"].y)
                else next(
                    (f"{TILE['bomb']}{bomb.timer}" for bomb in game.state.bombs if (bomb.x, bomb.y) == (x, y)),
                    TILE["monster"] if (x, y) in game.state.monsters else TILE["wall"] if (x, y) in game.state.walls else TILE["box"] if (x, y) in game.state.boxes else TILE["empty"],
                )
            ),
            3,
        ),
        selectable=lambda x, y: (x, y) == (player.x, player.y)
        or any(
            is_legal_action(game.state, "P1", action) and (x, y) == (player.x + dx, player.y + dy)
            for action, (dx, dy) in {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}.items()
        ),
        initial=(player.x, player.y),
        footer_lines=["Selectable cells are your current tile and four adjacent tiles."],
        decorate_unselectable=False,
    )
    if coord is None:
        return None
    if coord == (player.x, player.y):
        options = ["Wait"]
        actions = ["wait"]
        if is_legal_action(game.state, "P1", "bomb"):
            options.insert(0, "Place bomb")
            actions.insert(0, "bomb")
        index = select_menu(_compact_header(game, ["Current tile selected.", "Choose bomb or wait."]), options)
        if index is None:
            return None
        return actions[index]
    dx = coord[0] - player.x
    dy = coord[1] - player.y
    mapping = {(0, -1): "up", (0, 1): "down", (-1, 0): "left", (1, 0): "right"}
    return mapping.get((dx, dy))


def run_manual(game: BombermanGame) -> None:
    while not game.state.is_terminal:
        while True:
            action = prompt_player_action(game)
            if action is None:
                print("Game cancelled.")
                return
            ai_action = choose_action(game.state, "P2")
            try:
                game.step({"P1": action, "P2": ai_action})
                _message_screen(game, [f"You chose: {action}", f"AI chose: {ai_action}", *game.state.log[-4:]])
                break
            except ValueError as error:
                _message_screen(game, [f"Illegal action: {error}"])
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
