# -*- coding: utf-8 -*-
import pygame


class Balloon(pygame.sprite.Sprite):
    def __init__(self, image, balloon, answer_id):
        super().__init__()
        self.answer_id = answer_id
        self.image = image
        self.screen = balloon.screen
        self.balloon = balloon
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = 10
        self.speed = self.balloon.balloon_speed

    def update(self):
        self.rect.y += self.speed

    def check_answer(self):
        if self.balloon.topic_id == self.answer_id:
            self.balloon.reset_balloon()
        elif self.balloon.topic_id != self.answer_id:
            self.balloon.score -= 1
            self.balloon.remove_balloon()


class BalloonLeft(pygame.sprite.Sprite):
    def __init__(self, image, balloon, answer_id):
        super().__init__()
        self.answer_id = answer_id
        self.image = image
        self.screen = balloon.screen
        self.balloon = balloon
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = 10
        self.speed = self.balloon.balloon_speed_left

    def update(self):
        self.rect.y += self.speed

    def check_answer(self):
        if self.balloon.topic_id_left == self.answer_id:
            self.balloon.reset_balloon_left()
        elif self.balloon.topic_id_left != self.answer_id:
            self.balloon.score[0] -= 1
            self.balloon.remove_balloon_left()


class BalloonRight(pygame.sprite.Sprite):
    def __init__(self, image, balloon, answer_id):
        super().__init__()
        self.answer_id = answer_id
        self.image = image
        self.screen = balloon.screen
        self.balloon = balloon
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = 10
        self.speed = self.balloon.balloon_speed_right

    def update(self):
        self.rect.y += self.speed

    def check_answer(self):
        if self.balloon.topic_id_right == self.answer_id:
            self.balloon.reset_balloon_right()
        elif self.balloon.topic_id_right != self.answer_id:
            self.balloon.score[1] -= 1
            self.balloon.remove_balloon_right()
