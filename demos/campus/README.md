# Campus Scheduler Demo

Stage-one minimum CLI campus scheduling demo with manual operation and baseline auto scheduling.

## Run
- `python3 -m demos.campus.cli --mode manual`
- `python3 -m demos.campus.cli --mode auto`

## Controls
- In manual mode, choose each student's target building with arrow keys and `Enter`.
- `Wait` is available as a menu action.

## Implemented
- 168-hour simulation with three students
- Building coordinates, opening hours, capacities, travel time
- Energy, satiety, credits, health, mood
- Fatigue and hunger debuffs
- Traits and achievements
- Baseline scheduler that prefers safe and reachable plans

## Not Implemented
- Stage-two search planning
- GUI or animation
- Complex future reservation conflict solving

## Assumptions
- A move command means "head toward this building to perform its default action later".
- Late-night mood handling is implemented as a small hourly modifier for non-sleep actions.

## Tests
- `python3 -m unittest tests.test_campus -v`
