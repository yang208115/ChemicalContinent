# -*- coding: utf-8 -*-
import pygame
import random
import sys

pygame.init()


class Balloons():
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Balloon')
        self.clock = pygame.time.Clock()
        self.balloon_number = 0
        self.topic_show = False
        self.topic_id = 0
        self.score = 0

        self.game_run = True
        self.if_game_over = False

    def run_game(self):

        self.balloons = pygame.sprite.Group()

        while self.game_run:
            self._check_event()
            self.load_image()
            self.create_balloon()
            self.update_balloon()
            self.set_show_score()
            self.game_over()

            self.update_screen()
            pygame.display.update()
            self.clock.tick(60)

    def update_screen(self):
        if not self.if_game_over:
            self.screen.fill((135, 180, 255))
            self.screen.blit(self.bg, (0, 0))
            self.balloons.draw(self.screen)
            self.create_answer()
            self.screen.blit(self.score_text, (40, 20))

        if self.if_game_over:
            self.screen.blit(self.game_over_img, (200, 100))
            self.screen.blit(self.start_game, (500, 380))

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
        self.game_over_img_tmp = pygame.image.load('image/game_over.png')
        self.game_over_img = pygame.transform.scale(self.game_over_img_tmp, (400, 200))
        self.start_game = pygame.image.load('image/start_game.png')
        self.topic = [
            pygame.image.load('image/1_1.png'),  # 684*40
            pygame.image.load('image/2_1.png'),
            pygame.image.load('image/3_1.png'),
            pygame.image.load('image/4_1.png')
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
                Answer_id = b[a]
                self.answer_images = pygame.transform.rotozoom(self.answer_image[b[a]], 0, 0.1)
                a += 1
                balloons = Balloon(self.answer_images, self, Answer_id)
                balloons.rect.x = num
                self.balloons.add(balloons)
                self.balloon_number += 1

    def create_answer(self):
        if self.topic_show == False:
            self.topic_id = random.randint(0, 3)
        self.screen.blit(self.topic[self.topic_id], (60, 500))
        self.topic_show = True

    def remove_balloon(self):
        for balloon in self.balloons:
            self.balloons.remove(balloon)
            self.balloon_number = 0
            self.topic_show = False

    def _check_balloon_y(self):
        for balloon in self.balloons:
            if balloon.rect.y >= 510:
                self.score -= 1
                break
        for balloon in self.balloons:
            if balloon.rect.y >= 510:
                self.remove_balloon()

    def update_balloon(self):
        self.balloons.update()
        self._check_balloon_y()

    def check_moues(self, x, y):
        for balloon in self.balloons:
            if balloon.rect.y <= y <= balloon.rect.y + 243:
                if balloon.rect.x <= x <= balloon.rect.x + 190:
                    balloon.check_Answer()

        if 500 <= x <= 500 + 200:
            if 380 <= y <= 380 + 100:
                self.remove_balloon()
                self.create_balloon()
                self.score = 0
                self.if_game_over = False

    def reset_balloon(self):
        self.score += 1
        self.remove_balloon()
    def set_show_score(self):
        self.score_text_tmp = " 得分：" + str(self.score)
        self.font = pygame.font.Font("c:/windows/Fonts/simhei.ttf", 30)
        self.score_text = self.font.render(self.score_text_tmp, True, (255, 255, 255))

    def game_over(self):
        if self.score < 0:
            self.if_game_over = True


class Balloon(pygame.sprite.Sprite):
    def __init__(self, image, balloon, Answer_id):
        pygame.sprite.Sprite.__init__(self)
        self.answer_id = Answer_id
        self.image = image
        self.screen = balloon.screen
        self.balloon = balloon
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = 10
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

    def check_Answer(self):
        if self.balloon.topic_id == self.answer_id:
            self.balloon.reset_balloon()
        elif self.balloon.topic_id != self.answer_id:
            self.balloon.score -= 1
            self.balloon.remove_balloon()

if __name__ == '__main__':
    cr = Balloons()
    cr.run_game()
