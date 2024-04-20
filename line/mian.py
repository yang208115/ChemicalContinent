import pygame
import sys

# 初始化 Pygame
pygame.init()

# 定义常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)
FONT_COLOR = (0, 0, 0)
QUESTION_FONT_SIZE = 24
OPTION_FONT_SIZE = 20
LINE_COLOR = (0, 0, 0)
LINE_WIDTH = 2

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("连线问答游戏")

# 游戏状态变量
questions = [
    {
        "question": "把下面的动物和它们的英文名连线：",
        "options": ["狗", "猫", "鸟", "鱼"],
        "correct_order": [3, 1, 0, 2]  # 鱼、猫、狗、鸟
    },
    {
        "question": "把下面的水果和它们的英文名连线：",
        "options": ["苹果", "橙子", "香蕉", "草莓"],
        "correct_order": [0, 1, 2, 3]  # 苹果、橙子、香蕉、草莓
    }
]
current_question = 0
points = []  # 存储选项位置
lines = []  # 存储连线的起点和终点

# 加载字体
question_font = pygame.font.Font("./Fonts/simsun.ttc", 24)
option_font = pygame.font.Font("./Fonts/simsun.ttc", 24)

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击选项进行连线
                pos = pygame.mouse.get_pos()
                if len(points) < len(questions[current_question]["options"]):
                    points.append(pos)

                    # 检查是否连接完整一组选项
                    if len(points) == len(questions[current_question]["options"]):
                        # 检查连线顺序是否正确
                        correct_order = questions[current_question]["correct_order"]
                        matched = True
                        for i in range(len(correct_order)):
                            if i != correct_order.index(i):
                                matched = False
                                break

                        if matched:
                            print("答案正确！")
                        else:
                            print("答案错误！")

    # 绘制游戏界面
    screen.fill(BACKGROUND_COLOR)

    # 绘制问题
    question_text = question_font.render(questions[current_question]["question"], True, FONT_COLOR)
    screen.blit(question_text, (20, 20))

    # 绘制选项
    option_y = 100
    for i, option in enumerate(questions[current_question]["options"]):
        option_text = option_font.render(option, True, FONT_COLOR)
        screen.blit(option_text, (100, option_y))
        option_y += 40

    # 绘制选项的连线
    for i in range(len(points) - 1):
        pygame.draw.line(screen, LINE_COLOR, points[i], points[i + 1], LINE_WIDTH)

    # 更新屏幕
    pygame.display.flip()

# 退出游戏
pygame.quit()
sys.exit()
