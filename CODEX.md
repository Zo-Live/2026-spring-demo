# CODEX.md

## Core Lessons From This Repo

### 1. Build the shared interaction layer for failure, not for the happy path
- `curses` breaks easily when titles or grids grow.
- Never assume terminal width/height is sufficient.
- Always clip writes before `addstr`.
- If multiple demos share a UI primitive, add configuration hooks early:
  - selected cell style
  - whether unselectable cells are decorated
  - compact vs full title/header

### 2. “Readable in static logs” and “usable in interactive mode” are different problems
- Static rendering can afford richer context.
- Interactive rendering must aggressively compress.
- Large dashboards above a menu/grid are a common source of unusable screens.
- Good default:
  - auto mode: richer summary
  - manual mode: compact status + current decision context

### 3. Manual mode must always show:
- current state
- legal choices
- immediate consequence model or at least enough hints
- result after the action

If any of those is missing, the user perceives the system as broken even when the engine is technically working.

### 4. Filter invalid actions before the user sees them
- For menu-driven demos, “select then fail” feels bad.
- Prefer “only legal actions shown” over “show all and reject most”.
- Exceptions:
  - spatial selection where illegal cells are useful context
  - then clearly differentiate legal vs illegal cells visually

### 5. Emoji are useful, but terminal width lies
- Different terminals disagree on emoji width.
- If alignment matters, reserve wider cells than you think you need.
- Avoid mixing emoji + digits in a single grid cell unless that cell width is explicitly padded.
- If absolute alignment becomes critical, provide an ASCII fallback instead of fighting Unicode width forever.

### 6. Baseline AI quality matters more than initial implementation speed
- A baseline that is too weak undermines the whole demo.
- Minimal does not mean random or nearly random.
- Good baseline principles:
  - detect immediate wins/losses
  - detect short-horizon threats
  - constrain candidate actions to meaningful neighborhoods
  - prefer robust heuristics over shallow pseudo-randomness

### 7. Logs are part of gameplay
- In CLI demos, logs are not secondary.
- They are the substitute for animation and implicit state changes.
- Always log:
  - what action happened
  - why it was invalid
  - what state changed
  - why the turn/game ended

### 8. When a user reports “nothing happened”, assume UX failure first
- Usually the engine did something.
- The real bug is one of:
  - action result not shown
  - state screen and action screen disconnected
  - menu hidden by terminal overflow
  - too much context pushing choices off-screen

### 9. Shared abstractions should stop before they become a trap
- Common package structure was worth it.
- Common CLI helpers were worth it.
- A single universal renderer would have been a mistake.
- Reuse the interaction primitives, not the full presentation model.

### 10. Tighten the loop early with real TTY runs
- Non-interactive smoke tests are insufficient for `curses`.
- For any interactive CLI:
  - run at least one real TTY launch
  - verify menus fit
  - verify selection highlight is actually readable
  - verify cancel paths work

## Repo-Specific Reminders

### Gomoku
- User expectation for baseline AI is higher than “just legal”.
- Threat awareness before five-in-a-row is required.
- Visual consistency matters: if static board uses `●/○`, interactive board must too.

### Civilization
- Users need an always-visible explanation of resource flow.
- Tech benefits were implemented, but not self-evident.
- City markers in-map should stay simple; IDs belong in the side summary, not inside the cell.

### Campus
- A map was the wrong UI abstraction for a finite destination set.
- State explanation is mandatory here; otherwise the game feels arbitrary.
- Always show travel times from the current location during manual choice.

### Bomberman
- A “baseline AI” that suicides on turn 1 destroys trust immediately.
- Bomb placement must be visibly accessible from the manual control loop.
- Monster movement must be obvious in logs or board state; otherwise users assume it is broken.

## Process Lessons

### Things to do sooner next time
- Run a TTY session earlier.
- Build compact headers before adding rich dashboards.
- Add one “manual mode smoke” check for each demo, not just auto mode.
- Write explanation panels when implementing mechanics, not after confusion appears.

### Things not to do again
- Don’t push full dashboards into every `curses` title area.
- Don’t rely on implicit legality feedback.
- Don’t leave mixed symbolic vocabularies (`B/W` in one place, `●/○` in another).
- Don’t assume emoji grids will align without explicit padding.

## Default Strategy For Similar Future Work
1. Implement engine/rules first.
2. Make auto mode readable.
3. Build a compact manual loop with legal-action filtering.
4. Run a real TTY session before polishing.
5. Only then add richer rendering and explanations.
