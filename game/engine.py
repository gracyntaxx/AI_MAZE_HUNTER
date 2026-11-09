"""Frame-rate-independent rules and state transitions for the maze game."""

from dataclasses import dataclass
from time import monotonic

from algorithms import astar, bfs
from game.challenges import is_correct, question_for
from levels import LEVELS

Position = tuple[int, int]

BASE_SLOWDOWN_SECONDS = 5.0
SLOWDOWN_MULTIPLIER = 1.65
MOVES_PER_SPEED_UP = 8
SPEED_UP_SECONDS = 0.045
MIN_HUNTER_INTERVAL = 0.24
CHALLENGE_MOVE_INTERVAL = 7
CHALLENGES_PER_LEVEL = 3


@dataclass
class LevelStats:
    moves: int = 0
    started_at: float = 0.0
    elapsed_before_pause: float = 0.0


class MazeGame:
    """Owns gameplay state; the renderer and input layer remain separate."""

    def __init__(self) -> None:
        self.level_index = 0
        self.state = "menu"
        self.level: dict = {}
        self.grid: list[list[str]] = []
        self.player: Position = (0, 0)
        self.hunter: Position = (0, 0)
        self.exit: Position = (0, 0)
        self.stats = LevelStats()
        self.hunter_interval = 0.7
        self.hunter_elapsed = 0.0
        self.slowdown_remaining = 0.0
        self.challenge_index = 0
        self.challenge_feedback = ""
        self.challenge_feedback_remaining = 0.0
        self.total_moves = 0
        self.total_time = 0.0
        self.notice = ""
        self.notice_remaining = 0.0
        self.path_hint: list[Position] = []
        self.start_level(0, begin=False)

    def start_level(self, index: int, begin: bool = True) -> None:
        self.level_index = index
        self.level = LEVELS[index]
        self.grid = [list(row) for row in self.level["rows"]]
        self.player = self._find("S")
        self.hunter = self._find("H")
        self.exit = self._find("X")
        self.stats = LevelStats(started_at=monotonic())
        self.hunter_interval = self.level["hunter_interval"]
        self.hunter_elapsed = 0.0
        self.slowdown_remaining = 0.0
        self.challenge_index = 0
        self.challenge_feedback = ""
        self.challenge_feedback_remaining = 0.0
        self.path_hint = []
        self.state = "playing" if begin else "menu"
        self.update_path_hint()

    def _find(self, token: str) -> Position:
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                if cell == token:
                    return row_index, col_index
        raise ValueError(f"Level {self.level_index + 1} has no {token} cell.")

    @property
    def level_name(self) -> str:
        return self.level["name"]

    @property
    def current_time(self) -> float:
        if self.state == "playing":
            return self.stats.elapsed_before_pause + monotonic() - self.stats.started_at
        return self.stats.elapsed_before_pause

    @property
    def effective_hunter_interval(self) -> float:
        if self.slowdown_remaining > 0:
            return self.hunter_interval * SLOWDOWN_MULTIPLIER
        return self.hunter_interval

    @property
    def speed_level(self) -> int:
        return 1 + self.stats.moves // MOVES_PER_SPEED_UP

    @property
    def shortest_path(self) -> int:
        return bfs(self.grid, self._find("S"), self.exit).path_length

    @property
    def efficiency(self) -> float:
        if not self.stats.moves:
            return 0.0
        return min(100.0, self.shortest_path / self.stats.moves * 100.0)

    @property
    def current_question(self) -> dict:
        return question_for(self.level_index, self.challenge_index)

    def update_path_hint(self) -> None:
        self.path_hint = astar(self.grid, self.player, self.exit).path

    def move_player(self, delta: Position) -> bool:
        if self.state != "playing":
            return False
        row, col = self.player
        destination = row + delta[0], col + delta[1]
        if not self._walkable(destination):
            return False
        self.player = destination
        self.stats.moves += 1
        self.total_moves += 1
        self.update_path_hint()

        if self.player == self.exit:
            self._complete_level()
            return True
        if self.player == self.hunter:
            self._freeze_clock()
            self.state = "game_over"
            return True
        if self.stats.moves % MOVES_PER_SPEED_UP == 0:
            self.hunter_interval = max(
                MIN_HUNTER_INTERVAL, self.hunter_interval - SPEED_UP_SECONDS
            )
            self._notify("HUNTER SPEED INCREASED")
        if (
            self.stats.moves % CHALLENGE_MOVE_INTERVAL == 0
            and self.challenge_index < CHALLENGES_PER_LEVEL
        ):
            self._freeze_clock()
            self.state = "challenge"
            self.hunter_elapsed = 0.0
        return True

    def submit_answer(self, answer_index: int) -> bool:
        if self.state != "challenge":
            return False
        correct = is_correct(self.current_question, answer_index)
        question = self.current_question
        if correct:
            self.slowdown_remaining = BASE_SLOWDOWN_SECONDS
            self.challenge_feedback = "Correct! Hunter slowed for 5 seconds."
        else:
            self.challenge_feedback = (
                f"Not quite. {question['explanation']}"
            )
        self.challenge_feedback_remaining = 2.2
        self.challenge_index += 1
        self.stats.started_at = monotonic()
        self.state = "playing"
        return correct

    def tick(self, dt: float) -> None:
        if self.state != "playing":
            return
        self.total_time += dt
        if self.slowdown_remaining > 0:
            self.slowdown_remaining = max(0.0, self.slowdown_remaining - dt)
        if self.challenge_feedback_remaining > 0:
            self.challenge_feedback_remaining = max(
                0.0, self.challenge_feedback_remaining - dt
            )
        if self.notice_remaining > 0:
            self.notice_remaining = max(0.0, self.notice_remaining - dt)
        self.hunter_elapsed += dt
        if self.hunter_elapsed >= self.effective_hunter_interval:
            self.hunter_elapsed = 0.0
            self._move_hunter()

    def _move_hunter(self) -> None:
        result = astar(self.grid, self.hunter, self.player)
        if len(result.path) > 1:
            self.hunter = result.path[1]
        if self.hunter == self.player:
            self._freeze_clock()
            self.state = "game_over"

    def _walkable(self, position: Position) -> bool:
        row, col = position
        return (
            0 <= row < len(self.grid)
            and 0 <= col < len(self.grid[0])
            and self.grid[row][col] != "#"
        )

    def _complete_level(self) -> None:
        self._freeze_clock()
        if self.level_index == len(LEVELS) - 1:
            self.state = "victory"
        else:
            self.state = "level_complete"

    def toggle_pause(self) -> None:
        if self.state == "playing":
            self._freeze_clock()
            self.state = "paused"
        elif self.state == "paused":
            self.stats.started_at = monotonic()
            self.state = "playing"

    def restart(self) -> None:
        self.start_level(self.level_index)

    def continue_level(self) -> None:
        if self.state == "level_complete":
            self.start_level(self.level_index + 1)

    def _notify(self, message: str) -> None:
        self.notice = message
        self.notice_remaining = 2.0

    def _freeze_clock(self) -> None:
        if self.state == "playing":
            self.stats.elapsed_before_pause = self.current_time
