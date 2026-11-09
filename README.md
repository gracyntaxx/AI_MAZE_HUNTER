# AI Maze Hunter
### A Pathfinding-Based Educational Maze Game

> **Think Smart. Escape the Hunter. Find the Shortest Path.**

AI Maze Hunter is a Python-based 2D maze escape game built using Pygame. It combines interactive gameplay with fundamental Artificial Intelligence pathfinding algorithms and problem-solving concepts.

The player controls an Explorer who must navigate through a maze and reach the exit (`X`) while an AI-controlled Hunter continuously calculates and follows the shortest available route to catch them.

The game demonstrates how search algorithms work in real-world scenarios through an interactive, progressively challenging experience.

---

# 1. Project Overview

## 1.1 Objective

Build a fully functional, playable desktop game that:

1. Allows the player to navigate a grid-based maze using keyboard controls.
2. Implements an AI-controlled Hunter that pursues the Explorer using the A* pathfinding algorithm.
3. Introduces three progressively challenging game levels.
4. Demonstrates the working principles of BFS, DFS and A* through educational explanations and comparisons.
5. Includes coding and logical reasoning challenges that reward correct answers with temporary Hunter slowdowns.
6. Demonstrates how route efficiency, distance, time and unnecessary movements affect the player's chances of survival.

## 1.2 Core Gameplay

- The Explorer starts at a designated entrance.
- The player manually navigates the maze using arrow keys or WASD.
- Walls block movement.
- The Hunter automatically calculates a path toward the Explorer using A*.
- The Hunter moves through valid maze cells and recalculates its route as the Explorer changes position.
- Every eight successful Explorer moves, the Hunter increases its movement speed.
- The player can encounter coding or logical reasoning challenges.
- Correct answers temporarily slow down the Hunter.
- The player must reach the exit before being caught.

## 1.3 Project Information

| Attribute | Specification |
|---|---|
| Project name | AI Maze Hunter |
| Project type | 2D desktop game |
| Programming language | Python |
| Game development library | Pygame |
| Primary AI algorithm | A* Search |
| Educational algorithms | BFS, DFS, A* |
| Maze structure | Two-dimensional grid |
| Movement | Four-directional |
| Player character | Explorer |
| AI character | Hunter |
| Number of levels | 3 |
| Controls | Keyboard |
| Platform | Desktop |

---

# 2. Technology Stack

Use the following technologies and libraries.

| Technology | Purpose |
|---|---|
| Python 3 | Main programming language and game logic |
| Pygame | Rendering, keyboard input, game loop, animation and collision handling |
| `heapq` | Priority queue for the A* algorithm |
| `collections.deque` | Queue implementation for BFS |
| Python lists | Grid representation and path storage |
| Python dictionaries and sets | Visited nodes, parent tracking and search data |
| `math` / `time` | Distance calculations and timing where required |
| Git and GitHub | Version control |

## Installation

The only mandatory external dependency is Pygame Community Edition, which is
compatible with the Pygame API used by this project and supports the optional
browser build.

```bash
python -m pip install -r requirements.txt
```

Run the game using:

```bash
python main.py
```

### Browser build

The Python/Pygame game can also be packaged for modern browsers with Pygbag.
Install the optional browser build dependency and create a static site bundle:

```bash
python -m pip install -r requirements-web.txt
python -m pygbag --build --app_name "AI Maze Hunter" --title "AI Maze Hunter" .
python scripts/fix_pygbag_html.py build/web/index.html
```

The generated site is in `build/web/`. The GitHub Actions workflow publishes
that folder to GitHub Pages after the repository's Pages source is configured
to use GitHub Actions. Pygbag 0.9.3 currently emits a missing BrowserFS CDN URL;
the small post-build script redirects that one asset to the published CDNJS
build so the browser loader can unpack the game bundle.

---

# 3. Game Architecture

Implement the project using modular, object-oriented Python code.

Avoid putting the entire game inside `main.py`.

## 3.1 Recommended Folder Structure

Create the following project structure:

```text
AI-Maze-Hunter/
│
├── main.py
├── config.py
├── README.md
├── ARCHITECTURE.md
├── IMPLEMENTATION.md
├── requirements.txt
├── .gitignore
│
├── assets/
│   ├── images/
│   │   ├── explorer.png
│   │   ├── hunter.png
│   │   ├── wall.png
│   │   ├── floor.png
│   │   └── exit.png
│   │
│   ├── fonts/
│   │
│   └── sounds/
│       ├── move.wav
│       ├── caught.wav
│       ├── victory.wav
│       └── challenge_correct.wav
│
├── algorithms/
│   ├── __init__.py
│   ├── astar.py
│   ├── bfs.py
│   └── dfs.py
│
├── game/
│   ├── __init__.py
│   ├── maze.py
│   ├── explorer.py
│   ├── hunter.py
│   ├── collision.py
│   ├── difficulty.py
│   ├── challenges.py
│   ├── game_state.py
│   ├── level_manager.py
│   └── renderer.py
│
├── levels/
│   ├── __init__.py
│   └── level_data.py
│
└── tests/
    ├── __init__.py
    ├── test_astar.py
    ├── test_bfs.py
    ├── test_dfs.py
    ├── test_maze.py
    └── test_game_logic.py
```

