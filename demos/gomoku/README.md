# Gomoku Demo

Stage-one minimum CLI Gomoku demo with human-vs-AI and AI-vs-AI modes.

## Run
- `python3 -m demos.gomoku.cli --mode manual`
- `python3 -m demos.gomoku.cli --mode auto`

## Controls
- Arrow keys move the cursor in `manual` mode when running in a TTY.
- `Enter` confirms a move.
- `q` cancels the game.

## Implemented
- Standard board state and legal move checks
- Human-vs-AI mode
- AI-vs-AI auto demo
- Five-in-a-row winner detection in four directions
- Basic baseline AI with win, block, and nearby-placement priorities

## Not Implemented
- Renju forbidden-move rules
- Advanced search or evaluation
- GUI

## Tests
- `python3 -m unittest tests.test_gomoku -v`
