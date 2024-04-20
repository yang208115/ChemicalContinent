import pygame
import sys
import math

# 初始化 Pygame
pygame.init()

# 定义常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)
POINT_COLOR = (0, 0, 0)
LINE_COLOR = (0, 0, 0)
POINT_RADIUS = 5
LINE_WIDTH = 2

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("连线游戏")

# 定义点和线的类
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

# 初始化游戏状态变量
points = []
lines = []

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 鼠标左键点击
                mouse_x, mouse_y = pygame.mouse.get_pos()
                new_point = Point(mouse_x, mouse_y)

                # 点之间的连线角度约束，相邻点之间的连线不能超过45度
                if len(points) >= 1:
                    last_point = points[-1]
                    dx = new_point.x - last_point.x
                    dy = new_point.y - last_point.y
                    angle = math.degrees(math.atan2(dy, dx))
                    if abs(angle) <= 45:
                        points.append(new_point)
                        if len(points) >= 2:
                            lines.append(Line(points[-2], points[-1]))
                else:
                    points.append(new_point)

    # 渲染游戏界面
    screen.fill(BACKGROUND_COLOR)

    # 绘制点
    for point in points:
        pygame.draw.circle(screen, POINT_COLOR, (point.x, point.y), POINT_RADIUS)

    # 绘制线
    for line in lines:
        pygame.draw.line(screen, LINE_COLOR, (line.start_point.x, line.start_point.y),
                         (line.end_point.x, line.end_point.y), LINE_WIDTH)

    # 检查游戏结束条件：所有点都已连接
    if len(points) > 1 and all(point.connected for point in points):
        # 游戏胜利，显示提示信息
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render("Congratulations! You connected all points!", True, (255, 0, 0))
        screen.blit(text_surface, (200, 250))

    # 更新屏幕
    pygame.display.flip()

# 退出游戏
pygame.quit()
sys.exit()