The agent may adjust the internal file structure if technically necessary, but all major responsibilities must remain modular and separated.

## 3.2 Module Responsibilities

### `main.py`
- Initialize Pygame.
- Create the game window.
- Initialize the game manager.
- Run the main game loop.
- Process events.
- Update game objects.
- Render the current screen.
- Handle game exit.

### `config.py`
Store configurable constants:

- Screen dimensions.
- Grid dimensions.
- Tile size.
- Frames per second.
- Explorer movement settings.
- Hunter base speed.
- Hunter speed multiplier.
- Difficulty thresholds.
- Colors.
- Font sizes.
- UI spacing.

Avoid scattering hardcoded values throughout the project.

### `game/maze.py`
Responsible for:

- Loading maze layouts.
- Maintaining the grid.
- Identifying walls and walkable cells.
- Returning valid neighboring cells.
- Checking whether a position is inside the maze.
- Identifying the start and exit.
- Resetting a level.

### `game/explorer.py`
Responsible for:

- Explorer position.
- Keyboard-controlled movement.
- Movement validation.
- Successful move counting.
- Tracking the player's route.
- Preventing movement through walls.

### `game/hunter.py`
Responsible for:

- Hunter position.
- Calculating a route using A*.
- Following the calculated path.
- Recalculating its route when the Explorer moves.
- Increasing movement speed.
- Applying temporary slowdown effects.
- Handling Hunter movement timing.

### `algorithms/astar.py`
Implement the A* pathfinding algorithm.

### `algorithms/bfs.py`
Implement Breadth-First Search for educational demonstration and path comparison.

### `algorithms/dfs.py`
Implement Depth-First Search for educational demonstration and path comparison.

### `game/collision.py`
Responsible for:

- Checking Explorer-Hunter collisions.
- Detecting whether the Explorer has reached the exit.
- Detecting collision after a Hunter movement.
- Determining game-over and victory conditions.

### `game/difficulty.py`
Responsible for:

- Tracking successful Explorer movements.
- Increasing Hunter speed after every eight successful moves.
- Applying and removing temporary speed modifiers.
- Managing difficulty progression.

### `game/challenges.py`
Responsible for:

- Displaying coding and logical reasoning questions.
- Managing multiple-choice answers.
- Validating answers.
- Rewarding correct answers.
- Applying temporary Hunter slowdowns.
- Managing challenge progression.

### `game/game_state.py`
Manage the current game state:

- Main menu.
- Playing.
- Paused.
- Challenge.
- Level completed.
- Game over.
- Final victory.

### `game/level_manager.py`
Responsible for:

- Loading levels.
- Tracking current level.
- Resetting level-specific variables.
- Moving to the next level.
- Detecting final game completion.

### `game/renderer.py`
Responsible for:

- Rendering the maze.
- Rendering the Explorer.
- Rendering the Hunter.
- Rendering the exit.
- Displaying the HUD.
- Displaying menus, challenges and results.
- Drawing overlays and notifications.

---

# 4. Maze Representation

## 4.1 Grid Structure

Represent the maze using a two-dimensional Python list.

Each cell should have one of the following values:

| Symbol | Meaning |
|---|---|
| `1` | Wall |
| `0` | Walkable path |
| `S` | Starting position |
| `X` | Exit |

Example:

```python
maze = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 'S', 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 'X', 1],
    [1, 1, 1, 1, 1, 1, 1]
]
```

This is an illustrative grid, not a mandatory level layout.

The Explorer and Hunter positions should be stored separately from the static maze grid.

## 4.2 Coordinates

Use grid coordinates:

```python
(row, column)
```

For example:

```python
explorer_position = (1, 1)
hunter_position = (5, 5)
exit_position = (5, 5)
```

The renderer must convert grid coordinates into pixel coordinates.

## 4.3 Movement Rules

The game must support four-directional movement only:

- Up: `(-1, 0)`
- Down: `(1, 0)`
- Left: `(0, -1)`
- Right: `(0, 1)`

Diagonal movement must not be allowed.

