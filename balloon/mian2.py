# -*- coding: utf-8 -*-
import pygame
import random
import sys
import re
import os

pygame.init()


class SceneSwitching:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('chemical reaction')
        self.clock = pygame.time.Clock()

        self.game_run = True
        self.screen = pygame.display.set_mode((800, 600))

        # self.scene = Balloons()
        self.scenes = MainScene(self, self.clock)

    def run_game(self):
        self.scenes.run_game()


class MainScene():
    def __init__(self, scene, clock):
        self.screen = scene.screen
        self.clock = clock
        pygame.display.set_caption('chemical reaction')
        self.scene = scene

    def run_game(self):
        """定义游戏主程序"""

        while self.scene.game_run:
            self._check_event()
            self.load_img()

            self.update_screen()
            pygame.display.update()
            self.clock.tick(60)

    def _check_event(self):
        """检查事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 500 <= mouse_x <= 500 + 200:
                    if 380 <= mouse_y <= 380 + 100:
                        self.scene.scenes = Balloons(self.clock)
                        self.scene.scenes.run_game()

    def update_screen(self):
        self.screen.fill((135, 180, 255))
        self.screen.blit(self.start_game, (500, 380))

    def load_img(self):
        self.start_game = pygame.image.load('image/start_game.png')


class Balloons:
    def __init__(self, clock):
        """初始化Balloons类"""
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Balloon')
        self.clock = clock
        self.balloon_number = 0
        self.topic_show = False
        self.topic_id = 0
        self.score = 0
        self.step = 0
        self.length = 200
        self.balloon_speed = 3
        self.balloons = pygame.sprite.Group()

        self.game_run = True
        self.if_game_over = False

    def run_game(self):
        """定义游戏主程序"""

        while self.game_run:
            self._check_event()
            self.load_image()
            self.create_balloon()
            self.update_balloon()
            self.set_show_score()
            self.game_over()

            self.update_screen()
            pygame.display.update()
            self.clock.tick(60)

    def update_screen(self):
        """更新屏幕"""
        if not self.if_game_over:
            self.screen.fill((135, 180, 255))
            self.screen.blit(self.bg, (0, 0))
            self.balloons.draw(self.screen)
            self.create_answer()
            self.screen.blit(self.score_text, (40, 20))
            pygame.draw.rect(self.screen, (192, 192, 192), (295, 0, self.length + 10, 20))
            pygame.draw.rect(self.screen, (251, 174, 63), (295, 0, self.step % self.length + 15, 20))
            self.screen.blit(self.picture, (self.step % self.length + 295 - 5, 0))

        if self.if_game_over:
            self.screen.blit(self.game_over_img, (200, 100))
            self.screen.blit(self.start_game, (500, 380))

    def _check_event(self):
        """检查事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                moues_x, moues_y = pygame.mouse.get_pos()
                self.check_moues(moues_x, moues_y)

    def load_image(self):
        """
        加载图片

        通过pygame的image类的load方法加载图片
        并且修改图片尺寸和大小

        return : None
        """
        self.bg_tmp = pygame.image.load('image/bg_skies.png')
        self.bg = pygame.transform.scale(self.bg_tmp, (800, 600))
        self.balloon_tmp = pygame.image.load('image/balloon.png')
        self.balloon = pygame.transform.rotozoom(self.balloon_tmp, 0, 0.1)  # 984*1420
        self.game_over_img_tmp = pygame.image.load('image/game_over.png')
        self.game_over_img = pygame.transform.scale(self.game_over_img_tmp, (400, 200))
        self.start_game = pygame.image.load('image/start_game.png')
        self.picture_tmp = pygame.image.load('image/balloon.png')
        self.picture = pygame.transform.scale(self.picture_tmp, (20, 20))

        self.topic = []  # 动态加载题库图片
        self.topic_tmp, self.topic_num = extract_files_with_id('image/', 1)
        for i in range(0, self.topic_num):
            topic_img = pygame.image.load(self.topic_tmp[i])
            self.topic.append(topic_img)

        self.answer_image = []  # 动态加载答案图片
        self.answer_tmp, self.answer_num = extract_files_with_id('image/', 2)
        for i in range(0, self.answer_num):
            answer_img = pygame.image.load(self.answer_tmp[i])
            self.answer_image.append(answer_img)

    def create_balloon(self):
        """创建气球"""
        if self.balloon_number != 4:  # 检查气球数量是否为4
            balloon_number_x = [80, 280, 480, 680]  # 设置气球初始x轴坐标
            a = 0
            b = random.sample([i for i in range(0, self.answer_num)], 4)  # 从一个指定范围内的数字中随机选择4个不重复的数字
            for num in balloon_number_x:  # 创建气球
                answer_id = b[a]  # 获取答案id
                self.answer_images = pygame.transform.rotozoom(self.answer_image[b[a]], 0, 0.1)  # 创建气球图片
                a += 1
                balloons = Balloon(self.answer_images, self, answer_id)  # 创建气球
                self.answer_ids = random.choice(b)
                balloons.rect.x = num  # 初始化气球x坐标
                self.balloons.add(balloons)  # 加入精灵组
                self.balloon_number += 1

    def create_answer(self):
        """创建题目"""
        if not self.topic_show:
            # self.topic_id = random.randint(0, b=self.topic_num - 1)
            self.topic_id = self.answer_ids
        self.screen.blit(self.topic[self.topic_id], (60, 500))  # 显示题目
        self.topic_show = True

    def remove_balloon(self):
        for balloon in self.balloons:
            self.balloons.remove(balloon)
            self.balloon_number = 0
            self.topic_show = False
            self.step = 0
            print(self.balloon_speed)

    def _check_balloon_y(self):
        for balloon in self.balloons:
            if balloon.rect.y >= 510:
                self.score -= 1
                break
        for balloon in self.balloons:
            if balloon.rect.y >= 510:
                self.remove_balloon()

    def update_balloon(self):
        self.balloons.update()
        self.step += float(200 / (510 / self.balloon_speed))
        self._check_balloon_y()

    def check_moues(self, x, y):
        for balloon in self.balloons:
            if balloon.rect.y <= y <= balloon.rect.y + 243:
                if balloon.rect.x <= x <= balloon.rect.x + 190:
                    balloon.check_answer()
        if self.if_game_over:
            if 500 <= x <= 500 + 200:
                if 380 <= y <= 380 + 100:
                    self.remove_balloon()
                    self.create_balloon()
                    self.score = 0
                    self.if_game_over = False

    def reset_balloon(self):
        self.score += 1
        self.remove_balloon()
        self.set_balloon_speed()

    def set_show_score(self):
        self.score_text_tmp = " 得分：" + str(self.score)
        self.font = pygame.font.Font("c:/windows/Fonts/simhei.ttf", 30)
        self.score_text = self.font.render(self.score_text_tmp, True, (255, 0, 0))

    def game_over(self):
        if self.score < 0:
            self.if_game_over = True

    def set_balloon_speed(self):
        if self.score == 10:
            self.balloon_speed = 3 + 1
        elif self.score == 20:
            self.balloon_speed = 3 + 1 + 0.8
        elif self.score == 30:
            self.balloon_speed = 3 + 1 + 0.8 + 0.6
        elif self.score == 40:
            self.balloon_speed = 3 + 1 + 0.8 + 0.6 + 0.4
        elif self.score == 50:
            self.balloon_speed = 3 + 1 + 0.8 + 0.6 + 0.4 + 0.2


