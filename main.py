import pygame
import sys
from settings import *
from display import display
from typing import *
class Game():
    def __init__(self):
        pygame.display.set_caption("Typing Test")
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    typeGame.type(pygame.key.name(event.key))





            screen.fill("#636e72")
            display()
            pygame.display.update()
            self.clock.tick(FPS)

game = Game()

game.run()