A movement is successful only if the destination is a valid walkable cell.

The Explorer and Hunter must never pass through walls.

The maze should be designed so that:

- There is at least one valid route from the starting position to the exit.
- The Hunter can reach the Explorer through valid paths.
- The maze contains turns, corridors and dead ends.
- The levels become progressively more challenging.

---

# 5. Pathfinding Algorithms

This is the core educational and technical component of AI Maze Hunter.

Implement three search algorithms:

1. Breadth-First Search (BFS)
2. Depth-First Search (DFS)
3. A* Search

**Important algorithm constraint:** A* is the primary and exclusive pathfinding algorithm used to control the Hunter's pursuit in the game. BFS and DFS must be implemented for educational demonstrations, algorithm comparison and path analysis. They must not replace A* as the Hunter's movement controller.

## 5.1 Breadth-First Search (BFS)

### Concept

BFS explores neighboring nodes level by level.

It uses a FIFO queue.

For an unweighted grid where every movement has equal cost, BFS finds the shortest path.

### Implementation requirements

- Use `collections.deque`.
- Start from the source position.
- Explore all valid neighboring cells.
- Maintain a visited set.
- Maintain a parent dictionary.
- Stop when the target is reached.
- Reconstruct the path from the parent dictionary.

### Expected output

Return:

- Found path.
- Path length.
- Whether a path exists.
- Number of explored nodes.

### Educational purpose

Demonstrate why BFS guarantees a shortest path in an unweighted grid.

## 5.2 Depth-First Search (DFS)

### Concept

DFS explores one path as deeply as possible before backtracking.

It uses a stack or recursion.

DFS does not guarantee the shortest path.

### Implementation requirements

- Use a stack-based implementation.
- Maintain visited nodes.
- Maintain parent tracking.
- Avoid revisiting already explored nodes.
- Reconstruct the path if the destination is found.

### Expected output

Return:

- Found path.
- Path length.
- Whether a path exists.
- Number of explored nodes.

### Educational purpose

Demonstrate how deep exploration and backtracking work, including how DFS may explore unnecessary routes.

## 5.3 A* Search

<badge color="success">Primary Hunter AI algorithm</badge>

### Concept

A* combines the cost already travelled with an estimate of the distance remaining.

It uses:

\[
f(n) = g(n) + h(n)
\]

Where:

- `g(n)` = actual cost from the starting node to the current node.
- `h(n)` = estimated cost from the current node to the target.
- `f(n)` = total estimated cost.

### Heuristic

Use Manhattan distance because the maze supports four-directional movement.

\[
h(n) = |r_1-r_2| + |c_1-c_2|
\]

### Implementation requirements

- Use Python's `heapq` as a priority queue.
- Maintain a `g_score` dictionary.
- Maintain an `f_score` or calculate priority when inserting into the heap.
- Maintain a parent dictionary.
- Maintain a closed or visited set.
- Explore valid neighboring cells only.
- Update the cost when a better route is found.
- Reconstruct the final path.
- Handle situations where no path exists.

All grid movements should have equal cost of 1.

### Expected output

Return:

- Shortest path.
- Path length.
- Number of explored nodes.
- Whether a path exists.

### Hunter integration

The Hunter must:

1. Read the current Explorer position.
2. Use its own current position as the A* starting node.
3. Calculate the route to the Explorer.
4. Follow the next cell in the calculated path.
5. Recalculate the route when the Explorer changes position.
6. Repeat this process until the Explorer is caught or the game ends.

The Hunter must never teleport.

The Hunter must never move through walls.

The Hunter should visibly move cell by cell.

If no valid route exists, the Hunter should remain in place until a valid route can be found.

## 5.4 Algorithm Comparison

Provide an educational comparison screen or results section.

| Feature | BFS | DFS | A* |
|---|---|---|---|
| Search strategy | Level by level | Depth first | Cost + heuristic |
| Data structure | Queue | Stack | Priority queue |
| Shortest path | Yes, unweighted grid | Not guaranteed | Yes, with admissible heuristic |
| Heuristic | No | No | Yes |
| Main purpose | Shortest-path demonstration | Backtracking demonstration | Intelligent pursuit |

Compare:

- Path length.
- Number of explored nodes.
- Search strategy.
- Execution time, where measurable.

For fair comparisons, use the same maze, source and destination.

---

# 6. Characters and Game Mechanics

## 6.1 Explorer

The Explorer is the player-controlled character.

### Responsibilities

- Start at the designated entrance.
- Move using arrow keys or WASD.
- Navigate through valid cells.
- Avoid walls.
- Reach the exit.
- Avoid being caught by the Hunter.

### Movement rules

