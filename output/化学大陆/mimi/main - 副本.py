# coding=gbk

import pygame
import sys
import random

# ��ʼ��pygame
pygame.init()

# ���ô��ڳߴ�ͱ���
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ԫ��������")

# ������ɫ
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# ���ر���ͼ��
background = pygame.image.load("./image/bg_skies.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


# ����Ԫ�ط�����
class Element(pygame.sprite.Sprite):
    def __init__(self, symbol, category, position):
        super().__init__()
        self.symbol = symbol
        self.category = category
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)  # Ԫ�ط����ú�ɫ��ʾ
        self.font = pygame.font.Font("./Fonts/simsun.ttc", 30)
        text = self.font.render(symbol, True, WHITE)
        self.image.blit(text, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.original_position = position  # ��¼Ԫ�ط��ŵ�ԭʼλ��
        self.dragging = False
        self.score = 0

    def update(self):
        # ���Ԫ�ط������ڱ���ק�������λ��Ϊ���λ��
        if self.dragging:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.topleft = (mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1])

    def reset_position(self):
        self.rect.topleft = self.original_position


# ����Ԫ�ط����б�
elements_data = [
    ("H", "�ǽ���Ԫ��"),
    ("He", "ϡ������Ԫ��"),
    ("Li", "����Ԫ��"),
    ("Be", "����Ԫ��"),
    ("C", "�ǽ���Ԫ��"),
    ("O", "�ǽ���Ԫ��"),
    ("Na", "����Ԫ��"),
    ("Mg", "����Ԫ��"),
    ("Ne", "ϡ������Ԫ��"),
    ("K", "����Ԫ��"),
    ("Ar", "ϡ������Ԫ��"),
    ("Sc", "����Ԫ��"),
    ("N", "�ǽ���Ԫ��"),
    ("Br", "�ǽ���Ԫ��"),
    ("Ca", "����Ԫ��"),
    ("Kr", "ϡ������Ԫ��"),
    # ������Ӹ���Ԫ�ط���...
]

pos = [
    (100, 100),(200, 100),(300, 100),(400, 100),
    (100, 200),(200, 200),(300, 200),(400, 200),
    (100, 300),(200, 300),(300, 300),(400, 300),
    (100, 400),(200, 400),(300, 400),(400, 400),
]
random.shuffle(pos)
elements = [Element(data[0], data[1], pos[i]) for i, data in enumerate(elements_data)]

# ���������
categories = {
    "�ǽ���Ԫ��": pygame.Rect(50, 500, 200, 50),
    "����Ԫ��": pygame.Rect(300, 500, 200, 50),
    "ϡ������Ԫ��": pygame.Rect(550, 500, 200, 50)
}

# ��Ϸ��ѭ��
running = True
clock = pygame.time.Clock()
score = 0

while running:
    screen.blit(background, (0, 0))

    # �����¼�
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # ����Ƿ�����Ԫ�ط���
            for element in elements:
                if element.rect.collidepoint(event.pos):
                    element.dragging = True
                    # ���������λ�ú�Ԫ�ط������Ͻǵ�ƫ����
                    element.offset = (event.pos[0] - element.rect.left, event.pos[1] - element.rect.top)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # ����Ƿ��ͷ���Ԫ�ط���
            for element in elements:
                if element.dragging:
                    element.dragging = False
                    # ����Ƿ���ק����ȷλ��
                    for category, rect in categories.items():
                        if rect.collidepoint(element.rect.center):
                            if element.category == category:
                                elements.remove(element)
                                score += 1
                            else:
                                element.reset_position()
                                score -= 1
                            break

    # ����Ԫ�ط���λ��
    for element in elements:
        element.update()
        screen.blit(element.image, element.rect.topleft)

    # ���Ʒ����
    for category, rect in categories.items():
        pygame.draw.rect(screen, GREEN, rect, 2)

    # ��ʾ�÷�
    font = pygame.font.Font("./Fonts/simsun.ttc", 30)
    score_text = font.render(f"�÷�: {score}", True, WHITE)
    text = font.render(" �ǽ���Ԫ��        ����Ԫ��       ϡ������Ԫ��", True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(text, (50, 510))

    pygame.display.flip()
    clock.tick(60)

# �˳���Ϸ
pygame.quit()
sys.exit()
