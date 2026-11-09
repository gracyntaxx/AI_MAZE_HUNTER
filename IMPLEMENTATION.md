# Implementation Notes

## Development phases

1. **Maze and search:** Added three fixed maze layouts and tested BFS, DFS, and
   A* with a common `SearchResult` type.
2. **Game mechanics:** Added player input, cell-by-cell A* pursuit, pause,
   collision and exit states, route efficiency, and level progression.
3. **Challenges and difficulty:** Added three multiple-choice questions per
   level, five-second Hunter slowdowns for correct answers, and speed increases
   after every eight valid moves.
4. **Interface and verification:** Added menu, instructions, algorithm guide,
   gameplay HUD, overlays, and automated tests.

## Key decisions

- The three mazes are predefined for reliable, repeatable gameplay.
- The game engine does not depend on Pygame, which keeps rules independently
  testable.
- Movement and Hunter timing use elapsed time rather than frame counts.
- A* uses Manhattan distance and a priority queue. BFS provides shortest
  unweighted route length; DFS demonstrates that a valid route need not be
  optimal.
- Challenges pause the game clock and Hunter while the player answers.

## Run and test

```powershell
python -m pip install -r requirements.txt
python main.py
python -m unittest discover -v
```
