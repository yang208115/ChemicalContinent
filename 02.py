import pygame
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

# 初始化 Pygame
pygame.init()

# 创建 matplotlib 图形
fig = Figure(figsize=(8, 6))
ax = fig.add_subplot(111)

# 隐藏坐标轴和刻度
ax.axis('off')

# 渲染化学方程式
equation = r"$\mathrm{2H_2 + O_2 \to 2H_2O}$"
equation_fontsize = 20
equation_position = (200, 200)  # 初始位置

# 使用 matplotlib 渲染为图像
def render_equation(equation, fontsize, position):
    ax.clear()  # 清空绘图区域
    ax.text(position[0], position[1], equation, fontsize=fontsize, ha='center', va='center')
    canvas.draw()  # 绘制图形
    buf = canvas.tostring_rgb()  # 转换为 RGB 字节流
    size = canvas.get_width_height()  # 获取图像大小
    equation_image = pygame.image.fromstring(buf, size, "RGB")  # 创建 Pygame 图像
    return equation_image

# 创建 matplotlib 画布
canvas = FigureCanvas(fig)

# 设置屏幕大小
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 初始方程式图像
equation_image = render_equation(equation, equation_fontsize, equation_position)

# 游戏循环
running = True
dragging = False
offset_x, offset_y = 0, 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # 检查鼠标是否点击了方程式图像
                equation_rect = equation_image.get_rect(topleft=equation_position)
                if equation_rect.collidepoint(event.pos):
                    dragging = True
                    mouse_x, mouse_y = event.pos
                    offset_x = equation_position[0] - mouse_x
                    offset_y = equation_position[1] - mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                # 更新方程式位置
                mouse_x, mouse_y = event.pos
                equation_position = (mouse_x + offset_x, mouse_y + offset_y)
                equation_image = render_equation(equation, equation_fontsize, equation_position)

    # 绘制
    screen.fill((255, 255, 255))
    screen.blit(equation_image, equation_position)
    pygame.display.flip()

pygame.quit()
