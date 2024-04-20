# coding=gbk
# -*- coding: utf-8 -*-
import pygame
import time
import sys
import os

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
        pygame.display.set_caption('chemical reaction')
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
        pygame.display.set_caption('chemical reaction')
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
        # ������ο򲼾�����ĳ�ʼ����
        initial_x = 16  # ���ο����Ͻ� x ����ĳ�ʼֵ
        width = 180  # ���ο�Ŀ��
        gap_x = 16  # ���ο�֮���ˮƽ���
        initial_y = 100  # ���ο����Ͻ� y ����ĳ�ʼֵ
        height = 120  # ���ο�ĸ߶�
        gap_y = 50  # ���ο�֮��Ĵ�ֱ���
        # ���� x �б���ʾ���ο�����Ͻ� x ����
        x = [
            initial_x,
            initial_x + width + gap_x,
            initial_x + width + gap_x + width + gap_x,
            initial_x + width + gap_x + width + gap_x + width + gap_x
        ]

        # ���� x2 �б���ʾ���ο�����½� x ����
        x2 = [
            initial_x + width,
            initial_x + width + gap_x + width,
            initial_x + width + gap_x + width + gap_x + width,
            initial_x + width + gap_x + width + gap_x + width + gap_x + width
        ]

        # ���� y �б���ʾ���ο�����Ͻ� y ����
        y = [
            initial_y,
            initial_y + height + gap_y,
            initial_y + height + gap_y + height + gap_y
        ]

        # ���� y2 �б���ʾ���ο�����½� y ����
        y2 = [
            initial_y + height,
            initial_y + height + gap_y + height,
            initial_y + height + gap_y + height + gap_y + height
        ]

        a = 1
        for y3, y4 in zip(y, y2):
            for x3, x4 in zip(x, x2):
                if x3 <= mouse_x <= x4:
                    if y3 <= mouse_y <= y4:
                        if os.path.exists(f'image/{a}'):
                            """�ؿ�ѡ��"""
                            pass
                        else:
                            print(f"�ؿ���δ����,{a}")
                a += 1
        if 10 <= mouse_x <=90:
            if 10 <= mouse_y <= 90:
                self.scene.set_main_scene()

    def create_level(self):
        # ���峣���ͼ��
        initial_x = 16  # ��ʼ x ����
        width = 180  # ���ο���
        gap_x = 16  # ˮƽ���

        initial_y = 100  # ��ʼ y ����
        height = 120  # ���ο�߶�
        gap_y = 50  # ��ֱ���
        # ���ɾ��ο�����Ͻ� x �����б� x
        x = []
        for i in range(4):  # ѭ�������ĸ����ο������
            if i == 0:
                x.append(initial_x)  # ��һ�����ο������
            else:
                x.append(x[i - 1] + width + gap_x)  # �������ο������

        # ���ɾ��ο�����Ͻ� y �����б� y
        y = []
        for j in range(3):  # ѭ�������������ο������
            if j == 0:
                y.append(initial_y)  # ��һ�����ο������
            else:
                y.append(y[j - 1] + height + gap_y)  # �������ο������

        a = 1
        for y2 in y:
            for x2 in x:
                pygame.draw.rect(self.screen, (255, 255, 0), (x2, y2, 180, 120))

        for y2 in y:
            for x2 in x:
                self.level_text_tmp = str(a)
                self.level_text = self.font.render(self.level_text_tmp, True, (0, 0, 0))
                self.screen.blit(self.level_text, (x2 + 80, y2 + 50))
                a += 1


if __name__ == '__main__':
    cr = SceneSwitching()
    cr.run_game()
