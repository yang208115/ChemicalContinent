import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

pygame.init()

# 创建 matplotlib 图形
fig = Figure(figsize=(11, 11))
ax = fig.add_subplot(111)

# 渲染化学方程式（示例方程式：2 H2 + O2 -> 2 H2O）
equation = r"$\mathrm{H}_2$"
ax.text(0.5, 0.5, equation, fontsize=20, ha='center', va='center')

# 使用 matplotlib 渲染为图像
canvas = FigureCanvas(fig)
buf = io.BytesIO()
canvas.print_png(buf)
buf.seek(0)

# 将图像加载到 Pygame
equation_image = pygame.image.load(buf)

# 设置屏幕大小
screen = pygame.display.set_mode((800, 600))

# 游戏循环
running = True
while running:

    ax.text(0.5, 0.5, equation, fontsize=20, ha='center', va='center')

    # 使用 matplotlib 渲染为图像
    canvas = FigureCanvas(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    buf.seek(0)

    # 将图像加载到 Pygame
    equation_image = pygame.image.load(buf)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 绘制化学方程式图像
    screen.fill((255, 255, 255))  # 清空屏幕
    screen.blit(equation_image, (-138, -120))  # 绘制化学方程式图像到指定位置

    pygame.display.flip()

pygame.quit()
