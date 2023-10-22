# -*- coding: utf-8 -*-
import pygame
import random
import sys
from pygame.locals import *

pygame.init()


class ChemicalReaction():
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Ballon')
        self.clock = pygame.time.Clock()
        self.balloon_number = 0

        self.game_run = True

    def run_game(self):

        self.balloons = pygame.sprite.Group()

        while self.game_run:
            self._cheak_event()
            self.load_image()
            self._create_balloon()
            self._update_balloon()

            self.update_screen()
            pygame.display.update()
            self.clock.tick(60)

    def update_screen(self):
        self.screen.fill((135, 180, 255))
        self.screen.blit(self.bg, (0, 0))
        self.balloons.draw(self.screen)
        self.screen.blit(self.topic[0], (60, 500))

    def _cheak_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def load_image(self):
        self.bg_tmp = pygame.image.load('image/bg_skies.png')
        self.bg = pygame.transform.scale(self.bg_tmp, (800, 600))
        self.balloon_tmp = pygame.image.load('image/balloon.png')
        self.balloon = pygame.transform.rotozoom(self.balloon_tmp, 0, 0.1)  # 984*1420
        self.topic = [
            pygame.image.load('image/1_1.png')  # 684*40
        ]
        self.answer_image = [
            pygame.image.load('image/2_1.png'),  # 234*190
            pygame.image.load('image/2_2.png'),
            pygame.image.load('image/2_3.png'),
            pygame.image.load('image/2_4.png')
        ]

    def _create_balloon(self):
        if self.balloon_number != 4:
            balloon_number_x = [80, 280, 480, 680]
            a = 0
            for num in balloon_number_x:
                self.answer_images = pygame.transform.rotozoom(self.answer_image[a], 0, 0.1)
                a += 1
                balloons = Balloon(self.answer_images, self, self.answer_image)
                balloons.rect.x = num
                self.balloons.add(balloons)
                self.balloon_number += 1

    def _cheak_balloon_y(self):
        for balloon in self.balloons:
            if balloon.rect.y >= 510:
                self.balloons.remove(balloon)
                self.balloon_number = 0

    def _update_balloon(self):
        self.balloons.update()
        self._cheak_balloon_y()


class Balloon(pygame.sprite.Sprite):
    def __init__(self, image, balloon, Answer_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.screen = balloon.screen
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = 10
        self.speed = 3

    def update(self):
        self.rect.y += self.speed


if __name__ == '__main__':
    cr = ChemicalReaction()
    cr.run_game()
