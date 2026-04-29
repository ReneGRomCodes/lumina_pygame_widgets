"""
Main PyGame loop for testing/development.
"""
import pygame
import sys


def run_lumina() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock, framerate = pygame.time.Clock(), 30

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill([255, 255, 255])
        screen.blit(screen, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(framerate)


if __name__  == "__main__":
    run_lumina()
