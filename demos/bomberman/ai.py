from __future__ import annotations

from demos.bomberman.models import Bomb, GameState
from demos.bomberman.rules import DIRECTIONS, blast_cells, danger_cells, is_legal_action


def _simulate_position(state: GameState, player_id: str, action: str) -> tuple[int, int]:
    player = state.players[player_id]
    if action in DIRECTIONS:
        dx, dy = DIRECTIONS[action]
        return (player.x + dx, player.y + dy)
    return (player.x, player.y)


def _safe_actions(state: GameState, player_id: str) -> list[str]:
    danger_now = danger_cells(state, {1})
    player = state.players[player_id]
    safe: list[str] = []
    for action in ("up", "down", "left", "right", "wait"):
        if not is_legal_action(state, player_id, action):
            continue
        position = _simulate_position(state, player_id, action)
        if position in state.monsters or position in danger_now:
            continue
        safe.append(action)
    if not safe and is_legal_action(state, player_id, "wait"):
        safe.append("wait")
    return safe


def _can_escape_own_bomb(state: GameState, player_id: str) -> bool:
    player = state.players[player_id]
    hypothetical = blast_cells(state, Bomb(player.x, player.y, 0, player_id))
    for action in ("up", "down", "left", "right"):
        if not is_legal_action(state, player_id, action):
            continue
        if _simulate_position(state, player_id, action) not in hypothetical and _simulate_position(state, player_id, action) not in state.monsters:
            return True
    return False


def choose_action(state: GameState, player_id: str) -> str:
    player = state.players[player_id]
    opponent_id = "P2" if player_id == "P1" else "P1"
    opponent = state.players[opponent_id]
    legal = [action for action in ("up", "down", "left", "right", "bomb", "wait") if is_legal_action(state, player_id, action)]
    if not legal:
        return "wait"

    safe_moves = _safe_actions(state, player_id)
    if (player.x, player.y) in danger_cells(state, {1}):
        return max(
            safe_moves or ["wait"],
            key=lambda action: (
                _simulate_position(state, player_id, action) not in state.monsters,
                -abs(_simulate_position(state, player_id, action)[0] - opponent.x)
                - abs(_simulate_position(state, player_id, action)[1] - opponent.y),
            ),
        )

    if (
        "bomb" in legal
        and abs(player.x - opponent.x) + abs(player.y - opponent.y) <= 2
        and _can_escape_own_bomb(state, player_id)
    ):
        return "bomb"

    ranked = safe_moves or [action for action in legal if action != "bomb"] or legal
    return max(
        ranked,
        key=lambda action: (
            action != "wait",
            _simulate_position(state, player_id, action) not in state.monsters,
            -(
                abs(_simulate_position(state, player_id, action)[0] - opponent.x)
                + abs(_simulate_position(state, player_id, action)[1] - opponent.y)
            ),
        ),
    )