- One successful input moves the Explorer by one cell.
- Invalid movement must not increment the move counter.
- Movement should be smooth and visually clear.
- Prevent accidental repeated movement from a single key press.
- Allow continuous keyboard movement if implemented with a controlled movement interval.

Track:

- Current position.
- Total successful moves.
- Route taken.
- Completion time.

## 6.2 Hunter

The Hunter is an AI-controlled enemy.

### Responsibilities

- Continuously pursue the Explorer.
- Use A* to calculate its route.
- Move one valid cell at a time.
- Recalculate its route when the Explorer moves.
- Become faster as the game progresses.
- Be temporarily slowed when the player solves a challenge correctly.

### Movement

Hunter movement must be controlled using a time-based interval, not by moving every rendered frame.

This ensures consistent gameplay regardless of computer performance.

Suggested configurable starting values:

```python
HUNTER_BASE_INTERVAL = 0.65
HUNTER_MIN_INTERVAL = 0.20
HUNTER_SPEED_INCREASE = 0.05
```

The values represent seconds between Hunter movements and should be playtested and balanced.

### Dynamic difficulty

Every eight successful Explorer moves:

- Increase the Hunter's movement speed.
- Reduce the time interval between Hunter moves.
- Display a small difficulty notification.

Never increase speed after invalid movement or blocked movement.

Apply a configurable maximum speed so that the Hunter never becomes impossibly fast.

## 6.3 Hunter Slowdown Power-Up

Correct answers to coding or logical reasoning challenges temporarily slow the Hunter.

Requirements:

- Display a clear success notification.
- Apply a temporary movement interval multiplier.
- Track the remaining duration.
- Restore the Hunter's normal difficulty-adjusted speed after the effect expires.
- Ensure that slowdown effects do not permanently overwrite difficulty progression.

Use a separate modifier system so difficulty and power-ups work independently.

Example configurable settings:

```python
HUNTER_SLOWDOWN_MULTIPLIER = 1.5
HUNTER_SLOWDOWN_DURATION = 5.0
```

A multiplier greater than 1 increases the time between Hunter moves, making it slower.

---

# 7. Coding and Logic Challenges

An important feature of AI Maze Hunter is its educational challenge system.

The player must solve coding or logical reasoning questions to obtain temporary Hunter slowdowns.

## 7.1 Challenge Requirements

- Include a question bank.
- Support multiple-choice questions.
- Display three or four answer options.
- Allow the player to select an answer using keyboard controls.
- Validate the selected answer.
- Display immediate feedback.
- Reward correct answers with a temporary Hunter slowdown.
- Incorrect answers must not grant a power-up.
- Avoid repeatedly displaying the same question within a level when possible.

## 7.2 Question Categories

Include questions from:

1. Basic programming logic.
2. Python fundamentals.
3. Loops and conditions.
4. Arrays and lists.
5. Data structures.
6. Searching algorithms.
7. Logical reasoning.
8. Basic pathfinding concepts.

Questions should be suitable for beginner-level computer science students.

## 7.3 Challenge Progression

The presentation specifies three to five coding or logic questions as part of the escape experience.

Implement a configurable challenge count, defaulting to three questions per level, with the question bank supporting additional questions.

Challenges should be triggered at controlled milestones or designated challenge points, rather than appearing randomly every frame.

A correct answer:

- Grants a slowdown.
- Displays a success message.
- Allows the player to continue.

An incorrect answer:

- Displays the correct answer or an explanation.
- Does not grant the slowdown.
- Allows the player to continue.

The game should pause Hunter movement while a question is being answered so that the challenge tests knowledge rather than keyboard speed.

## 7.4 Question Data Structure

Store questions separately from game rendering logic.

Example:

```python
questions = [
    {
        "question": "Which data structure is used in BFS?",
        "options": [
            "Stack",
            "Queue",
            "Heap",
            "Tree"
        ],
        "answer": 1,
        "explanation": "BFS uses a FIFO queue."
    }
]
```

Do not hardcode question logic directly into the Pygame event loop.

---

# 8. Game Levels

The game must contain exactly three main levels, with increasing difficulty.

## Level 1: The First Escape

**Objective:** Introduce the player to the game.

Characteristics:

- Small and relatively simple maze.
- Clear entrance and exit.
- Fewer obstacles.
- Short corridors.
- Limited dead ends.
- Introduces Explorer movement.
- Introduces basic Hunter pursuit.

Learning objectives:

- Understand grid movement.
- Understand walls and walkable cells.
- Observe the Hunter following the Explorer.
- Understand the basic idea of pathfinding.

## Level 2: Twisting Tunnels

**Objective:** Introduce more complex navigation and decision-making.

