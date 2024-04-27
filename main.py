# coding=gbk
# -*- coding: utf-8 -*-
import pygame
import time
import sys
import os

from BalloonsTwoPlayer import BalloonsTwoPlayer
from BalloonsOnePlayer import BalloonsOnePlayer
from QAOnePlayer import QAOnePlayer
from QATwoPlayer import QATwoPlayer
from tao import Tao
from mimi import Mimi
from ChemistryGame import ChemistryGame
from maze import Maze

pygame.init()
pygame.mixer.init()


# �ڡ���ѧ��½��������Ԫ�غ�����Ԫ��֮���ì���������ң��ݱ��һ�����ҵ�Ԫ��֮ս����������ʱ�����Լ���ս������ʧ�����δ֪�������С�ͻȻ������Ԫ��������������һ�����š�̼��ս�۵�С����������һ����������˷ǳ��м���������������һ���ܽ���Ԫ�ء���

class SceneSwitching:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('chemical reaction')
        self.clock = pygame.time.Clock()

        self.game_run = True
        self.screen = pygame.display.set_mode((800, 600))

        self.scenes = MainScene(self, self.clock)

    def run_game(self):
        self.scenes.run_game()

    def set_main_scene(self):
        self.scenes = MainScene(self, self.clock, True)
        self.scenes.run_game()

    def set_selecta_level(self, player_num):
        self.scenes = SelectALevel(self, self.clock, player_num)
        self.scenes.run_game()


