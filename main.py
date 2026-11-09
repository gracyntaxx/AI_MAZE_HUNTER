"""Entry point for AI Maze Hunter (desktop and Pygbag browser builds)."""

import asyncio

import pygame

from config import DIRECTIONS, FPS, SCREEN_HEIGHT, SCREEN_WIDTH, WINDOW_TITLE
from game.engine import MazeGame
from game.renderer import Renderer


MOVE_KEYS = {
    pygame.K_UP: DIRECTIONS["up"],
    pygame.K_w: DIRECTIONS["up"],
    pygame.K_DOWN: DIRECTIONS["down"],
    pygame.K_s: DIRECTIONS["down"],
    pygame.K_LEFT: DIRECTIONS["left"],
    pygame.K_a: DIRECTIONS["left"],
    pygame.K_RIGHT: DIRECTIONS["right"],
    pygame.K_d: DIRECTIONS["right"],
}


async def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    game = MazeGame()
    renderer = Renderer(screen)
    running = True

    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                action = next(
                    (name for name, rect in renderer.buttons.items() if rect.collidepoint(event.pos)),
                    None,
                )
                if action == "play":
                    game.start_level(0)
                elif action == "how":
                    game.state = "how"
                elif action == "algorithms":
                    game.state = "algorithms"
                elif action == "back":
                    game.state = "menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game.state in {"how", "algorithms"}:
                        game.state = "menu"
                    elif game.state not in {"menu", "victory"}:
                        game.state = "menu"
                elif game.state == "menu" and event.key in {pygame.K_RETURN, pygame.K_SPACE}:
                    game.start_level(0)
                elif game.state == "playing":
                    if event.key in MOVE_KEYS:
                        game.move_player(MOVE_KEYS[event.key])
                    elif event.key == pygame.K_p:
                        game.toggle_pause()
                    elif event.key == pygame.K_r:
                        game.restart()
                elif game.state == "paused":
                    if event.key in {pygame.K_p, pygame.K_RETURN}:
                        game.toggle_pause()
                    elif event.key == pygame.K_r:
                        game.restart()
                elif game.state == "challenge" and event.key in {pygame.K_1, pygame.K_2, pygame.K_3}:
                    game.submit_answer(event.key - pygame.K_1)
                elif game.state == "level_complete" and event.key in {pygame.K_RETURN, pygame.K_SPACE}:
                    game.continue_level()
                elif game.state == "game_over":
                    if event.key == pygame.K_r:
                        game.restart()
                    elif event.key in {pygame.K_RETURN, pygame.K_SPACE}:
                        game.state = "menu"
                elif game.state == "victory" and event.key in {pygame.K_RETURN, pygame.K_SPACE}:
                    game.total_moves = 0
                    game.total_time = 0.0
                    game.start_level(0)

        game.tick(dt)
        renderer.draw(game)
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
