# coding=gbk

import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 设置窗口尺寸和标题
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("元素哪里逃")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 加载背景图像
background = pygame.image.load("./image/bg_skies.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


# 创建元素符号类
class Element(pygame.sprite.Sprite):
    def __init__(self, symbol, category, position):
        super().__init__()
        self.symbol = symbol
        self.category = category
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)  # 元素符号用红色表示
        self.font = pygame.font.Font("./Fonts/simsun.ttc", 30)
        text = self.font.render(symbol, True, WHITE)
        self.image.blit(text, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.original_position = position  # 记录元素符号的原始位置
        self.dragging = False
        self.score = 0

    def update(self):
        # 如果元素符号正在被拖拽，则更新位置为鼠标位置
        if self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.topleft = (mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1])

    def reset_position(self):
        self.rect.topleft = self.original_position


# 创建元素符号列表
elements_data = [
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
    ("Sc", "金属元素"),
    ("N", "非金属元素"),
    ("Br", "非金属元素"),
    ("Ca", "金属元素"),
    ("Kr", "稀有气体元素"),
    # 继续添加更多元素符号...
]

pos = [
    (100, 100),(200, 100),(300, 100),(400, 100),
    (100, 200),(200, 200),(300, 200),(400, 200),
    (100, 300),(200, 300),(300, 300),(400, 300),
    (100, 400),(200, 400),(300, 400),(400, 400),
]
random.shuffle(pos)
elements = [Element(data[0], data[1], pos[i]) for i, data in enumerate(elements_data)]

# 创建分类框
categories = {
    "非金属元素": pygame.Rect(50, 500, 200, 50),
    "金属元素": pygame.Rect(300, 500, 200, 50),
    "稀有气体元素": pygame.Rect(550, 500, 200, 50)
}

# 游戏主循环
running = True
clock = pygame.time.Clock()
score = 0

while running:
    screen.blit(background, (0, 0))

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 检查是否点击了元素符号
            for element in elements:
                if element.rect.collidepoint(event.pos):
                    element.dragging = True
                    # 计算鼠标点击位置和元素符号左上角的偏移量
                    element.offset = (event.pos[0] - element.rect.left, event.pos[1] - element.rect.top)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # 检查是否释放了元素符号
            for element in elements:
                if element.dragging:
                    element.dragging = False
                    # 检查是否拖拽到正确位置
                    for category, rect in categories.items():
                        if rect.collidepoint(element.rect.center):
                            if element.category == category:
                                elements.remove(element)
                                score += 1
                            else:
                                element.reset_position()
                                score -= 1
                            break

    # 更新元素符号位置
    for element in elements:
        element.update()
        screen.blit(element.image, element.rect.topleft)

    # 绘制分类框
    for category, rect in categories.items():
        pygame.draw.rect(screen, GREEN, rect, 2)

    # 显示得分
    font = pygame.font.Font("./Fonts/simsun.ttc", 30)
    score_text = font.render(f"得分: {score}", True, WHITE)
    text = font.render(" 非金属元素        金属元素       稀有气体元素", True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(text, (50, 510))

    pygame.display.flip()
    clock.tick(60)

# 退出游戏
pygame.quit()
sys.exit()
