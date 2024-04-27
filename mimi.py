# coding=gbk

import pygame
import sys
import random
from BalloonsOnePlayer import BalloonsOnePlayer


# ����Ԫ�ط�����
class Element(pygame.sprite.Sprite):
    def __init__(self, symbol, category, position):
        super().__init__()
        self.symbol = symbol
        self.category = category
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))  # Ԫ�ط����ú�ɫ��ʾ
        self.font = pygame.font.Font("./Fonts/simsun.ttc", 30)
        text = self.font.render(symbol, True, (255, 255, 255))
        self.image.blit(text, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.original_position = position  # ��¼Ԫ�ط��ŵ�ԭʼλ��
        self.dragging = False
        self.score = 0
        self.if_ok = False

    def update(self):
        # ���Ԫ�ط������ڱ���ק�������λ��Ϊ���λ��
        if self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.topleft = (mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1])

    def reset_position(self):
        self.rect.topleft = self.original_position


class Mimi:
    def __init__(self, clock, scene):
        """��ʼ��Balloons��"""
        self.screen = scene.screen
        self.scene = scene
        pygame.display.set_caption("Ԫ�ص�����")
        self.clock = clock
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.score = 0
        self.if_wim = False
        self.font = pygame.font.Font("./Fonts/simsun.ttc", 30)

        self.elements_data = [
            ("H", "�ǽ���Ԫ��"),
            ("C", "�ǽ���Ԫ��"),
            ("O", "�ǽ���Ԫ��"),
            ("N", "�ǽ���Ԫ��"),
            ("P", "�ǽ���Ԫ��"),
            ("S", "�ǽ���Ԫ��"),
            ("Br", "�ǽ���Ԫ��"),
            ("Si", "�ǽ���Ԫ��"),
            ("He", "ϡ������Ԫ��"),
            ("Ar", "ϡ������Ԫ��"),
            ("Ne", "ϡ������Ԫ��"),
            ("K", "����Ԫ��"),
            ("U", "����Ԫ��"),
            ("Li", "����Ԫ��"),
            ("Be", "����Ԫ��"),
            ("Na", "����Ԫ��"),
            ("Mg", "����Ԫ��"),
            ("Hg", "����Ԫ��"),
            ("Ca", "����Ԫ��"),
            ("Fe", "����Ԫ��"),
            ("Mn", "����Ԫ��"),
            ("Cu", "����Ԫ��"),
            ("Ag", "����Ԫ��"),
            ("Au", "����Ԫ��"),
            ("Zn", "����Ԫ��"),
            ("Pt", "����Ԫ��"),
            ("Hg", "����Ԫ��"),
            ("Sn", "����Ԫ��"),
            ("Pb", "����Ԫ��"),
        ]

        self.pos = [
            (100, 100), (200, 100), (300, 100), (400, 100),
            (100, 200), (200, 200), (300, 200), (400, 200),
            (100, 300), (200, 300), (300, 300), (400, 300),
            (100, 400), (200, 400), (300, 400), (400, 400),
        ]
        self.categories = {
            "�ǽ���Ԫ��": pygame.Rect(50, 500, 200, 80),
            "����Ԫ��": pygame.Rect(300, 500, 200, 80),
            "ϡ������Ԫ��": pygame.Rect(550, 500, 200, 80)
        }
        random.shuffle(self.pos)
        selected_elements = random.sample(self.elements_data, 16)
        self.elements = [Element(data[0], data[1], self.pos[i]) for i, data in enumerate(selected_elements)]
        self.elements2 = []

        self.if_game_run = True

        pygame.mixer.music.load('./Musics/musics.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    def load_img(self):
        self.background_tmp = pygame.image.load("./image/bg_skies.png")
        self.background = pygame.transform.scale(self.background_tmp, (800, 600))
        self.win_tmp = pygame.image.load('image/win2.png')
        self.win = pygame.transform.scale(self.win_tmp, (250, 250))
        self.return_tmp = pygame.image.load("./image/return.png")
        self.return_ = pygame.transform.scale(self.return_tmp, (80, 80))
        self.next_level_tmp = pygame.image.load('image/next_level.png')
        self.next_level = pygame.transform.rotozoom(self.next_level_tmp, 0, 0.5)
        self.return_main_scene_tmp = pygame.image.load('image/return_main_scene.png')
        self.return_main_scene = pygame.transform.rotozoom(self.return_main_scene_tmp, 0, 0.5)
        self.return_select_sLevel_tmp = pygame.image.load('image/return_select_aLevel.png')
        self.return_select_sLevel = pygame.transform.rotozoom(self.return_select_sLevel_tmp, 0, 0.5)

    def run_game(self):
        self.load_img()

        while self.if_game_run:
            # �����¼�
            self.screen.fill((135, 180, 255))
            self.screen.blit(self.background, (0, 0))

            self._check_event()

            # ����Ԫ�ط���λ��
            for element in self.elements:
                element.update()
                self.screen.blit(element.image, element.rect.topleft)

            if len(self.elements2) == 16 and not self.if_wim:
                self.if_wim = True

            # ���Ʒ����
            # for category, rect in self.categories.items():
            #     pygame.draw.rect(self.screen, self.GREEN, rect, 2)

            self.update_screen()


        pygame.quit()
        sys.exit()

    def update_screen(self):
        for category, rect in self.categories.items():
            pygame.draw.rect(self.screen, self.GREEN, rect, 2)
        score_text = self.font.render(f"�÷�: {self.score}", True, (0, 0, 0))
        text = self.font.render("  �ǽ���Ԫ��       ����Ԫ��       ϡ������Ԫ��", True, (255, 255, 255))
        self.screen.blit(score_text, (200, 20))
        self.screen.blit(text, (50, 521))
        self.screen.blit(self.return_, (10, 10))
        if self.if_wim:
            self.screen.blit(self.win, (275, 150))
            self.screen.blit(self.next_level, (550, 500))
            self.screen.blit(self.return_select_sLevel, (330, 500))
            self.screen.blit(self.return_main_scene, (110, 500))

        pygame.display.flip()
        self.clock.tick(60)

    def _check_event(self):
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.if_game_run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 10 <= x <= 90 and 10 <= y <= 90:
                    pygame.mixer.music.stop()
                    self.scene.set_main_scene()
            if event.type == pygame.MOUSEBUTTONDOWN and self.if_wim:
                x, y = pygame.mouse.get_pos()
                if 110 <= x <= 110 + 170:
                    if 500 <= y <= 500 + 60:
                        pygame.mixer.music.stop()
                        self.scene.set_main_scene()
                if 330 <= x <= 330 + 170:
                    if 500 <= y <= 500 + 60:
                        pygame.mixer.music.stop()
                        self.scene.set_selecta_level(1)
                if 550 <= x <= 550 + 170:
                    if 500 <= y <= 500 + 60:
                        pygame.mixer.music.stop()
                        self.scene.scenes = BalloonsOnePlayer(self.clock, self.scene, 2)
                        self.scene.run_game()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # ����Ƿ�����Ԫ�ط���
                for element in self.elements:
                    if element.rect.collidepoint(event.pos):
                        element.dragging = True
                        # ���������λ�ú�Ԫ�ط������Ͻǵ�ƫ����
                        element.offset = (event.pos[0] - element.rect.left, event.pos[1] - element.rect.top)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # ����Ƿ��ͷ���Ԫ�ط���
                for element in self.elements:
                    if element.dragging:
                        element.dragging = False
                        # ����Ƿ���ק����ȷλ��
                        for category, rect in self.categories.items():
                            if rect.collidepoint(element.rect.center):
                                if element.category == category:
                                    self.elements2.append(element)
                                    self.elements.remove(element)
                                    self.score += 1
                                else:
                                    element.reset_position()
                                    self.score -= 1
                                break