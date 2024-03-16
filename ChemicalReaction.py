# -*- coding: utf-8 -*-
import pygame
import sys
from pygame.locals import *

pygame.init()


# noinspection PyAttributeOutsideInit
class ChemicalReaction:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('chemical reaction')
        self.clock = pygame.time.Clock()

        self.game_run = True

    def run_game(self):
        while self.game_run:
            self._cheak_event()
            self.load_image()

            self.screen.fill((135, 180, 255))
            self.screen.blit(self.o2, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def _cheak_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def load_image(self):
        self.o2_tmp = pygame.image.load('image/o2.png')
        self.o2 = pygame.transform.rotozoom(self.o2_tmp, 0, 0.3)


if __name__ == '__main__':
    cr = ChemicalReaction()
    cr.run_game()