Characteristics:

- Larger maze than Level 1.
- Multiple turns and corridors.
- More dead ends.
- Longer alternative routes.
- Increased Hunter difficulty.
- Coding and logical reasoning challenges.

Learning objectives:

- Understand how different paths affect escape.
- Observe how the Hunter recalculates routes.
- Understand why unnecessary detours are risky.
- Experience temporary slowdown power-ups.

## Level 3: Final Run

**Objective:** Test the player's navigation and decision-making skills.

Characteristics:

- Most challenging maze.
- More complex corridor structures.
- Multiple dead ends.
- Longer paths.
- More demanding Hunter pursuit.
- Coding and logical reasoning challenges.
- Highest difficulty setting.

Learning objectives:

- Apply efficient navigation.
- Minimize unnecessary movements.
- Make quick decisions.
- Reach the exit before capture.

## Level Design Requirements

Every level must:

- Have a valid start and exit.
- Be solvable.
- Be connected sufficiently for the Hunter to pursue the Explorer.
- Have a predefined Hunter starting position.
- Have an appropriate maze size and difficulty.
- Be visually distinguishable from the other levels.

Store maze layouts and character starting positions in `levels/level_data.py`.

Do not randomly generate mazes at runtime unless explicitly needed. Prefer predefined, tested layouts for predictable gameplay and reliable level progression.

---

# 9. Game Screens and User Interface

Build a polished, understandable and visually consistent interface.

The game should feel like an actual playable game, not a basic algorithm demonstration.

## 9.1 Main Menu

Display:

- Game title: AI MAZE HUNTER.
- Subtitle: A Pathfinding-Based Educational Game.
- Play button.
- How to Play.
- Algorithm Guide.
- Exit button.

The main menu should clearly introduce the objective.

## 9.2 How to Play Screen

Explain:

- Control the Explorer.
- Avoid the Hunter.
- Navigate around walls.
- Reach the exit marked X.
- Answer coding questions correctly to slow down the Hunter.
- The Hunter gets faster as you make more successful moves.

Display keyboard controls.

## 9.3 Gameplay Screen

The gameplay screen must contain:

### Main area

- Grid-based maze.
- Wall tiles.
- Walkable tiles.
- Explorer.
- Hunter.
- Exit.

### HUD

Display:

- Current level and level name.
- Successful moves.
- Elapsed time.
- Hunter speed or difficulty indicator.
- Power-up status and remaining duration.
- Optional shortest-path distance.

The player should be able to distinguish the Explorer, Hunter, walls and exit immediately.

## 9.4 Pause Screen

Pressing `P` should pause the game.

Display:

- Resume.
- Restart Level.
- Main Menu.

Hunter movement and game timer must stop while paused.

## 9.5 Challenge Screen

Display:

- Question.
- Answer options.
- Keyboard selection instructions.
- Submit or confirm action.
- Feedback after submission.

The maze should remain visible behind an overlay where practical.

## 9.6 Level Completion Screen

Display:

- Level completed.
- Time taken.
- Number of successful moves.
- Shortest possible path length.
- Whether the player used an efficient route.
- Next Level button.

## 9.7 Game Over Screen

Display when the Hunter catches the Explorer.

Show:

- Game Over.
- Hunter caught the Explorer.
- Level reached.
- Time survived.
- Number of moves.
- Restart Level.
- Main Menu.

## 9.8 Final Victory Screen

After completing all three levels, display:

**YOU ESCAPED THE HUNTER!**

Show:

- All levels completed.
- Total moves.
- Total time.
- Performance summary.
- Final shortest-path comparison.
- Play Again.
- Main Menu.

---

# 10. Game Controls

Use the following controls consistently throughout the game.

| Key | Action |
|---|---|
| Arrow keys | Move Explorer |
| W / A / S / D | Move Explorer |
| Enter | Start game / Continue to next level |
| Space | Start game |
| P | Pause / Resume |
| R | Restart current level |
| 1 / 2 / 3 | Select challenge answer |
| Escape | Pause or return to menu |

The controls should be displayed in the How to Play screen.

Avoid using the same key for conflicting actions in different game states.

---

# 11. Game State Management

Implement a centralized state management system.

Suggested states:

```python
MAIN_MENU = "main_menu"
HOW_TO_PLAY = "how_to_play"
ALGORITHM_GUIDE = "algorithm_guide"
PLAYING = "playing"
PAUSED = "paused"
CHALLENGE = "challenge"
LEVEL_COMPLETE = "level_complete"
GAME_OVER = "game_over"
VICTORY = "victory"
```

### State transition flow

