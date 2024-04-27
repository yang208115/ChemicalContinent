# coding=gbk
import sys
import pygame


class Maze:
    def __init__(self, clock, scene):
        self.screen = scene.screen
        self.scene = scene
        pygame.display.set_caption('Chemistry maze')
        self.clock = clock
        self.player_pos = [
            [50, 504],  # 开始 0
            [105, 490],  # S 1
            [170, 400],  # O2 2
            [290, 508],  # NaOH 3
            [410, 410],  # O2 4
            [605, 460],  # KOH 5
            [615, 545],  # 出口下 6
            [420, 360],  # H2O 7
            [675, 305],  # O2 8
            [620, 220],  # CuO 9
            [600, 125],  # BaCl 10
            [730, 75]  # 出口右 11
        ]
        self.player_poss = 0
        self.score = 0

        self.if_game_run = True
        self.if_win = False
        self.if_fail = False

        self.if_ys_show = [
            True,  # S 0
            True,  # N2 1
            True,  # O2 2
            True,  # O2 3
            True,  # O2 4
            True,  # O2 5
            True,  # NaOH 6
            True,  # nH2SO4 7
            True,  # H2O 8
            True,  # KOH 9
            True,  # AgCl 10
            True,  # CO2 11
            True,  # CUO 12
            True  # BaCl2 13
        ]

        pygame.mixer.music.load('./Musics/musics.mp3')
        self.font = pygame.font.Font('./Fonts/simsun.ttc', 48)
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
        self.background_tmp = pygame.image.load("./image/bg_skies.png")
        self.background = pygame.transform.scale(self.background_tmp, (800, 600))
        self.return_tmp = pygame.image.load("./image/return.png")
        self.return_ = pygame.transform.scale(self.return_tmp, (80, 80))
        self.maze_tmp = pygame.image.load("./image/maze.png")
        self.maze = pygame.transform.rotozoom(self.maze_tmp, 0, 0.8)
        self.maze3_tmp = pygame.image.load("./image/maze3.png")
        self.ys_S_tmp = pygame.image.load("./image/ys1/S.png")
        self.ys_S = pygame.transform.rotozoom(self.ys_S_tmp, 0, 0.6)
        self.ys_S_pos = self.ys_S.get_rect()
        self.ys_N2_tmp = pygame.image.load("./image/ys1/N2.png")
        self.ys_N2 = pygame.transform.rotozoom(self.ys_N2_tmp, 0, 0.5)
        self.ys_N2_pos = self.ys_N2.get_rect()
        self.ys_O2_tmp = pygame.image.load("./image/ys1/O2.png")
        self.ys_O2 = pygame.transform.rotozoom(self.ys_O2_tmp, 0, 0.5)
        self.ys_O2_pos = self.ys_O2.get_rect()
        self.ys_NaOH_tmp = pygame.image.load("./image/ys1/NaOH.png")
        self.ys_NaOH = pygame.transform.rotozoom(self.ys_NaOH_tmp, 0, 0.4)
        self.ys_NaOH_pos = self.ys_NaOH.get_rect()
        self.ys_nH2SO4_tmp = pygame.image.load("./image/ys1/nH2So4.png")
        self.ys_nH2SO4 = pygame.transform.rotozoom(self.ys_nH2SO4_tmp, 0, 0.3)
        self.ys_nH2SO4_pos = self.ys_nH2SO4.get_rect()
        self.ys_H2O_tmp = pygame.image.load("./image/ys1/H2O.png")
        self.ys_H2O = pygame.transform.rotozoom(self.ys_H2O_tmp, 0, 0.3)
        self.ys_H2O_pos = self.ys_H2O.get_rect()
        self.ys_KOH_tmp = pygame.image.load("./image/ys1/KOH.png")
        self.ys_KOH = pygame.transform.rotozoom(self.ys_KOH_tmp, 0, 0.3)
        self.ys_KOH_pos = self.ys_KOH.get_rect()
        self.ys_AgCl_tmp = pygame.image.load("./image/ys1/AgCl.png")
        self.ys_AgCl = pygame.transform.rotozoom(self.ys_AgCl_tmp, 0, 0.3)
        self.ys_AgCl_pos = self.ys_AgCl.get_rect()
        self.ys_CO2_tmp = pygame.image.load("./image/ys1/CO2.png")
        self.ys_CO2 = pygame.transform.rotozoom(self.ys_CO2_tmp, 0, 0.3)
        self.ys_CO2_pos = self.ys_CO2.get_rect()
        self.ys_CUO_tmp = pygame.image.load("./image/ys1/CUO.png")
        self.ys_CUO = pygame.transform.rotozoom(self.ys_CUO_tmp, 0, 0.3)
        self.ys_CUO_pos = self.ys_CUO.get_rect()
        self.ys_BaCl2_tmp = pygame.image.load("./image/ys1/BaCl2.png")
        self.ys_BaCl2 = pygame.transform.rotozoom(self.ys_BaCl2_tmp, 0, 0.3)
        self.ys_BaCl2_pos = self.ys_BaCl2.get_rect()
        self.scoreboard_wim = pygame.image.load("image/scoreboard.png")
        self.scoreboard_fail = pygame.image.load("image/scoreboard2.png")
        self.next_level_tmp = pygame.image.load('image/next_level.png')
        self.next_level = pygame.transform.rotozoom(self.next_level_tmp, 0, 0.5)
        self.return_main_scene_tmp = pygame.image.load('image/return_main_scene.png')
        self.return_main_scene = pygame.transform.rotozoom(self.return_main_scene_tmp, 0, 0.5)
        self.return_select_sLevel_tmp = pygame.image.load('image/return_select_aLevel.png')
        self.return_select_sLevel = pygame.transform.rotozoom(self.return_select_sLevel_tmp, 0, 0.5)

    def update_screen(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.maze3_tmp, (80, 60))
        self.screen.blit(self.maze, (80, 60))
        self.show_ys()

        pygame.draw.rect(self.screen, (255, 255, 0), [self.player_pos[self.player_poss][0], self.player_pos
        [self.player_poss][1], 25, 25], 0)

        if self.if_win:
            self.score_text = self.font.render(str(self.score), True, (0, 0, 0))
            self.screen.blit(self.scoreboard_wim, (150, 100))
            self.screen.blit(self.score_text, (318, 318))
            self.screen.blit(self.next_level, (550, 500))
            self.screen.blit(self.return_select_sLevel, (330, 500))
            self.screen.blit(self.return_main_scene, (110, 500))

        if self.if_fail:
            self.score_text = self.font.render(str(self.score), True, (0, 0, 0))
            self.screen.blit(self.scoreboard_fail, (150, 100))
            self.screen.blit(self.score_text, (318, 318))
            self.screen.blit(self.next_level, (550, 500))
            self.screen.blit(self.return_select_sLevel, (330, 500))
            self.screen.blit(self.return_main_scene, (110, 500))

        self.screen.blit(self.return_, (10, 10))

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
        self.check_moues_click_ys(x, y)
        if 10 <= x <= 90 and 10 <= y <= 90:
            pygame.mixer.music.stop()
            self.scene.set_main_scene()
        if self.if_fail:
            if 110 <= x <= 110+170:
                if 500 <= y <= 500+60:
                    pygame.mixer.music.stop()
                    self.scene.set_main_scene()
            if 330 <= x <= 330+170:
                if 500 <= y <= 500+60:
                    pygame.mixer.music.stop()
                    self.scene.set_selecta_level(1)
            if 550 <= x <= 550+170:
                if 500 <= y <= 500+60:
                    pygame.mixer.music.stop()
                    self.scene.set_selecta_level(1)

        if self.if_win:
            if 110 <= x <= 110+170:
                if 500 <= y <= 500+60:
                    pygame.mixer.music.stop()
                    self.scene.set_main_scene()
            if 330 <= x <= 330+170:
                if 500 <= y <= 500+60:
                    pygame.mixer.music.stop()
                    self.scene.set_selecta_level(1)
            if 550 <= x <= 550+170:
                if 500 <= y <= 500+60:
                    pygame.mixer.music.stop()
                    self.scene.set_selecta_level(1)

    def check_moues_click_ys(self, x, y):
        if self.player_poss == 0:
            if 100 <= x <= 100 + self.ys_S_pos.width:
                if 472 <= y <= 472 + self.ys_S_pos.height:
                    self.player_poss = 1
                    self.if_ys_show[0] = False
                    self.score += 1
        elif self.player_poss == 1:
            if 100 <= x <= 100 + self.ys_N2_pos.width:
                if 300 <= y <= 300 + self.ys_N2_pos.height:
                    self.if_fail = True
            if 160 <= x <= 160 + self.ys_O2_pos.width:
                if 395 <= y <= 395 + self.ys_O2_pos.height:
                    self.player_poss = 2
                    self.if_ys_show[2] = False
                    self.score += 1
        elif self.player_poss == 2:
            if 91 <= x <= 91 + self.ys_nH2SO4_pos.width:
                if 170 <= y <= 170 + self.ys_nH2SO4_pos.height:
                    self.if_fail = True
            if 402 <= x <= 402 + self.ys_O2_pos.width:
                if 400 <= y <= 400 + self.ys_O2_pos.height:
                    self.player_poss = 4
                    self.if_ys_show[3] = False
                    self.score += 1
            if 407 <= x <= 407 + self.ys_H2O_pos.width:
                if 365 <= y <= 365 + self.ys_H2O_pos.height:
                    self.player_poss = 7
                    self.if_ys_show[8] = False
                    self.score += 1
            if 260 <= x <= 260 + self.ys_NaOH_pos.width:
                if 505 <= y <= 505 + self.ys_NaOH_pos.height:
                    self.player_poss = 3
                    self.if_ys_show[6] = False
                    self.score += 1
        elif self.player_poss == 3:
            if 402 <= x <= 402 + self.ys_O2_pos.width:
                if 400 <= y <= 400 + self.ys_O2_pos.height:
                    self.if_fail = True
            if 590 <= x <= 590 + self.ys_O2_pos.width:
                if 459 <= y <= 459 + self.ys_O2_pos.height:
                    self.if_fail = True
        elif self.player_poss == 4:
            if 590 <= x <= 590 + self.ys_KOH_pos.width:
                if 459 <= y <= 459 + self.ys_KOH_pos.height:
                    self.player_poss = 6
                    self.if_ys_show[9] = False
                    self.if_win = True
                    self.score += 1
        elif self.player_poss == 7:
            if 395 <= x <= 395 + self.ys_AgCl_pos.width:
                if 216 <= y <= 216 + self.ys_AgCl_pos.height:
                    self.if_fail = True
            if 525 <= x <= 525 + self.ys_CO2_pos.width:
                if 270 <= y <= 270 + self.ys_CO2_pos.height:
                    self.if_fail = True
            if 663 <= x <= 663 + self.ys_O2_pos.width:
                if 302 <= y <= 302 + self.ys_O2_pos.height:
                    self.player_poss = 8
                    self.if_ys_show[4] = False
                    self.score += 1
        elif self.player_poss == 8:
            if 610 <= x <= 610 + self.ys_O2_pos.width:
                if 219 <= y <= 219 + self.ys_O2_pos.height:
                    self.player_poss = 9
                    self.if_ys_show[12] = False
                    self.score += 1
        elif self.player_poss == 9:
            if 282 <= x <= 282 + self.ys_O2_pos.width:
                if 160 <= y <= 160 + self.ys_O2_pos.height:
                    self.if_fail = True
            if 585 <= x <= 585 + self.ys_BaCl2_pos.width:
                if 121 <= y <= 121 + self.ys_BaCl2_pos.height:
                    self.player_poss = 11
                    self.if_ys_show[13] = False
                    self.if_win = True
                    self.score += 1

    def show_ys(self):
        if self.if_ys_show[0]:
            self.screen.blit(self.ys_S, (100, 472))
        if self.if_ys_show[1]:
            self.screen.blit(self.ys_N2, (100, 300))
        if self.if_ys_show[2]:
            self.screen.blit(self.ys_O2, (160, 395))
        if self.if_ys_show[3]:
            self.screen.blit(self.ys_O2, (402, 400))
        if self.if_ys_show[4]:
            self.screen.blit(self.ys_O2, (663, 302))
        if self.if_ys_show[5]:
            self.screen.blit(self.ys_O2, (282, 160))
        if self.if_ys_show[6]:
            self.screen.blit(self.ys_NaOH, (260, 505))
        if self.if_ys_show[7]:
            self.screen.blit(self.ys_nH2SO4, (91, 170))
        if self.if_ys_show[8]:
            self.screen.blit(self.ys_H2O, (407, 365))
        if self.if_ys_show[9]:
            self.screen.blit(self.ys_KOH, (590, 459))
        if self.if_ys_show[10]:
            self.screen.blit(self.ys_AgCl, (395, 216))
        if self.if_ys_show[11]:
            self.screen.blit(self.ys_CO2, (525, 270))
        if self.if_ys_show[12]:
            self.screen.blit(self.ys_CUO, (610, 219))
        if self.if_ys_show[13]:
            self.screen.blit(self.ys_BaCl2, (585, 121))
