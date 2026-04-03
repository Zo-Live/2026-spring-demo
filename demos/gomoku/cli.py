from __future__ import annotations

import argparse

from demos.gomoku.ai import choose_move
from demos.gomoku.config import DEFAULT_BOARD_SIZE, DEFAULT_WIN_LENGTH
from demos.gomoku.engine import GomokuGame
from demos.gomoku.render import render_board
from shared.cli_app import auto_pause, build_parser
from shared.cursor_input import select_grid


def build_cli_parser() -> argparse.ArgumentParser:
    parser = build_parser("Gomoku stage-one demo")
    parser.add_argument("--size", type=int, default=DEFAULT_BOARD_SIZE)
    parser.add_argument("--win-length", type=int, default=DEFAULT_WIN_LENGTH)
    return parser


def run_manual(game: GomokuGame) -> None:
    print("Manual mode: you are Black (●), AI is White (○).")
    while not game.state.is_terminal:
        print(render_board(game.state.board, game.state.last_move))
        print(f"Move {game.state.move_count + 1}, current player: {game.state.current_player}")
        if game.state.current_player == "B":
            move = select_grid(
                title="Select your move",
                width=game.state.board.size,
                height=game.state.board.size,
                renderer=lambda x, y: game.state.board.get(x, y),
                selectable=lambda x, y: 0 <= x < game.state.board.size and 0 <= y < game.state.board.size and game.state.board.get(x, y) == ".",
                footer_lines=["Empty cells are selectable."],
            )
            if move is None:
                print("Game cancelled.")
                return
            game.apply_move(*move)
        else:
            move = choose_move(game.state.board, game.state.current_player, game.win_length)
            print(f"AI move: {move}")
            game.apply_move(*move)
    print(render_board(game.state.board, game.state.last_move))
    if game.state.winner:
        print(f"Winner: {game.state.winner}")
    else:
        print("Draw.")


def run_auto(game: GomokuGame, delay: float) -> None:
    while not game.state.is_terminal:
        print(render_board(game.state.board, game.state.last_move))
        move = choose_move(game.state.board, game.state.current_player, game.win_length)
        print(f"Auto move {game.state.move_count + 1}: {game.state.current_player} -> {move}")
        game.apply_move(*move)
        auto_pause(delay)
    print(render_board(game.state.board, game.state.last_move))
    if game.state.winner:
        print(f"Winner: {game.state.winner}")
    else:
        print("Draw.")


def main() -> None:
    args = build_cli_parser().parse_args()
    game = GomokuGame(size=args.size, win_length=args.win_length)
    if args.mode == "manual":
        run_manual(game)
    else:
        run_auto(game, args.step_delay)


if __name__ == "__main__":
    main()