```text
MAIN MENU
    |
    v
HOW TO PLAY / PLAY
    |
    v
LEVEL 1: THE FIRST ESCAPE
    |
    +---- Hunter catches Explorer ----> GAME OVER
    |
    +---- Explorer reaches exit
                  |
                  v
          LEVEL COMPLETE
                  |
                  v
LEVEL 2: TWISTING TUNNELS
    |
    +---- Hunter catches Explorer ----> GAME OVER
    |
    +---- Explorer reaches exit
                  |
                  v
          LEVEL COMPLETE
                  |
                  v
LEVEL 3: FINAL RUN
    |
    +---- Hunter catches Explorer ----> GAME OVER
    |
    +---- Explorer reaches exit
                  |
                  v
             VICTORY
```

The game must not continue updating Hunter movement, timers or difficulty while in paused, challenge or completed states.

---

# 12. Collision Detection and Win/Lose Conditions

## 12.1 Hunter Collision

The Explorer loses when the Hunter occupies the same grid cell as the Explorer.

Check collision:

- After successful Explorer movement.
- After Hunter movement.
- When the Hunter recalculates and follows its path.

If the Hunter reaches the Explorer's position, immediately transition to the Game Over state.

## 12.2 Exit Detection

The Explorer wins the current level when they reach the designated exit cell.

If the exit is reached before a capture condition, transition to Level Complete.

The exit should not be accessible through walls.

## 12.3 Collision Edge Cases

Handle:

- Explorer moving into a wall.
- Hunter moving into a wall.
- Explorer and Hunter attempting to occupy the same cell.
- Hunter reaching the Explorer immediately after the Explorer moves.
- Explorer reaching the exit.
- Hunter having no available path.
- Multiple state transitions occurring in the same update.

Prioritize a consistent and predictable outcome for each event.

---

# 13. Performance Tracking and Results

The educational purpose of the game is to demonstrate the relationship between route efficiency and survival.

Track the following:

| Metric | Description |
|---|---|
| Player moves | Total successful Explorer movements |
| Shortest distance | Minimum path length from start to exit |
| Actual distance | Number of moves taken by the player |
| Time | Time taken to complete the level |
| Hunter speed | Current Hunter movement speed |
| Explored nodes | Nodes visited by the search algorithm |
| Escape status | Completed or caught |

At level completion, calculate:

```text
Extra Moves = Actual Moves - Shortest Path Length
```

Also display a simple route-efficiency percentage:

```text
Efficiency = (Shortest Path Length / Actual Moves) * 100
```

Handle zero-move cases safely.

Do not use the player's final position to calculate the shortest path. Use the original level start and exit positions.

The results screen should explain how unnecessary detours increase the chance of being caught.

---

# 14. Visual Design Requirements

Create a polished 2D game interface using Pygame.

The visual presentation should support the educational concept while remaining readable and playable.

## Design direction

Use a dark, atmospheric maze environment with contrasting characters and clear visual hierarchy.

Suggested palette:

| Element | Suggested appearance |
|---|---|
| Background | Deep dark teal |
| Maze walls | Dark charcoal / blue-grey |
| Walkable paths | Muted grey / teal |
| Explorer | Bright peach / warm light tone |
| Hunter | Strong magenta / red |
| Exit | Bright yellow / green |
| Primary text | Light peach / off-white |
| HUD panels | Dark blue / teal |

The design direction should be inspired by the presentation's dark teal and peach visual language.

### Visual requirements

- Clear grid boundaries.
- Distinct wall and floor textures or colors.
- Visually different Explorer and Hunter.
- Clearly marked exit.
- Smooth character movement or controlled cell transitions.
- Readable typography.
- Consistent buttons.
- Clean HUD.
- Visible feedback for successful challenges.
- Distinct visual feedback for capture and victory.

### Asset handling

Use local assets where available.

If image assets are unavailable, implement attractive Pygame-based vector or geometric representations as fallbacks.

The game must remain fully functional without external image assets.

Never allow missing assets or fonts to crash the game.

---

# 15. Main Game Loop

Use a standard Pygame game loop.

The loop should handle:

1. Event processing.
2. Keyboard input.
3. Game-state management.
4. Explorer movement.
5. Hunter pathfinding and movement.
6. Collision detection.
7. Timer updates.
8. Difficulty progression.
9. Power-up duration.
10. Rendering.
11. Frame-rate control.

Use:

```python
clock = pygame.time.Clock()
```

Use:

```python
clock.tick(FPS)
```

A target of 60 FPS is recommended for rendering.

**Important:** The game rendering speed and character movement speed must be independent.

Do not use `time.sleep()` to control character movement because it blocks the game loop.

