# Micro Civilization Demo

Stage-one minimum CLI civilization demo with manual play and baseline auto-run.

## Run
- `python3 -m demos.civilization.cli --mode manual`
- `python3 -m demos.civilization.cli --mode auto`

## Controls
- Arrow keys select map coordinates in TTY mode.
- Menus also use arrow keys plus `Enter`.

## Implemented
- Random map generation and capital placement
- Terrain, resources, city, building, and technology rules
- Full turn loop with score calculation
- Manual single-player operation
- Baseline auto manager using rule priorities

## Not Implemented
- Stage-two search planning
- Advanced balancing and map editor
- GUI

## Assumptions
- New city construction has no resource cost in this minimum demo.
- City spacing uses Manhattan distance `>= 3`.
- The score uses a weighted resource term similar to the document's suggested formula.

## Tests
- `python3 -m unittest tests.test_civilization -v`
