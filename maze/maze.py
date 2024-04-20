# coding=gbk
import sys
import pygame


class ChemistryGame:
    def __init__(self, clock, scene):
        self.screen = scene.screen
        self.scene = scene
        pygame.display.set_caption('Chemistry maze')
        self.clock = clock

        self.if_game_run = True

        pygame.mixer.music.load('./Musics/musics.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    def run_game(self):
        self.load_img()

        while self.if_game_run:

            self.update_screen()
            self._check_event()
            pygame.display.update()
            self.clock.tick(60)

    def load_img(self):
        pass

    def update_screen(self):
        pass

    def _check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.if_game_over = True
                self.if_stop = True
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                moues_x, moues_y = pygame.mouse.get_pos()
                self.check_moues(moues_x, moues_y)
            elif event.type == pygame.K_p:
                self.if_stop = True
                pygame.quit()
                sys.exit()

    def check_moues(self, x, y):
        pass
