# -*- coding: utf-8 -*-
from BalloonsTwoPlayer import BalloonsTwoPlayer
from BalloonsOnePlayer import BalloonsOnePlayer
import pygame
import time
import sys
import os

pygame.init()
pygame.mixer.init()


# 在“化学大陆”，金属元素和其他元素之间的矛盾愈演愈烈，演变成一场激烈的元素之战。主角醒来时发现自己身处战场，迷失在这个未知的世界中。突然，金属元素向他攻击，而一个身着“碳”战袍的小兵救了主角一命。主角因此非常感激，他决定和他们一起打败金属元素……

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
        self.text = ('在“化学大陆”，金属元素和其他元素之间的矛\n盾愈演愈烈，演变成一场激烈的元素之战。主角\n醒来时发现自己身处战场，迷失在这个未知的世\n界中。突然，'
                     '金属元素向他攻击，而一个身着\n“碳”战袍的小兵救了主角一命。主角因此非常\n感激，他决定和他们一起打败金属元素……!')
        self.text_lines = self.text.split('\n')
        self.text_surfaces = [self.font.render(line, True, (0, 0, 0)) for line in self.text_lines]
        # 设置打字机效果的参数
        self.typing_speed = 30  # 打字速度，每分钟字数
        self.time_per_char = 60 / self.typing_speed  # 计算每个字符的显示时间
        self.elapsed_time = 0
        self.current_line = 0
        self.current_char = 0
        self.if_prologue = if_prologue

    def run_game(self):
        """定义游戏主程序"""

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
        """检查事件"""
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
        self.create_level()

    def load_img(self):
        self.bg_tmp = pygame.image.load('image/bg_skies.png')
        self.bg = pygame.transform.scale(self.bg_tmp, (800, 600))

    def _check_event(self):
        """检查事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_mouse(mouse_x, mouse_y)

    def check_mouse(self, mouse_x, mouse_y):
        x = [16, 16 + 180 + 16, 16 + 180 + 16 + 180 + 16, 16 + 180 + 16 + 180 + 16 + 180 + 16]
        x2 = [16 + 180, 16 + 180 + 16 + 180, 16 + 180 + 16 + 180 + 16 + 180, 16 + 180 + 16 + 180 + 16 + 180 + 16 + 180]
        y = [50, 50 + 120 + 50, 50 + 120 + 50 + 120 + 50]
        y2 = [50 + 120, 50 + 120 + 50 + 120, 50 + 120 + 50 + 120 + 50 + 120]
        a = 1
        for y3, y4 in zip(y, y2):
            for x3, x4 in zip(x, x2):
                if x3 <= mouse_x <= x4:
                    if y3 <= mouse_y <= y4:
                        if os.path.exists(f'image/{a}'):
                            if self.player_num == 1:
                                self.scene.scene = BalloonsOnePlayer(self.clock, self.scene, a)
                                self.scene.scene.run_game()
                            if self.player_num == 2:
                                self.scene.scene = BalloonsTwoPlayer(self.clock, self.scene, a)
                                self.scene.scene.run_game()
                        else:
                            print("关卡暂未开放")
                a += 1

    def create_level(self):
        x = [16, 16 + 180 + 16, 16 + 180 + 16 + 180 + 16, 16 + 180 + 16 + 180 + 16 + 180 + 16]
        y = [50, 50 + 120 + 50, 50 + 120 + 50 + 120 + 50]
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