Use Pygame's timing facilities or elapsed-time tracking instead.

---

# 16. Implementation Phases

Follow the implementation roadmap in the project presentation.

Do not attempt to build every feature in one large, untested step.

## Phase 1: Maze Creation

Tasks:

- Set up Python and Pygame.
- Create the game window.
- Define the grid representation.
- Implement maze loading.
- Define walls and paths.
- Define Explorer and Hunter starting positions.
- Define the exit.
- Create maze rendering.
- Test valid and invalid movement cells.

**Completion condition:** A maze renders correctly and all cells are represented accurately.

## Phase 2: Pathfinding Algorithms

Tasks:

- Implement BFS.
- Implement DFS.
- Implement A*.
- Implement Manhattan distance.
- Implement path reconstruction.
- Implement valid-neighbor detection.
- Test pathfinding on multiple maze layouts.
- Verify shortest-path correctness.
- Connect A* to the Hunter.

**Completion condition:** All three algorithms work independently and the Hunter can follow an A* route.

## Phase 3: Game Mechanics

Tasks:

- Implement Explorer keyboard controls.
- Implement Hunter movement.
- Implement Hunter route recalculation.
- Implement collision detection.
- Implement exit detection.
- Implement win and lose conditions.
- Implement level transitions.
- Implement game states.
- Implement movement and timer tracking.

**Completion condition:** A complete playable maze chase works from start to finish.

## Phase 4: Challenges and Power-Ups

Tasks:

- Create the question bank.
- Implement multiple-choice questions.
- Implement answer validation.
- Implement correct-answer rewards.
- Implement temporary Hunter slowdown.
- Implement speed increases after every eight successful Explorer moves.
- Implement difficulty notifications.
- Test interaction between slowdown and difficulty.

**Completion condition:** Challenge answers affect Hunter speed correctly and difficulty progression works.

## Phase 5: Testing and Evaluation

Tasks:

- Test all three levels.
- Test all keyboard controls.
- Test wall collisions.
- Test Hunter route calculation.
- Test difficulty progression.
- Test challenge rewards.
- Test pause and restart.
- Test level completion.
- Test game over.
- Test final victory.
- Test performance metrics.
- Test missing asset fallbacks.

**Completion condition:** The complete game is stable, playable and demonstrates the intended algorithms correctly.

---

# 17. Testing Requirements

The coding agent must create and execute meaningful tests.

## 17.1 Algorithm Tests

### BFS

- Finds a shortest path in an unweighted grid.
- Returns a valid path.
- Does not pass through walls.
- Correctly handles unreachable destinations.
- Handles source equal to destination.

### DFS

- Finds a path when one exists.
- Does not revisit nodes indefinitely.
- Returns a valid path.
- Handles unreachable destinations.

### A*

- Finds an optimal path on the unweighted grid with Manhattan distance.
- Returns a valid path.
- Does not pass through walls.
- Correctly handles unreachable destinations.
- Correctly reconstructs the path.
- Recalculates when the Explorer moves.

## 17.2 Game Tests

- Explorer cannot move through walls.
- Invalid moves do not increment the move counter.
- Hunter cannot move through walls.
- Hunter follows the A* route.
- Hunter speed increases after eight successful moves.
- Correct challenge answers activate slowdown.
- Incorrect answers do not activate slowdown.
- Slowdown expires correctly.
- Pause freezes gameplay.
- Restart resets the current level.
- Reaching the exit completes the level.
- Hunter catching the Explorer triggers Game Over.
- Completing the third level triggers Victory.

## 17.3 Level Tests

For every level:

- Confirm the start and exit exist.
- Confirm the maze is solvable.
- Confirm the Hunter has a valid pursuit route.
- Confirm there are no invalid grid coordinates.
- Confirm the player can complete the level.

---

# 18. Code Quality Requirements

The agent must follow these standards:

1. Use modular and object-oriented Python.
2. Keep game logic separate from rendering.
3. Keep pathfinding algorithms separate from character classes.
4. Use meaningful variable and function names.
5. Add comments to explain important algorithmic logic.
6. Avoid unnecessary global variables.
7. Avoid duplicated logic.
8. Handle invalid inputs safely.
9. Avoid blocking operations in the game loop.
10. Use constants for configurable values.
11. Handle missing assets gracefully.
12. Ensure all modules can be imported without starting the game.
13. Keep the game runnable using one command.
14. Avoid unnecessary external dependencies.
15. Do not leave placeholder implementations for core functionality.

The code should be understandable to a beginner Python student who wants to learn how the game and its algorithms work.

---

# 19. Functional Acceptance Criteria

The project is considered complete only when all of the following requirements are satisfied.

### Core game

