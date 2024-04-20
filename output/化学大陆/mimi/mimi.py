# coding=gbk

import pygame
import sys
import random


# 创建元素符号类
class Element(pygame.sprite.Sprite):
    def __init__(self, symbol, category, position):
        super().__init__()
        self.symbol = symbol
        self.category = category
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))  # 元素符号用红色表示
        self.font = pygame.font.Font("./Fonts/simsun.ttc", 30)
        text = self.font.render(symbol, True, (255, 255, 255))
        self.image.blit(text, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.original_position = position  # 记录元素符号的原始位置
        self.dragging = False
        self.score = 0
        self.if_ok = False

    def update(self):
        # 如果元素符号正在被拖拽，则更新位置为鼠标位置
        if self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.topleft = (mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1])

    def reset_position(self):
        self.rect.topleft = self.original_position


class Mimi:
    def __init__(self, clock, scene):
        """初始化Balloons类"""
        self.screen = scene.screen
        self.scene = scene
        pygame.display.set_caption("元素的秘密")
        self.clock = clock
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.score = 0
        self.if_wim = False

        self.elements_data = [
            ("H", "非金属元素"),
            ("He", "稀有气体元素"),
            ("Li", "金属元素"),
            ("Be", "金属元素"),
            ("C", "非金属元素"),
            ("O", "非金属元素"),
            ("Na", "金属元素"),
            ("Mg", "金属元素"),
            ("Ne", "稀有气体元素"),
            ("K", "金属元素"),
            ("Ar", "稀有气体元素"),
            ("Hg", "金属元素"),
            ("N", "非金属元素"),
            ("Br", "非金属元素"),
            ("Ca", "金属元素"),
            ("Si", "非金属元素"),
            # 继续添加更多元素符号...
        ]

        self.pos = [
            (100, 100), (200, 100), (300, 100), (400, 100),
            (100, 200), (200, 200), (300, 200), (400, 200),
            (100, 300), (200, 300), (300, 300), (400, 300),
            (100, 400), (200, 400), (300, 400), (400, 400),
        ]
        self.categories = {
            "非金属元素": pygame.Rect(50, 500, 200, 50),
            "金属元素": pygame.Rect(300, 500, 200, 50),
            "稀有气体元素": pygame.Rect(550, 500, 200, 50)
        }
        random.shuffle(self.pos)
        self.elements = [Element(data[0], data[1], self.pos[i]) for i, data in enumerate(self.elements_data)]
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
        self.return_main_scene_tmp = pygame.image.load('image/return_main_scene.png')
        self.return_main_scene = pygame.transform.rotozoom(self.return_main_scene_tmp, 0, 0.5)
        self.return_tmp = pygame.image.load("./image/return.png")
        self.return_ = pygame.transform.scale(self.return_tmp, (80, 80))

    def run_game(self):
        self.load_img()

        while self.if_game_run:
            # 处理事件
            self.screen.fill((135, 180, 255))
            self.screen.blit(self.background, (0, 0))
            for event in pygame.event.get():
                x, y = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    self.if_game_run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if 10 <= x <= 90 and 10 <= y <= 90:
                        self.scene.set_main_scene()
                if event.type == pygame.MOUSEBUTTONDOWN and self.if_wim:
                    x, y = pygame.mouse.get_pos()
                    if 330 <= x <= 500:
                        if 500 <= y <= 560:
                            pygame.mixer.music.stop()
                            self.scene.set_main_scene()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # 检查是否点击了元素符号
                    for element in self.elements:
                        if element.rect.collidepoint(event.pos):
                            element.dragging = True
                            # 计算鼠标点击位置和元素符号左上角的偏移量
                            element.offset = (event.pos[0] - element.rect.left, event.pos[1] - element.rect.top)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # 检查是否释放了元素符号
                    for element in self.elements:
                        if element.dragging:
                            element.dragging = False
                            # 检查是否拖拽到正确位置
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

            # 更新元素符号位置
            for element in self.elements:
                element.update()
                self.screen.blit(element.image, element.rect.topleft)

            if len(self.elements2) == 16 and not self.if_wim:
                self.if_wim = True

            # 绘制分类框
            for category, rect in self.categories.items():
                pygame.draw.rect(self.screen, self.GREEN, rect, 2)

            # 显示得分
            font = pygame.font.Font("./Fonts/simsun.ttc", 30)
            score_text = font.render(f"得分: {self.score}", True, (0, 0, 0))
            text = font.render(" 非金属元素        金属元素       稀有气体元素", True, (255, 255, 255))
            self.screen.blit(score_text, (200, 20))
            self.screen.blit(text, (50, 510))
            self.screen.blit(self.return_, (10, 10))
            if self.if_wim:
                self.screen.blit(self.win, (275, 150))
                self.screen.blit(self.return_main_scene, (330, 500))

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()
