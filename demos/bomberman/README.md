# Bomberman Demo

Stage-one minimum CLI bomberman demo with human-vs-AI and AI-vs-AI modes.

## Run
- `python3 -m demos.bomberman.cli --mode manual`
- `python3 -m demos.bomberman.cli --mode auto`

## Controls
- Manual mode uses arrow keys on the board to select an adjacent tile, or the current tile for `bomb` / `wait`.
- `Enter` confirms the selection.

## Implemented
- Grid generation with fixed iron walls and random boxes
- Two-player turn loop plus random monsters
- Movement legality checks
- Bomb countdown and cross explosion with blocking rules
- Human-vs-AI and AI-vs-AI baseline play

## Not Implemented
- Power-ups and advanced chain reactions
- Stage-two adversarial search
- GUI

## Assumptions
- Monster spawn uses empty cells only in this minimum version.
- Players cannot move onto each other.

## Tests
- `python3 -m unittest tests.test_bomberman -v`
