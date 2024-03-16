# -*- coding: utf-8 -*-
import pygame
import sys
from pygame.locals import *

pygame.init()


class ChemicalReaction:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('chemical reaction')
        self.clock = pygame.time.Clock()
        self.scenep = SceneStart()
        self.game_run = True

    def run_game(self):

        self.scenep.load_img()

        while self.game_run:
            self._cheak_event()

            self.screen.fill(self.scenep.bg)
            self.screen.blit(self.scenep.set_scene, (400, 300))
            pygame.display.update()
            self.clock.tick(60)

    def _cheak_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 400 <= mouse_x <= 500:
                    if 300 <= mouse_y <= 375:
                        if self.scenep.name == 'start':
                            self.scenep = SceneGame()
                            self.scenep.load_img()
                        elif self.scenep.name == 'game':
                            self.scenep = SceneStart()
                            self.scenep.load_img()


class SceneStart:
    def __init__(self):
        self.name = 'start'
        self.bg = (255, 255, 255)  # 白色

    def load_img(self):
        self.set_scene = pygame.image.load('image/set_scene.png')  # 100*75


class SceneGame:
    def __init__(self):
        self.name = 'game'
        self.bg = (0, 0, 0)  # 黑色

    def load_img(self):
        self.set_scene = pygame.image.load('image/set_scene.png')


if __name__ == '__main__':
    cr = ChemicalReaction()
    cr.run_game()
