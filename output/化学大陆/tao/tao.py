# -*- coding: utf-8 -*-

import pygame
import random
import sys
import os


class ChemicalSymbol(pygame.sprite.Sprite):
    def __init__(self, image_path, initial_position, id):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=initial_position)
        self.dragging = False
        self.offset = (0, 0)
        self.id = id
        self.if_stop = True

    def update(self):
        if self.if_stop:
            if self.dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.rect.center = (mouse_x - self.offset[0], mouse_y - self.offset[1])

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Table(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)


class Tao:
    def __init__(self, clock, scene):
        """初始化 Tao 类"""
        self.screen = scene.screen
        self.scene = scene
        pygame.display.set_caption("元素的秘密")
        self.clock = clock
        self.if_game_run = True
        self.if_wim = False

        # 加载背景图像和表格图像
        self.background = pygame.image.load("./image/bg_skies.png").convert()
        self.background = pygame.transform.scale(self.background, (800, 600))
        self.table = Table("./image/biao.png", (0, 200))  # 创建表格对象
        self.win_tmp = pygame.image.load('image/win2.png')
        self.win = pygame.transform.scale(self.win_tmp, (250, 250))
        self.return_main_scene_tmp = pygame.image.load('image/return_main_scene.png')
        self.return_main_scene = pygame.transform.rotozoom(self.return_main_scene_tmp, 0, 0.5)
        self.return_tmp = pygame.image.load("./image/return.png")
        self.return_ = pygame.transform.scale(self.return_tmp, (80, 80))

        # 创建化学符号对象列表
        self.chemical_symbols = []
        self.symbol_positions = [(100, 50), (200, 50), (300, 50), (400, 50), (500, 50),
                                 (100, 150), (200, 150), (300, 150), (400, 150), (500, 150), (600, 150)]
        self.symbol_positions2 = [
            (97, 200), (715, 200), (360, 260),(450, 260), (535, 260), (100, 330),
            (180, 330), (360, 330), (535, 330), (625, 330), (715, 330),
        ]
        self.symbol_positions3 = [
            (180, 260), (800, 260), (450, 360), (530, 330), (625, 325), (180, 390),
            (270, 390), (450, 390), (625, 390), (715, 390), (800, 390),
        ]

        tmp = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        random.shuffle(tmp)
        for index, i in enumerate(tmp):
            path = os.path.abspath('.')
            symbol_image_path = fr"{path}\tao\image\CC\{i}.png"  # 48*56
            self.symbol_position = self.symbol_positions[index]  # 使用索引获取对应位置
            chemical_symbol = ChemicalSymbol(symbol_image_path, self.symbol_position, i)
            self.chemical_symbols.append(chemical_symbol)

        # 初始化得分
        self.score = 0

        pygame.mixer.music.load('./Musics/musics.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    def run_game(self):
        while self.if_game_run:
            self.set_show_score()
            self._check_event()
            for symbol in self.chemical_symbols:
                symbol.update()  # 更新化学符号对象状态
            self.update_screen()
            pygame.display.update()
            self.clock.tick(60)

    def update_screen(self):
        self.screen.blit(self.background, (0, 0))  # 绘制背景图像
        self.screen.blit(self.table.image, self.table.rect)  # 绘制表格图像
        self.screen.blit(self.score_text, (640, 20))
        self.screen.blit(self.return_, (10, 10))
        for symbol in self.chemical_symbols:
            symbol.draw(self.screen)  # 绘制化学符号
        if self.if_wim:
            self.screen.blit(self.win, (275, 150))
            self.screen.blit(self.return_main_scene, (330, 500))

    def _check_event(self):
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 10 <= x <= 90 and 10 <= y <= 90:
                    self.scene.set_main_scene()
            if event.type == pygame.MOUSEBUTTONDOWN and not self.if_wim:
                if event.button == 1:  # 左键按下
                    for symbol in self.chemical_symbols:
                        if symbol.rect.collidepoint(event.pos):
                            symbol.dragging = True
                            # 计算鼠标相对于符号中心的偏移量
                            symbol.offset = (event.pos[0] - symbol.rect.centerx,
                                             event.pos[1] - symbol.rect.centery)
            elif event.type == pygame.MOUSEBUTTONUP and not self.if_wim:
                a=0
                # mouse_x, mouse_y = pygame.mouse.get_pos()
                # print(mouse_x, mouse_y)
                if event.button == 1:  # 左键释放
                    for symbol in self.chemical_symbols:

                        if symbol.dragging:
                            symbol.dragging = False
                            # 检测化学符号是否与表格发生碰撞
                            if symbol.rect.colliderect(self.table.rect):
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                if self.symbol_positions2[symbol.id-1][0] <= mouse_x <= self.symbol_positions3[symbol.id-1][0]:
                                    if self.symbol_positions2[symbol.id-1][1] <= mouse_y <= \
                                            self.symbol_positions3[symbol.id-1][1]:
                                        if symbol.if_stop:
                                            symbol.if_stop = False
                                            self.score += 1
                                else:
                                    self.score -= 1
                            else:
                                pass
                            break  # 只处理一个化学符号的释放事件
                        if not symbol.if_stop:
                            a += 1
                            if a == 10:
                                self.if_wim = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 330 <= x <= 500:
                    if 500 <= y <= 560:
                        pygame.mixer.music.stop()
                        self.scene.set_main_scene()

    def set_show_score(self):
        self.score_text_tmp = " 得分：" + str(self.score)
        self.font = pygame.font.Font("./Fonts/simsun.ttc", 30)
        self.score_text = self.font.render(self.score_text_tmp, True, (0, 0, 0))