class Balloon(pygame.sprite.Sprite):
    def __init__(self, image, balloon, answer_id):
        pygame.sprite.Sprite.__init__(self)
        self.answer_id = answer_id
        self.image = image
        self.screen = balloon.screen
        self.balloon = balloon
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = 10
        self.speed = self.balloon.balloon_speed

    def update(self):
        self.rect.y += self.speed

    def check_answer(self):
        if self.balloon.topic_id == self.answer_id:
            self.balloon.reset_balloon()
        elif self.balloon.topic_id != self.answer_id:
            self.balloon.score -= 1
            self.balloon.remove_balloon()


def extract_files_with_id(folder_path, target_id):
    id_pattern = re.compile(r'(\d+)_(\d+)\.png')  # 正则表达式用于匹配数字_数字.png的模式
    a = 0

    results = []  # 存储提取出来的文件路径的列表

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.png'):  # 假设你的图片文件是以.png结尾的
            # 使用正则表达式从文件名中提取两个数字
            match = id_pattern.search(filename)
            if match:
                extracted_id = int(match.group(2))  # 提取第一个数字部分
                if extracted_id == target_id:
                    results.append(file_path)  # 将提取出来的文件路径添加到结果列表中
                    a += 1

    return results, a


if __name__ == '__main__':
    cr = SceneSwitching()
    cr.run_game()
    # cr = Balloons()
    # cr.run_game()
