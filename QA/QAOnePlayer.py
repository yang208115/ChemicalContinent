# coding=gbk
import pygame
import sys

pygame.init()


class QAOnePlater:
    def __init__(self, clock, scene):
        self.screen = scene.screen
        self.scene = scene
        pygame.display.set_caption('Chemistry QA one player')
        self.clock = clock
        self.if_game_run = True

    def run_game(self):
        self.load_img()
        while self.if_game_run:
            self.check_events()
            self.update_screen()

            pygame.display.update()
            self.clock.tick(60)

    def load_img(self):
        pass

    def update_screen(self):
        pass

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.cheak_mouse(mouse_x, mouse_y)

    def cheak_mouse(self,x ,y):
        pass