- [ ] Game launches using `python main.py`.
- [ ] Main menu works.
- [ ] How to Play screen works.
- [ ] Three levels are available.
- [ ] Explorer movement works.
- [ ] Hunter movement works.
- [ ] Walls prevent movement.
- [ ] Exit detection works.
- [ ] Capture detection works.

### Algorithms

- [ ] BFS is implemented.
- [ ] DFS is implemented.
- [ ] A* is implemented.
- [ ] Manhattan heuristic is used.
- [ ] A* controls Hunter movement.
- [ ] Hunter recalculates its route.
- [ ] All algorithms return valid results.
- [ ] Algorithm comparisons are displayed.

### Difficulty and challenges

- [ ] Hunter speed increases after every eight successful moves.
- [ ] Challenge questions work.
- [ ] Correct answers grant temporary slowdown.
- [ ] Incorrect answers do not grant slowdown.
- [ ] Slowdown duration is managed correctly.
- [ ] Difficulty progression and slowdown work together.

### Interface

- [ ] Main menu works.
- [ ] HUD displays relevant statistics.
- [ ] Pause and resume work.
- [ ] Restart works.
- [ ] Level completion screen works.
- [ ] Game Over screen works.
- [ ] Final Victory screen works.

### Quality

- [ ] All three levels are solvable.
- [ ] No movement through walls.
- [ ] No crashes due to missing assets.
- [ ] Game loop remains responsive.
- [ ] All core tests pass.
- [ ] Documentation is complete.

---

# 20. Instructions to the AI Coding Agent

You are responsible for building the complete AI Maze Hunter game described in this README.

Treat this document as the primary project specification.

## Development instructions

1. First inspect the existing project directory before creating or modifying files.
2. If a project already exists, preserve useful existing code and integrate changes instead of unnecessarily replacing everything.
3. Set up the complete folder structure.
4. Implement the game in the five development phases described above.
5. Make sure each module is functional before integrating the next.
6. Implement and test the algorithms independently.
7. Integrate A* into the Hunter's movement controller.
8. Implement the three predefined levels.
9. Implement the challenge and power-up systems.
10. Implement all game states and UI screens.
11. Add appropriate assets or create visual fallbacks.
12. Run the application and test the actual gameplay.
13. Fix all errors encountered during testing.
14. Run the test suite after completing the implementation.
15. Update documentation to reflect the actual implementation.

## Critical constraints

- Do not replace Python or Pygame with another technology.
- Do not turn this into a web application.
- Do not replace the grid-based maze with a different game format.
- Do not make the Hunter a manually controlled character.
- Do not make the Explorer AI-controlled.
- Do not use BFS or DFS to control the Hunter.
- Do not make the Hunter teleport.
- Do not allow movement through walls.
- Do not remove the three-level progression.
- Do not remove the coding and logical reasoning challenges.
- Do not remove the dynamic difficulty system.
- Do not make the game dependent on assets that are not included in the repository.
- Do not leave core functionality as TODOs or pseudocode.

## Final deliverables

The completed repository must contain:

1. Fully working Python/Pygame game.
2. All required Python source files.
3. Three predefined and tested maze levels.
4. Working BFS, DFS and A* implementations.
5. Functional Explorer and Hunter mechanics.
6. Functional coding challenge and slowdown systems.
7. Complete menu, gameplay, pause, victory and game-over interfaces.
8. `README.md` with installation, controls and project details.
9. `ARCHITECTURE.md` describing the modules and interactions.
10. `IMPLEMENTATION.md` describing implementation decisions and algorithms.
11. `requirements.txt`.
12. Automated tests.

## Final verification

Before declaring the project complete:

- Run `python -m pip install -r requirements.txt`.
- Run `python -m compileall .`.
- Run the automated test suite.
- Launch the game using `python main.py`.
- Verify the actual gameplay, not just whether the code compiles.
- Test all three levels and the main gameplay mechanics.
- Report any limitations honestly.

Do not claim that a feature has been tested unless it has actually been tested.

---

# 21. Expected Final Outcome

AI Maze Hunter should be a complete, interactive educational game that makes pathfinding understandable through gameplay.

The player should experience the difference between taking an efficient route and making unnecessary detours while being pursued by an intelligent Hunter.

The project should successfully demonstrate:

- How a maze can be represented as a graph.
- How BFS explores nodes level by level.
- How DFS explores paths and backtracks.
- How A* uses actual and estimated costs.
- How an AI agent can dynamically pursue a moving target.
- How movement efficiency affects gameplay.
- How algorithms can be applied in an interactive real-world-style problem.

**Think Smart. Escape the Hunter. Find the Shortest Path.**