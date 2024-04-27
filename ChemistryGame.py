# coding=gbk
import sys
import pygame
import random
from QAOnePlayer import QAOnePlayer

pygame.init()

# 定义常见物质及其分类
substances = {
    "金属氧化物": ["Fe2O3", "Al2O3", "CuO", "ZnO", "BaO", "Fe3O4", "Cu2O"],
    "非金属氧化物": ["CO2", "SO2", "NO2", "P2O5", "CO"],
    "酸": ["H2SO4", "HCl", "HNO3", "H3PO4", "H2CO3"],
    "碱": ["NaOH", "KOH", "NH3·H2O", "Ca(OH)2", "Ba(OH)2"],
    "盐": ["NaCl", "K2CO3", "CaCl2", "MgCl2", "MgSO4"]
}

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 设置屏幕尺寸
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 设置字体
font = pygame.font.Font("./Fonts/simsun.ttc", 26)


class ChemistryGame:
    def __init__(self, clock, scene):
        self.screen = scene.screen
        pygame.display.set_caption('Chemistry Maze')
        self.clock = clock
        self.scene = scene
        self.categories = ["金属氧化物", "非金属氧化物", "酸", "碱", "盐"]
        self.current_category_index = 0
        self.score = 0
        self.buttons = []
        self.create_buttons()
        self.a = 0
        self.if_wim = False

        pygame.mixer.music.load('./Musics/musics.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    def create_buttons(self):
        self.buttons.clear()
        button_size = 100
        button_spacing = 20
        button_start_x = (SCREEN_WIDTH - 3 * (button_size + button_spacing)) // 2
        button_start_y = (SCREEN_HEIGHT - 3 * (button_size + button_spacing)) // 2

        # 随机选择当前类别
        current_category = self.categories[self.current_category_index]
        category_substances = substances[current_category]

        # 从当前类别中随机选择四个物质作为按钮的主要物质
        chosen_substances = random.sample(category_substances, 4)

        # 从其余的物质中随机选择四个作为剩余按钮的物质
        remaining_categories = [cat for cat in self.categories if cat != current_category]
        other_substances = [sub for cat in remaining_categories for sub in substances[cat]]
        extra_substances = random.sample(other_substances, 4)

        # 合并所有物质，确保总共有九个物质
        all_substances = chosen_substances + extra_substances
        random.shuffle(all_substances)

        for i in range(3):
            for j in range(3):
                x = button_start_x + j * (button_size + button_spacing)
                y = button_start_y + i * (button_size + button_spacing)

                if i == 1 and j == 1:
                    # 中间按钮，显示当前类别，不可点击
                    category_text = current_category
                    button = Button(x, y, button_size, button_size, category_text, clickable=False)
                else:
                    # 其他按钮，随机选择物质
                    if all_substances:
                        substance_text = all_substances.pop(0)
                    else:
                        substance_text = ""  # 处理如果物质列表为空的情况

                    button = Button(x, y, button_size, button_size, substance_text)

                self.buttons.append(button)

    def run_game(self):
        self.load_img()

        while True:
            self._check_events()
            self.update_screen()
            pygame.display.update()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    x, y = pygame.mouse.get_pos()
                    self.check_mouse_click(pos)
                    self.check_mouse(x, y)

    def check_mouse(self, x, y):
        if 10 <= x <= 90 and 60 <= y <= 140:
            pygame.mixer.music.stop()
            self.scene.set_main_scene()
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
                self.scene.scenes = QAOnePlayer(self.clock, self.scene)
                self.scene.run_game()

    def check_mouse_click(self, pos):
        try:
            for button in self.buttons:
                if button.rect.collidepoint(pos) and not button.clicked and button.clickable:
                    button.clicked = True

                    if button.text in substances[self.categories[self.current_category_index]]:
                        button.color = GREEN
                        self.score += 1
                    else:
                        button.color = RED
                        self.score -= 1

                    button.clickable = False
        except IndexError:
            self.if_wim = True

        # 检查当前类别是否所有物质按钮都已点击
        if self.current_category_index < len(self.categories):
            category_buttons = [button for button in self.buttons if
                                button.text in substances[self.categories[self.current_category_index]]]
            if all(button.clicked for button in category_buttons):
                # 切换到下一个类别
                self.current_category_index += 1
                if self.current_category_index < len(self.categories):
                    self.create_buttons()

    def update_screen(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.bg, (0, 0))
        for button in self.buttons:
            button.draw(self.screen)
        self.screen.blit(self.return_, (10, 50))
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (20, 20))
        if self.if_wim:
            self.screen.blit(self.win, (275, 150))
            self.screen.blit(self.next_level, (550, 500))
            self.screen.blit(self.return_select_sLevel, (330, 500))
            self.screen.blit(self.return_main_scene, (110, 500))

    def load_img(self):
        self.return_tmp = pygame.image.load("./image/return.png")
        self.return_ = pygame.transform.scale(self.return_tmp, (80, 80))
        self.win_tmp = pygame.image.load('image/win2.png')
        self.win = pygame.transform.scale(self.win_tmp, (250, 250))
        self.bg_tmp = pygame.image.load('image/bg_skies.png')
        self.bg = pygame.transform.scale(self.bg_tmp, (800, 600))
        self.next_level_tmp = pygame.image.load('image/next_level.png')
        self.next_level = pygame.transform.rotozoom(self.next_level_tmp, 0, 0.5)
        self.return_main_scene_tmp = pygame.image.load('image/return_main_scene.png')
        self.return_main_scene = pygame.transform.rotozoom(self.return_main_scene_tmp, 0, 0.5)
        self.return_select_sLevel_tmp = pygame.image.load('image/return_select_aLevel.png')
        self.return_select_sLevel = pygame.transform.rotozoom(self.return_select_sLevel_tmp, 0, 0.5)


class Button:
    def __init__(self, x, y, width, height, text, clickable=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.clicked = False
        self.color = GRAY
        self.clickable = clickable

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        win.blit(text_surface, text_rect)
