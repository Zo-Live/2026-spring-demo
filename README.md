# 2026 Spring Course Design Stage-One Demos

This repository contains four comparable minimum viable command-line demos for the stage-one requirements described in [docs/2026课程设计选题.pdf](/home/zolive/2026-spring-demo/docs/2026课程设计选题.pdf).

The implementation goal is consistency rather than completeness: all four demos share similar code organization, use Python standard-library-first code, provide `manual` and `auto` modes, and include a baseline AI or scheduler that can finish a full run.

## Environment
- Python `3.11+`
- No heavy third-party dependencies
- Interactive cursor selection uses `curses` when a TTY is available

## Repository Layout
```text
demos/
  gomoku/
  civilization/
  campus/
  bomberman/
shared/
tests/
docs/
```

## Common Modes
- `--mode manual`: interactive single-player mode
- `--mode auto`: baseline automatic demo mode
- `--seed <int>`: fixed random seed
- `--step-delay <float>`: pause between auto steps

## Demo Commands

### Gomoku
- `python3 -m demos.gomoku.cli --mode manual`
- `python3 -m demos.gomoku.cli --mode auto`

### Micro Civilization
- `python3 -m demos.civilization.cli --mode manual`
- `python3 -m demos.civilization.cli --mode auto`

### Campus Scheduler
- `python3 -m demos.campus.cli --mode manual`
- `python3 -m demos.campus.cli --mode auto`

### Bomberman
- `python3 -m demos.bomberman.cli --mode manual`
- `python3 -m demos.bomberman.cli --mode auto`

## Controls
- Gomoku: arrow keys move the board cursor; `Enter` places a stone.
- Micro Civilization: arrow keys select map tiles for city placement; menus also use arrow keys.
- Campus Scheduler: arrow keys select target buildings on the campus grid.
- Bomberman: arrow keys select an adjacent tile to move, or the current tile for `bomb` / `wait`.

## Testing
- Full suite: `python3 -m unittest discover -s tests -v`
- Demo-specific tests are documented in each demo README.

## Notes
- Each demo directory contains its own `README.md`.
- The code intentionally focuses on stage-one rules only.
- Some balancing details are simplified where the original document left room for interpretation; these choices are documented in the corresponding demo README files.
