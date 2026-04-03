from __future__ import annotations

from random import Random

from demos.bomberman.config import BOMB_TIMER, DEFAULT_SIZE, MAX_ROUNDS, MONSTER_COUNT
from demos.bomberman.models import Bomb, GameState, Player
from demos.bomberman.rules import DIRECTIONS, blast_cells, in_bounds, is_blocked, is_legal_action


class BombermanGame:
    def __init__(self, rng: Random, size: int = DEFAULT_SIZE, max_rounds: int = MAX_ROUNDS, monster_count: int = MONSTER_COUNT) -> None:
        self.rng = rng
        walls = {(x, y) for y in range(size) for x in range(size) if x % 2 == 1 and y % 2 == 1}
        safety = {(0, 0), (1, 0), (0, 1), (size - 1, size - 1), (size - 2, size - 1), (size - 1, size - 2)}
        boxes: set[tuple[int, int]] = set()
        for y in range(size):
            for x in range(size):
                if (x, y) in walls or (x, y) in safety or (x, y) in {(0, 0), (size - 1, size - 1)}:
                    continue
                if self.rng.random() < 0.35:
                    boxes.add((x, y))
        empties = [(x, y) for y in range(size) for x in range(size) if (x, y) not in walls and (x, y) not in boxes and abs(x) + abs(y) > 4 and abs(x - (size - 1)) + abs(y - (size - 1)) > 4]
        self.rng.shuffle(empties)
        monsters = set(empties[:monster_count])
        players = {"P1": Player("P1", 0, 0), "P2": Player("P2", size - 1, size - 1)}
        self.state = GameState(size, size, walls, boxes, monsters, [], players, max_rounds=max_rounds)

    def legal_actions(self, player_id: str) -> list[str]:
        return [action for action in ("up", "down", "left", "right", "bomb", "wait") if is_legal_action(self.state, player_id, action)]

    def _move_player(self, player_id: str, action: str) -> None:
        player = self.state.players[player_id]
        if not player.alive:
            return
        if not is_legal_action(self.state, player_id, action):
            raise ValueError(f"illegal action for {player_id}: {action}")
        player.last_action = action
        if action in DIRECTIONS:
            dx, dy = DIRECTIONS[action]
            player.x += dx
            player.y += dy
            if (player.x, player.y) in self.state.monsters:
                player.alive = False
                self.state.log.append(f"{player_id} ran into a monster at {(player.x, player.y)}.")
        elif action == "bomb":
            self.state.bombs.append(Bomb(player.x, player.y, BOMB_TIMER, player_id))
            self.state.log.append(f"{player_id} planted a bomb at {(player.x, player.y)}.")

    def _move_monsters(self) -> None:
        new_positions: set[tuple[int, int]] = set()
        for monster in sorted(self.state.monsters):
            candidates = [monster]
            for dx, dy in DIRECTIONS.values():
                nx, ny = monster[0] + dx, monster[1] + dy
                if not in_bounds(self.state, nx, ny):
                    continue
                if is_blocked(self.state, nx, ny):
                    continue
                candidates.append((nx, ny))
            choice = self.rng.choice(candidates)
            new_positions.add(choice)
        self.state.monsters = new_positions
        for player in self.state.players.values():
            if player.alive and (player.x, player.y) in self.state.monsters:
                player.alive = False
                self.state.log.append(f"{player.player_id} was caught by a monster.")

    def _tick_bombs(self) -> None:
        for bomb in self.state.bombs:
            bomb.timer -= 1
        exploding = [bomb for bomb in self.state.bombs if bomb.timer <= 0]
        if not exploding:
            return
        blast_union: set[tuple[int, int]] = set()
        for bomb in exploding:
            blast_union |= blast_cells(self.state, bomb)
        destroyed_boxes = {box for box in self.state.boxes if box in blast_union}
        self.state.boxes -= destroyed_boxes
        self.state.monsters = {monster for monster in self.state.monsters if monster not in blast_union}
        for player in self.state.players.values():
            if player.alive and (player.x, player.y) in blast_union:
                player.alive = False
                self.state.log.append(f"{player.player_id} was hit by an explosion.")
        self.state.bombs = [bomb for bomb in self.state.bombs if bomb.timer > 0]

    def _update_outcome(self) -> None:
        alive_players = [player_id for player_id, player in self.state.players.items() if player.alive]
        if len(alive_players) == 1:
            self.state.winner = alive_players[0]
        elif len(alive_players) == 0:
            self.state.draw = True
        elif self.state.round_index >= self.state.max_rounds:
            self.state.draw = True

    def step(self, actions: dict[str, str]) -> None:
        if self.state.is_terminal:
            raise ValueError("game already finished")
        self.state.log.clear()
        for player_id in ("P1", "P2"):
            if self.state.players[player_id].alive:
                self._move_player(player_id, actions.get(player_id, "wait"))
        self._move_monsters()
        self._tick_bombs()
        self.state.round_index += 1
        self._update_outcome()
