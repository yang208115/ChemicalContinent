# -*- coding: utf-8 -*-
import pygame
import time
import sys
import os

from maze import Maze

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
                # if 430 <= mouse_x <= 430 + 341:
                #     if 380 <= mouse_y <= 380 + 124:
                #         self.scene.scenes = SelectALevel(self.scene, self.clock, 2)
                #         self.scene.scenes.run_game()
                if 50 <= mouse_x <= 50 + 341:
                    if 380 <= mouse_y <= 380 + 124:
                        self.scene.scenes = Maze(self.clock, self.scene)
                        self.scene.scenes.run_game()

    def update_screen(self):
        self.screen.fill((135, 180, 255))
        self.screen.blit(self.bg, (0, 0))
        if self.if_prologue:
            self.screen.blit(self.start_game_one_player, (50, 380))
            # self.screen.blit(self.start_game_two_player, (430, 380))
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
        # self.start_game_two_player = pygame.image.load('image/start_game_two_player2.png')
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
        """检查事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.check_mouse(mouse_x, mouse_y)

    def check_mouse(self, mouse_x, mouse_y):
        # 定义矩形框布局所需的初始参数
        initial_x = 16  # 矩形框左上角 x 坐标的初始值
        width = 180  # 矩形框的宽度
        gap_x = 16  # 矩形框之间的水平间隔
        initial_y = 100  # 矩形框左上角 y 坐标的初始值
        height = 120  # 矩形框的高度
        gap_y = 50  # 矩形框之间的垂直间隔
        # 定义 x 列表，表示矩形框的左上角 x 坐标
        x = [
            initial_x,
            initial_x + width + gap_x,
            initial_x + width + gap_x + width + gap_x,
            initial_x + width + gap_x + width + gap_x + width + gap_x
        ]

        # 定义 x2 列表，表示矩形框的右下角 x 坐标
        x2 = [
            initial_x + width,
            initial_x + width + gap_x + width,
            initial_x + width + gap_x + width + gap_x + width,
            initial_x + width + gap_x + width + gap_x + width + gap_x + width
        ]

        # 定义 y 列表，表示矩形框的左上角 y 坐标
        y = [
            initial_y,
            # initial_y + height + gap_y,
            # initial_y + height + gap_y + height + gap_y
        ]

        # 定义 y2 列表，表示矩形框的右下角 y 坐标
        y2 = [
            initial_y + height,
            # initial_y + height + gap_y + height,
            # initial_y + height + gap_y + height + gap_y + height
        ]

        a = 1
        for y3, y4 in zip(y, y2):
            for x3, x4 in zip(x, x2):
                if x3 <= mouse_x <= x4:
                    if y3 <= mouse_y <= y4:
                        if os.path.exists(f'image/{a}'):
                            """关卡选择"""
                            pass
                        else:
                            print(f"关卡暂未开放,{a}")
                a += 1
        if 10 <= mouse_x <= 90:
            if 10 <= mouse_y <= 90:
                self.scene.set_main_scene()

    def create_level(self):
        # 定义常量和间隔
        initial_x = 16  # 初始 x 坐标
        width = 180  # 矩形框宽度
        gap_x = 16  # 水平间隔

        initial_y = 100  # 初始 y 坐标
        height = 120  # 矩形框高度
        gap_y = 50  # 垂直间隔
        # 生成矩形框的左上角 x 坐标列表 x
        x = []
        for i in range(4):  # 循环生成四个矩形框的坐标
            if i == 0:
                x.append(initial_x)  # 第一个矩形框的坐标
            else:
                x.append(x[i - 1] + width + gap_x)  # 后续矩形框的坐标

        # 生成矩形框的左上角 y 坐标列表 y
        y = []
        for j in range(1):  # 循环生成三个矩形框的坐标
            if j == 0:
                y.append(initial_y)  # 第一个矩形框的坐标
            else:
                y.append(y[j - 1] + height + gap_y)  # 后续矩形框的坐标

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
