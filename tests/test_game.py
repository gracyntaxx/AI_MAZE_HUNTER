import unittest

from algorithms import astar, bfs, dfs
from game.engine import MazeGame, MIN_HUNTER_INTERVAL
from levels import LEVELS


class SearchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.grid = [
            list("#######"),
            list("#     #"),
            list("# ### #"),
            list("#     #"),
            list("#######"),
        ]

    def test_bfs_and_astar_find_shortest_path(self) -> None:
        source, target = (1, 1), (3, 5)
        breadth = bfs(self.grid, source, target)
        informed = astar(self.grid, source, target)
        self.assertTrue(breadth.found)
        self.assertEqual(breadth.path_length, informed.path_length)
        self.assertEqual(breadth.path[0], source)
        self.assertEqual(breadth.path[-1], target)

    def test_dfs_finds_a_valid_path(self) -> None:
        result = dfs(self.grid, (1, 1), (3, 5))
        self.assertTrue(result.found)
        self.assertEqual(result.path[0], (1, 1))
        self.assertEqual(result.path[-1], (3, 5))
        for row, col in result.path:
            self.assertNotEqual(self.grid[row][col], "#")

    def test_unreachable_and_same_position(self) -> None:
        grid = [list("#####"), list("# # #"), list("#####")]
        self.assertFalse(astar(grid, (1, 1), (1, 3)).found)
        self.assertEqual(bfs(grid, (1, 1), (1, 1)).path, [(1, 1)])

    def test_invalid_wall_position_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            bfs(self.grid, (0, 0), (1, 1))


class GameTests(unittest.TestCase):
    def setUp(self) -> None:
        self.game = MazeGame()

    def test_all_levels_are_connected_and_searchable(self) -> None:
        for level in LEVELS:
            grid = [list(row) for row in level["rows"]]
            start = next((r, c) for r, row in enumerate(grid) for c, cell in enumerate(row) if cell == "S")
            goal = next((r, c) for r, row in enumerate(grid) for c, cell in enumerate(row) if cell == "X")
            self.assertTrue(astar(grid, start, goal).found, level["name"])

    def test_wall_move_does_not_count(self) -> None:
        self.game.start_level(0)
        self.assertFalse(self.game.move_player((0, -1)))
        self.assertEqual(self.game.stats.moves, 0)

    def test_correct_answer_applies_temporary_slowdown(self) -> None:
        self.game.start_level(0)
        self.game.state = "challenge"
        normal_interval = self.game.effective_hunter_interval
        self.assertTrue(self.game.submit_answer(self.game.current_question["answer"]))
        self.assertGreater(self.game.effective_hunter_interval, normal_interval)
        self.game.tick(5.1)
        self.assertEqual(self.game.slowdown_remaining, 0)

    def test_wrong_answer_does_not_slow_hunter(self) -> None:
        self.game.start_level(0)
        self.game.state = "challenge"
        answer = self.game.current_question["answer"]
        self.assertFalse(self.game.submit_answer((answer + 1) % 3))
        self.assertEqual(self.game.slowdown_remaining, 0)

    def test_pause_stops_game_timer(self) -> None:
        self.game.start_level(0)
        self.game.toggle_pause()
        elapsed = self.game.current_time
        self.game.tick(4)
        self.assertEqual(self.game.current_time, elapsed)
        self.assertEqual(self.game.state, "paused")

    def test_hunter_moves_one_cell_along_astar_path(self) -> None:
        self.game.start_level(0)
        old_position = self.game.hunter
        route = astar(self.game.grid, self.game.hunter, self.game.player).path
        self.game._move_hunter()
        self.assertEqual(self.game.hunter, route[1])
        self.assertEqual(
            abs(old_position[0] - self.game.hunter[0])
            + abs(old_position[1] - self.game.hunter[1]),
            1,
        )

    def test_hunter_speed_increases_only_after_successful_moves(self) -> None:
        self.game.start_level(0)
        initial_interval = self.game.hunter_interval
        self.game.move_player((0, -1))
        self.assertEqual(self.game.hunter_interval, initial_interval)
        self.game.challenge_index = 3
        for _ in range(8):
            current, following = self.game.path_hint[:2]
            self.game.move_player((following[0] - current[0], following[1] - current[1]))
        self.assertLess(self.game.hunter_interval, initial_interval)
        self.assertGreaterEqual(self.game.hunter_interval, MIN_HUNTER_INTERVAL)

    def test_challenge_freezes_the_game_clock(self) -> None:
        self.game.start_level(0)
        self.game.state = "challenge"
        self.game.stats.elapsed_before_pause = 12.5
        self.game.stats.started_at -= 20
        self.assertEqual(self.game.current_time, 12.5)


if __name__ == "__main__":
    unittest.main()
