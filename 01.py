import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import pygame
from pygame.locals import *

# 初始化 Pygame
pygame.init()

# 创建 matplotlib 图形
fig = Figure(figsize=(8, 6))
ax = fig.add_subplot(111)

# 隐藏坐标轴
ax.axis('off')

# 渲染化学方程式
equation = r"$\mathrm{H_2}$"
equation_fontsize = 40  # 设置方程式的字体大小

# 设置屏幕大小
screen = pygame.display.set_mode((800, 600))

x = 400
y = 300

# 游戏循环
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 获取当前按键状态
    key_press = pygame.key.get_pressed()

    # 根据按键移动方程式位置
    if key_press[K_LEFT]:
        x -= 5
    if key_press[K_RIGHT]:
        x += 5

    # 清空屏幕
    screen.fill((0, 0, 0))

    # 绘制化学方程式
    ax.clear()  # 清空绘图区域
    ax.text(x, y, equation, fontsize=equation_fontsize, ha='center', va='center')
    canvas = FigureCanvas(fig)  # 创建画布
    buf = io.BytesIO()  # 创建字节流缓冲区
    # canvas.draw()  # 绘制画布
    canvas.print_png(buf)  # 将图形绘制到字节流中
    buf.seek(0)  # 移动指针到开头

    # 将图像加载到 Pygame
    equation_image = pygame.image.load(buf)
    screen.blit(equation_image, (0, 0))  # 绘制方程式图像到屏幕上

    pygame.display.flip()  # 更新显示
    clock.tick(60)  # 控制帧率

pygame.quit()