class MainScene:
    def __init__(self, scene, clock, if_prologue=True):
        self.screen = scene.screen
        self.clock = clock
        pygame.display.set_caption('Chemical Continent')
        self.scene = scene
        self.font = pygame.font.Font("./Fonts/simsun.ttc", 36)
        self.text = ('�ڡ���ѧ��½��������Ԫ�غ�����Ԫ��֮���ì\n���������ң��ݱ��һ�����ҵ�Ԫ��֮ս������\n����ʱ�����Լ���ս������ʧ�����δ֪����\n���С�ͻȻ��'
                     '����Ԫ��������������һ������\n��̼��ս�۵�С����������һ����������˷ǳ�\n�м���������������һ���ܽ���Ԫ�ء���!')
        self.text_lines = self.text.split('\n')
        self.text_surfaces = [self.font.render(line, True, (0, 0, 0)) for line in self.text_lines]
        # ���ô��ֻ�Ч���Ĳ���
        self.typing_speed = 30  # �����ٶȣ�ÿ��������
        self.time_per_char = 60 / self.typing_speed  # ����ÿ���ַ�����ʾʱ��
        self.elapsed_time = 0
        self.current_line = 0
        self.current_char = 0
        self.if_prologue = if_prologue

    def run_game(self):
        """������Ϸ������"""

        while self.scene.game_run:
            self._check_event()
            self.load_img()
            if not self.if_prologue:
                self.elapsed_time += self.clock.tick(60)
                if self.elapsed_time >= self.time_per_char:
                    self.elapsed_time = 0
                    self.current_char += 1
                if self.current_line < len(self.text_lines):
                    if self.current_char > len(self.text_lines[self.current_line]):
                        self.current_char = 0
                        self.current_line += 1
                if self.current_line >= len(self.text_lines):
                    time.sleep(3)
                    self.if_prologue = True

            self.update_screen()
            pygame.display.update()
            self.clock.tick(60)

    def _check_event(self):
        """����¼�"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 430 <= mouse_x <= 430 + 341:
                    if 380 <= mouse_y <= 380 + 124:
                        self.scene.scenes = SelectALevel(self.scene, self.clock, 2)
                        self.scene.scenes.run_game()
                elif 50 <= mouse_x <= 50 + 341:
                    if 380 <= mouse_y <= 380 + 124:
                        self.scene.scenes = SelectALevel(self.scene, self.clock, 1)
                        self.scene.scenes.run_game()

    def update_screen(self):
        self.screen.fill((135, 180, 255))
        self.screen.blit(self.bg, (0, 0))
        if self.if_prologue:
            self.screen.blit(self.start_game_one_player, (50, 380))
            self.screen.blit(self.start_game_two_player, (430, 380))
            self.screen.blit(self.title, (20, 15))
        if not self.if_prologue:
            for i, line_surface in enumerate(self.text_surfaces):
                if i < self.current_line:
                    self.screen.blit(line_surface, (5, 100 + i * 40))
                elif i == self.current_line:
                    current_line_text = self.text_lines[i][:self.current_char]
                    current_line_surface = self.font.render(current_line_text, True, (0, 0, 0))
                    self.screen.blit(current_line_surface, (5, 100 + i * 40))

    def load_img(self):
        self.start_game_two_player = pygame.image.load('image/start_game_two_player2.png')
        self.start_game_one_player = pygame.image.load('image/start_game_one_player2.png')  # 341 * 121
        self.bg_tmp = pygame.image.load('image/bg_skies.png')
        self.bg = pygame.transform.scale(self.bg_tmp, (800, 600))
        self.title_tmp = pygame.image.load('image/title.png')
        self.title = pygame.transform.scale(self.title_tmp, (760, 300))


class SelectALevel:
    def __init__(self, scene, clock, player_num):
        self.screen = scene.screen
        self.clock = clock
        pygame.display.set_caption('Chemical Continent')
        self.scene = scene
        self.font = pygame.font.Font("./Fonts/simsun.ttc", 30)
        self.player_num = player_num

    def run_game(self):
        while self.scene.game_run:
            self._check_event()
            self.load_img()

            self.update_screen()
            pygame.display.update()
            self.clock.tick(60)

    def update_screen(self):
        self.screen.fill((135, 180, 255))
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.return_, (10, 10))
        self.screen.blit(self.mode_img, (200, 10))
        self.create_level()

    def load_img(self):
        self.bg_tmp = pygame.image.load('image/bg_skies.png')
        self.bg = pygame.transform.scale(self.bg_tmp, (800, 600))
        self.return_tmp = pygame.image.load("./image/return.png")
        self.return_ = pygame.transform.scale(self.return_tmp, (80, 80))
        if self.player_num == 1:
            self.mode_img_tmp = pygame.image.load("./image/one_player.png")
        elif self.player_num == 2:
            self.mode_img_tmp = pygame.image.load("./image/two_player.png")
        self.mode_img = pygame.transform.scale(self.mode_img_tmp, (400, 80))

    def _check_event(self):
        """����¼�"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_mouse(mouse_x, mouse_y)

    def check_mouse(self, mouse_x, mouse_y):
        if self.player_num == 1:
            # ����ؿ���ť��������귶Χ
            level_positions = [
                (16, 100, 196, 220),  # ��1�ذ�ť����
                (212, 100, 392, 220),  # ��2�ذ�ť����
                (408, 100, 588, 220),  # ��3�ذ�ť����
                (604, 100, 784, 220),  # ��4�ذ�ť����
                (16, 240, 196, 390),  # ��5�ذ�ť����
                (212, 240, 392, 390)
            ]

            # ��������λ���Ƿ��ڹؿ���ť������
            for index, (x1, y1, x2, y2) in enumerate(level_positions, start=1):
                if x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2:
                    if index == 1:
                        self.scene.scenes = Tao(self.clock, self.scene)
                        self.scene.run_game()
                    if index == 2:
                        self.scene.scenes = Mimi(self.clock, self.scene)
                        self.scene.run_game()
                    if index == 3:
                        self.scene.scenes = BalloonsOnePlayer(self.clock, self.scene, 2)
                        self.scene.run_game()
                    if index == 4:
                        self.scene.scenes = ChemistryGame(self.clock, self.scene)
                        self.scene.run_game()
                    if index == 5:
                        self.scene.scenes = QAOnePlayer(self.clock, self.scene)
                        self.scene.run_game()
                    if index == 6:
                        self.scene.scenes = Maze(self.clock, self.scene)
                        self.scene.run_game()

        elif self.player_num == 2:
            level_positions = [
                (16, 100, 196, 220),
                (212, 100, 392, 220)
            ]

            for index, (x1, y1, x2, y2) in enumerate(level_positions, start=1):
                if x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2:
                    if index == 1:
                        self.scene.scenes = BalloonsTwoPlayer(self.clock, self.scene, 2)
                        self.scene.run_game()
                    if index == 2:
                        self.scene.scenes = QATwoPlayer(self.clock, self.scene)
                        self.scene.run_game()

        # ����Ƿ������ذ�ť����
        if 10 <= mouse_x <= 90 and 10 <= mouse_y <= 90:
            self.scene.set_main_scene()

    def create_level(self):
        if self.player_num == 1:
            # ���ɾ��ο�����Ͻ� x �����б� x
            x_positions = [16, 212, 408, 604, 16, 212]  # ���һ��λ����Ϊ16

            # ���ɾ��ο�����Ͻ� y �����б� y
            y_positions = [100, 100, 100, 100, 240, 240]  # ������ͼƬ��yλ����Ϊ240

            # ���عؿ���ťͼƬ
            level_images = [
                pygame.image.load(os.path.join("image", f"level{i}.png")) for i in range(1, 7)
            ]

            # ���ƹؿ���ť
            for x_pos, y_pos, image in zip(x_positions, y_positions, level_images):
                self.screen.blit(image, (x_pos, y_pos))
        elif self.player_num == 2:
            self.l1 = pygame.image.load("./image/2_1.png")
            self.l2 = pygame.image.load("./image/2_2.png")
            self.screen.blit(self.l1, (16, 100))
            self.screen.blit(self.l2, (212, 100))


if __name__ == '__main__':
    cr = SceneSwitching()
    cr.run_game()
