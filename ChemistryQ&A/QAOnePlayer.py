# coding=gbk
import pygame
import sys

pygame.init()


class QAOnePlater:
    def __init__(self, clock, scene):
        self.screen = scene.screen
        self.scene = scene
        pygame.display.set_caption('Chemistry Q&A one player')
        self.clock = clock
        self.if_game_run = True

    def run_game(self):
        self.load_image()

        while self.if_game_run:
            self.update_screen()
            self._check_event()

            pygame.display.update()
            self.clock.tick(60)

    def load_image(self):
        self.player1 = pygame.image.load('image/player1.png')  # 80*120
        self.bg = pygame.image.load('image/bg.png')
        self.answer_box = pygame.image.load('image/AnswerBox.png')  # 400*300
        self.button_pairs_tmp = pygame.image.load('image/button_pairs.png')  # 200*200
        self.button_error_tmp = pygame.image.load('image/button_error.png')  # 200*200

    def update_screen(self):
        if self.if_game_run:
            self.screen.fill((135, 180, 255))
            self.screen.blit(self.bg, (0, 0))

            self.screen.blit(self.player1, (360, 450))
            self.screen.blit(self.answer_box, (200, 50))

    def _check_event(self):
        """检查事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                moues_x, moues_y = pygame.mouse.get_pos()
                self.check_moues(moues_x, moues_y)

    def check_moues(self, x, y):
        pass
