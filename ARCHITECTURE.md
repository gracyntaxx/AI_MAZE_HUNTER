# Architecture

AI Maze Hunter uses a small modular Python/Pygame structure suitable for a
third-year computer science project:

- `main.py` initializes Pygame, routes input, and runs the frame loop.
- `game/engine.py` owns level state, movement rules, timing, scoring, and
  transitions. It does not import Pygame.
- `game/renderer.py` draws screens and HUD elements but does not decide game
  rules.
- `game/challenges.py` stores question data and answer validation.
- `algorithms/search.py` provides independent BFS, DFS, and A* implementations.
- `levels/level_data.py` stores the three deterministic maze layouts.
- `config.py` holds window, color, and control configuration.
- `tests/test_game.py` verifies algorithms, level connectivity, and game rules.

The maze is a four-directional grid. `#` represents a wall; spaces and the
`S`, `H`, and `X` markers represent traversable cells. The Hunter calls A*
from its current position to the Explorer on each move. BFS is used to
calculate the optimal unweighted distance, while DFS is included for the
algorithm comparison screen.
