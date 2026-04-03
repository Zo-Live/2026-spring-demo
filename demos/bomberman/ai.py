from __future__ import annotations

from demos.bomberman.models import GameState
from demos.bomberman.rules import DIRECTIONS, danger_cells, is_legal_action


def _simulate_position(state: GameState, player_id: str, action: str) -> tuple[int, int]:
    player = state.players[player_id]
    if action in DIRECTIONS:
        dx, dy = DIRECTIONS[action]
        return (player.x + dx, player.y + dy)
    return (player.x, player.y)


def choose_action(state: GameState, player_id: str) -> str:
    player = state.players[player_id]
    opponent_id = "P2" if player_id == "P1" else "P1"
    opponent = state.players[opponent_id]
    legal = [action for action in ("up", "down", "left", "right", "bomb", "wait") if is_legal_action(state, player_id, action)]
    if not legal:
        return "wait"

    danger = danger_cells(state, {1})
    safe_moves = [
        action
        for action in legal
        if _simulate_position(state, player_id, action) not in danger
        and _simulate_position(state, player_id, action) not in state.monsters
    ]
    if (
        "bomb" in legal
        and abs(player.x - opponent.x) + abs(player.y - opponent.y) <= 2
        and any(action in safe_moves for action in ("up", "down", "left", "right", "wait"))
    ):
        return "bomb"

    ranked = safe_moves or legal
    ranked = sorted(
        ranked,
        key=lambda action: (
            _simulate_position(state, player_id, action) not in state.monsters,
            abs(_simulate_position(state, player_id, action)[0] - opponent.x)
            + abs(_simulate_position(state, player_id, action)[1] - opponent.y),
            action != "wait",
        ),
        reverse=True,
    )
    return ranked[0]
