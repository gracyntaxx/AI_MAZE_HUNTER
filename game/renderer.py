"""Pygame presentation layer for menus, maze, HUD, and overlays."""

import pygame

from algorithms import astar, bfs, dfs
from config import (
    COLOR_ACCENT,
    COLOR_BG,
    COLOR_BUTTON,
    COLOR_BUTTON_HOVER,
    COLOR_DANGER,
    COLOR_EXPLORER,
    COLOR_EXIT,
    COLOR_FLOOR,
    COLOR_FLOOR_DOT,
    COLOR_HUNTER,
    COLOR_MUTED,
    COLOR_PANEL,
    COLOR_PANEL_BORDER,
    COLOR_SUCCESS,
    COLOR_TEXT,
    COLOR_WALL,
)
from game.engine import MazeGame


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.fonts = {
            "title": pygame.font.Font(None, 64),
            "heading": pygame.font.Font(None, 38),
            "body": pygame.font.Font(None, 25),
            "small": pygame.font.Font(None, 19),
        }
        self.buttons: dict[str, pygame.Rect] = {}

    def draw(self, game: MazeGame) -> None:
        self.screen.fill(COLOR_BG)
        if game.state == "menu":
            self._menu()
        elif game.state == "how":
            self._how_to_play()
        elif game.state == "algorithms":
            self._algorithm_guide(game)
        elif game.state in {"playing", "paused", "challenge", "level_complete", "game_over", "victory"}:
            self._gameplay(game)
            if game.state == "paused":
                self._overlay("PAUSED", ["P / ENTER  Resume", "R  Restart level", "ESC  Main menu"])
            elif game.state == "challenge":
                self._challenge(game)
            elif game.state == "level_complete":
                self._level_complete(game)
            elif game.state == "game_over":
                self._game_over(game)
            elif game.state == "victory":
                self._victory(game)
        pygame.display.flip()

    def _text(
        self,
        value: str,
        x: int,
        y: int,
        color=COLOR_TEXT,
        font: str = "body",
        center: bool = False,
    ) -> pygame.Rect:
        surface = self.fonts[font].render(value, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surface, rect)
        return rect

    def _button(self, name: str, label: str, center: tuple[int, int], width=260) -> None:
        rect = pygame.Rect(0, 0, width, 48)
        rect.center = center
        self.buttons[name] = rect
        color = COLOR_BUTTON_HOVER if rect.collidepoint(pygame.mouse.get_pos()) else COLOR_BUTTON
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, rect, 1, border_radius=8)
        self._text(label, rect.centerx, rect.centery, font="body", center=True)

    def _panel(self, rect: pygame.Rect) -> None:
        pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, rect, 1, border_radius=12)

    def _menu(self) -> None:
        self.buttons.clear()
        self._text("AI MAZE HUNTER", 640, 165, COLOR_ACCENT, "title", True)
        self._text("THINK SMART. ESCAPE THE HUNTER.", 640, 216, COLOR_MUTED, "body", True)
        self._text("A pathfinding game about choosing your route under pressure.", 640, 262, center=True)
        self._button("play", "START ESCAPE", (640, 360))
        self._button("how", "HOW TO PLAY", (640, 422))
        self._button("algorithms", "ALGORITHM LAB", (640, 484))
        self._text("WASD / ARROWS to move   •   P to pause   •   R to restart", 640, 585, COLOR_MUTED, "small", True)
        self._text("Built with Python + Pygame • BFS, DFS, and A*", 640, 628, COLOR_MUTED, "small", True)

    def _how_to_play(self) -> None:
        self.buttons.clear()
        self._text("HOW TO PLAY", 640, 105, COLOR_ACCENT, "title", True)
        lines = [
            "You are the Explorer (peach). Reach the yellow exit before the Hunter catches you.",
            "Move one tile at a time with the arrow keys or W / A / S / D. Walls block movement.",
            "The Hunter replans with A* and moves one cell at a time. Every 8 successful steps",
            "make the Hunter faster. A coding question appears every 7 steps; correct answers",
            "slow the Hunter for 5 seconds. The game pauses while you answer.",
            "",
            "CONTROLS",
            "ARROWS / WASD   Move Explorer          P   Pause / resume",
            "1 / 2 / 3       Answer a question       R   Restart level",
            "ENTER / SPACE   Start / continue        ESC   Menu",
        ]
        y = 206
        for line in lines:
            self._text(line, 180, y, COLOR_TEXT if line else COLOR_MUTED, "body")
            y += 42
        self._button("back", "BACK TO MENU", (640, 680))

    def _algorithm_guide(self, game: MazeGame) -> None:
        self.buttons.clear()
        self._text("ALGORITHM LAB", 640, 75, COLOR_ACCENT, "title", True)
        self._text("Same maze • same start and destination • different search strategies", 640, 125, COLOR_MUTED, "body", True)
        start = game._find("S")
        target = game.exit
        results = (
            ("BFS", bfs(game.grid, start, target), "Queue • explores level by level • shortest path"),
            ("DFS", dfs(game.grid, start, target), "Stack • explores deeply • path is not always shortest"),
            ("A*", astar(game.grid, start, target), "Priority queue • g(n) + h(n) • Hunter's algorithm"),
        )
        y = 205
        for name, result, description in results:
            rect = pygame.Rect(130, y, 1020, 100)
            self._panel(rect)
            self._text(name, 165, y + 18, COLOR_ACCENT, "heading")
            self._text(description, 300, y + 18, font="body")
            self._text(f"Route length: {result.path_length} cells     Nodes explored: {result.explored}", 300, y + 55, COLOR_MUTED, "small")
            y += 126
        self._text("BFS and A* guarantee a shortest route here; DFS is useful for showing backtracking.", 640, 610, COLOR_MUTED, "body", True)
        self._button("back", "BACK TO MENU", (640, 690))

    def _gameplay(self, game: MazeGame) -> None:
        self.buttons.clear()
        self._text("AI MAZE HUNTER", 28, 24, COLOR_ACCENT, "heading")
        self._text(f"LEVEL {game.level_index + 1}  /  3   •   {game.level_name.upper()}", 30, 70, COLOR_MUTED, "small")

        tile = min(34, 710 // len(game.grid[0]), 560 // len(game.grid))
        maze_width = tile * len(game.grid[0])
        maze_height = tile * len(game.grid)
        offset_x = 28
        offset_y = 132 + max(0, (560 - maze_height) // 2)
        board = pygame.Rect(offset_x - 8, offset_y - 8, maze_width + 16, maze_height + 16)
        self._panel(board)

        for row_index, row in enumerate(game.grid):
            for col_index, cell in enumerate(row):
                rect = pygame.Rect(offset_x + col_index * tile, offset_y + row_index * tile, tile, tile)
                if cell == "#":
                    pygame.draw.rect(self.screen, COLOR_WALL, rect)
                    pygame.draw.line(self.screen, COLOR_PANEL_BORDER, rect.topleft, (rect.right, rect.top), 1)
                else:
                    pygame.draw.rect(self.screen, COLOR_FLOOR, rect)
                    pygame.draw.rect(self.screen, COLOR_FLOOR_DOT, rect.inflate(-tile // 2, -tile // 2), border_radius=2)
                pygame.draw.rect(self.screen, COLOR_BG, rect, 1)
                position = (row_index, col_index)
                if position == game.exit:
                    pygame.draw.circle(self.screen, COLOR_EXIT, rect.center, max(5, tile // 3))
                    self._text("X", *rect.center, COLOR_BG, "small", True)
                if position == game.player:
                    pygame.draw.circle(self.screen, COLOR_EXPLORER, rect.center, max(7, tile // 3))
                    pygame.draw.circle(self.screen, (214, 140, 98), rect.center, max(3, tile // 6), 2)
                if position == game.hunter:
                    pygame.draw.circle(self.screen, COLOR_HUNTER, rect.center, max(7, tile // 3))
                    pygame.draw.circle(self.screen, (255, 190, 210), rect.center, max(3, tile // 6), 2)

        side_x = 790
        panel = pygame.Rect(side_x, 132, 455, 345)
        self._panel(panel)
        self._text("RUN STATUS", side_x + 24, 154, COLOR_ACCENT, "heading")
        self._text(f"Moves       {game.stats.moves:>4}", side_x + 24, 211)
        self._text(f"Time           {game.current_time:05.1f}s", side_x + 24, 246)
        self._text(f"Shortest path {game.shortest_path:>4}", side_x + 24, 281)
        self._text(f"Hunter speed   {game.speed_level:>2}", side_x + 24, 316)
        if game.slowdown_remaining > 0:
            self._text(f"SLOWDOWN      {game.slowdown_remaining:0.1f}s", side_x + 24, 351, COLOR_SUCCESS)
        else:
            self._text("Challenges    1 / 2 / 3", side_x + 24, 351, COLOR_MUTED)
        self._text("PATH EFFICIENCY", side_x + 24, 405, COLOR_MUTED, "small")
        bar = pygame.Rect(side_x + 24, 430, 390, 14)
        pygame.draw.rect(self.screen, COLOR_BG, bar, border_radius=7)
        fill_width = int(bar.width * game.efficiency / 100)
        if fill_width:
            pygame.draw.rect(self.screen, COLOR_SUCCESS, (bar.x, bar.y, fill_width, bar.height), border_radius=7)

        info = pygame.Rect(side_x, 493, 455, 170)
        self._panel(info)
        self._text("FIELD NOTES", side_x + 24, 514, COLOR_ACCENT, "body")
        self._text("Hunter uses A*: cost-so-far + estimated", side_x + 24, 552, font="small")
        self._text("distance. Manhattan distance fits this grid.", side_x + 24, 579, font="small")
        self._text("P pause  •  R restart  •  Esc menu", side_x + 24, 620, COLOR_MUTED, "small")
        if game.notice_remaining > 0:
            self._text(game.notice, 640, 690, COLOR_ACCENT, "body", True)
        elif game.challenge_feedback_remaining > 0:
            self._text(game.challenge_feedback, 640, 690, COLOR_SUCCESS, "small", True)

    def _overlay(self, title: str, lines: list[str]) -> None:
        self._dim()
        self._text(title, 640, 300, COLOR_ACCENT, "title", True)
        for index, line in enumerate(lines):
            self._text(line, 640, 370 + index * 42, center=True)

    def _challenge(self, game: MazeGame) -> None:
        self._dim()
        rect = pygame.Rect(190, 195, 900, 425)
        self._panel(rect)
        question = game.current_question
        self._text("QUICK THINK", 640, 237, COLOR_ACCENT, "heading", True)
        self._text(question["question"], 640, 294, center=True)
        for index, option in enumerate(question["options"]):
            self._text(f"{index + 1}.  {option}", 320, 355 + index * 50, font="body")
        self._text("Press 1, 2, or 3. Hunter movement is paused for this question.", 640, 553, COLOR_MUTED, "small", True)

    def _level_complete(self, game: MazeGame) -> None:
        self._dim()
        self._text("LEVEL COMPLETE", 640, 300, COLOR_SUCCESS, "title", True)
        self._text(f"{game.stats.moves} moves  •  shortest route {game.shortest_path}  •  {game.current_time:.1f} seconds", 640, 368, center=True)
        extra = max(0, game.stats.moves - game.shortest_path)
        self._text(f"{extra} extra moves. Efficient routes leave the Hunter fewer chances to catch up.", 640, 410, COLOR_MUTED, "small", True)
        self._text("Press ENTER for the next maze", 640, 485, COLOR_ACCENT, "body", True)

    def _game_over(self, game: MazeGame) -> None:
        self._dim()
        self._text("THE HUNTER CAUGHT YOU", 640, 300, COLOR_DANGER, "title", True)
        self._text(f"Level {game.level_index + 1} • {game.stats.moves} moves • {game.current_time:.1f} seconds survived", 640, 370, center=True)
        self._text("Press R to retry  •  ENTER to return to menu", 640, 440, COLOR_MUTED, "body", True)

    def _victory(self, game: MazeGame) -> None:
        self._dim()
        self._text("YOU ESCAPED THE HUNTER!", 640, 270, COLOR_SUCCESS, "title", True)
        self._text("All three mazes cleared. A* kept replanning as you moved.", 640, 345, center=True)
        self._text(f"Total moves: {game.total_moves}    Play time: {game.total_time:.1f}s", 640, 392, COLOR_MUTED, "body", True)
        self._text("Press ENTER to play again", 640, 470, COLOR_ACCENT, "body", True)

    def _dim(self) -> None:
        veil = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        veil.fill((4, 12, 16, 215))
        self.screen.blit(veil, (0, 0))
