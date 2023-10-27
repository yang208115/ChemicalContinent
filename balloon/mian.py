# -*- coding: utf-8 -*-
import pygame
import random
import sys

pygame.init()


class ChemicalReaction():
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Balloon')
        self.clock = pygame.time.Clock()
        self.balloon_number = 0
        self.topic_show = False
        self.topic_id = 0

        self.game_run = True

    def run_game(self):

        self.balloons = pygame.sprite.Group()

        while self.game_run:
            self._check_event()
            self.load_image()
            self.create_balloon()
            self._update_balloon()

            self.update_screen()
            pygame.display.update()
            self.clock.tick(60)

    def update_screen(self):
        self.screen.fill((135, 180, 255))
        self.screen.blit(self.bg, (0, 0))
        self.balloons.draw(self.screen)
        self.create_answer()

    def _check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                moues_x, moues_y = pygame.mouse.get_pos()
                self.check_moues(moues_x, moues_y)

    def load_image(self):
        self.bg_tmp = pygame.image.load('image/bg_skies.png')
        self.bg = pygame.transform.scale(self.bg_tmp, (800, 600))
        self.balloon_tmp = pygame.image.load('image/balloon.png')
        self.balloon = pygame.transform.rotozoom(self.balloon_tmp, 0, 0.1)  # 984*1420
        self.topic = [
            pygame.image.load('image/1_1.png'),  # 684*40
            pygame.image.load('image/2_1.png')
        ]
        self.answer_image = [
            pygame.image.load('image/1_2.png'),  # 234*190
            pygame.image.load('image/2_2.png'),
            pygame.image.load('image/3_2.png'),
            pygame.image.load('image/4_2.png')
        ]

    def create_balloon(self):
        if self.balloon_number != 4:
            balloon_number_x = [80, 280, 480, 680]
            a = 0
            b = random.sample([i for i in range(0, 4)], 4)
            for num in balloon_number_x:
                Answer_id = random.randint(1, 4)
                self.answer_images = pygame.transform.rotozoom(self.answer_image[b[a]], 0, 0.1)
                a += 1
                balloons = Balloon(self.answer_images, self, Answer_id)
                balloons.rect.x = num
                self.balloons.add(balloons)
                self.balloon_number += 1

    def create_answer(self):
        if self.topic_show == False:
            self.topic_id = random.randint(0, 1)
        self.screen.blit(self.topic[self.topic_id], (60, 500))
        self.topic_show = True


    def _check_balloon_y(self):
        for balloon in self.balloons:
            if balloon.rect.y >= 510:
                self.balloons.remove(balloon)
                self.balloon_number = 0
                self.topic_show =  False

    def _update_balloon(self):
        self.balloons.update()
        self._check_balloon_y()

    def check_moues(self, x, y):
        for balloon in self.balloons:
            if balloon.rect.y <= y <= balloon.rect.y + 243:
                if balloon.rect.x <= x <= balloon.rect.x + 190:
                    balloon.check_Answer()


class Balloon(pygame.sprite.Sprite):
    def __init__(self, image, balloon, Answer_id):
        pygame.sprite.Sprite.__init__(self)
        self.answer_id = Answer_id
        self.image = image
        self.screen = balloon.screen
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = 10
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

    def check_Answer(self):
        print(self.answer_id)


if __name__ == '__main__':
    cr = ChemicalReaction()
    cr.run_game()
