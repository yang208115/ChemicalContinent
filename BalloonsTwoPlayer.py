# -*- coding: utf-8 -*-
import pygame
import threading
import random
import time
import sys
from Balloons import Balloon_left, Balloon_right
from extract_files_with_id import extract_files_with_id

class BalloonsTwoPlayer:
    def __init__(self, clock, screen):
        """初始化Balloons类"""
        self.screen = screen
        pygame.display.set_caption('Balloon_two_player')
        self.clock = clock
        self.balloon_number_left = 0
        self.balloon_number_right = 0
        self.topic_show_left = False
        self.topic_show_right = False
        self.topic_id = 0
        self.score_left = 0
        self.score_right = 0
        self.step_left = 0
        self.step_right = 0
        self.length = 200
        self.balloon_speed_left = 3
        self.balloon_speed_right = 3
        self.time = 90
        self.if_time_threading = False
        self.if_left_win = False
        self.if_right_win = False
        self.balloons_left = pygame.sprite.Group()
        self.balloons_right = pygame.sprite.Group()

        self.game_run = True
        self.if_game_over = False

    def run_game(self):
        """定义游戏主程序"""

        while self.game_run:
            self._check_event()
            self.load_image()
            self.create_balloon_left()
            self.create_balloon_right()
            self.update_balloon()
            self.set_show_score_left()
            self.set_show_score_right()
            self.game_over()
            self.set_show_time()
            self.set_time()

            self.update_screen()
            pygame.display.update()
            self.clock.tick(120)

    def update_screen(self):
        """更新屏幕"""
        if not self.if_game_over:
            self.screen.fill((135, 180, 255))
            self.screen.blit(self.bg, (0, 0))
            self.balloons_left.draw(self.screen)
            self.balloons_right.draw(self.screen)
            self.create_answer_left()
            self.create_answer_right()
            self.screen.blit(self.score_text_left, (20, 50))
            pygame.draw.rect(self.screen, (192, 192, 192), (90, 0, self.length + 10, 20))
            pygame.draw.rect(self.screen, (251, 174, 63), (90, 0, self.step_left % self.length + 15, 20))
            self.screen.blit(self.picture, (self.step_left % self.length + 90 - 5, 0))
            pygame.draw.line(self.screen, 'black', (400, 0), (400, 800), 5)
            self.screen.blit(self.score_text_right, (420, 50))
            pygame.draw.rect(self.screen, (192, 192, 192), (490, 0, self.length + 10, 20))
            pygame.draw.rect(self.screen, (251, 174, 63), (490, 0, self.step_right % self.length + 15, 20))
            self.screen.blit(self.picture, (self.step_right % self.length + 490 - 5, 0))
            pygame.draw.rect(self.screen, (255, 255, 0), (305, 0, 180, 30))
            self.screen.blit(self.time_text, (385, 0))

        if self.if_left_win:
            self.screen.blit(self.win, (75, 200))
            # self.screen.blit(self.lost, (400, 200))
            self.if_game_over = True

        if self.if_right_win:
            self.screen.blit(self.win, (475, 200))
            # self.screen.blit(self.lost, (0, 200))
            self.if_game_over = True

    def _check_event(self):
        """检查事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.if_game_over = True
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                moues_x, moues_y = pygame.mouse.get_pos()
                self.check_moues(moues_x, moues_y)
            elif event.type == pygame.K_p:
                pygame.quit()
                sys.exit()

    def load_image(self):
        """
        加载图片

        通过pygame的image类的load方法加载图片
        并且修改图片尺寸和大小

        return : None
        """
        self.bg_tmp = pygame.image.load('image/bg_skies.png')
        self.bg = pygame.transform.scale(self.bg_tmp, (800, 600))
        self.game_over_img_tmp = pygame.image.load('image/game_over.png')
        self.game_over_img = pygame.transform.scale(self.game_over_img_tmp, (400, 200))
        self.start_game = pygame.image.load('image/start_game.png')
        self.picture_tmp = pygame.image.load('image/balloon.png')
        self.picture = pygame.transform.scale(self.picture_tmp, (20, 20))

        self.topic = []  # 动态加载题库图片 684 * 40
        self.topic_tmp, self.topic_num = extract_files_with_id('image/', 1)
        for i in range(0, self.topic_num):
            topic_img_tmp = pygame.image.load(self.topic_tmp[i])
            topic_img = pygame.transform.scale(topic_img_tmp, (400, 40))
            self.topic.append(topic_img)

        self.answer_image = []  # 动态加载答案图片
        self.answer_tmp, self.answer_num = extract_files_with_id('image/', 2)
        for i in range(0, self.answer_num):
            answer_img_tmp = pygame.image.load(self.answer_tmp[i])
            answer_img = pygame.transform.rotozoom(answer_img_tmp, 0, 0.6)
            self.answer_image.append(answer_img)

        self.win_tmp = pygame.image.load('image/win2.png')
        self.win = pygame.transform.scale(self.win_tmp, (250, 250))
        self.lost = pygame.image.load('image/lost.png')

    def create_balloon_left(self):
        """创建气球"""
        if self.balloon_number_left != 4:  # 检查气球数量是否为4
            balloon_number_x = [40, 130, 230, 320]  # 设置气球初始x轴坐标
            a = 0
            b = random.sample([i for i in range(0, self.answer_num)], 4)  # 从一个指定范围内的数字中随机选择4个不重复的数字
            for num in balloon_number_x:  # 创建气球
                answer_id = b[a]  # 获取答案id
                self.answer_images = pygame.transform.rotozoom(self.answer_image[b[a]], 0, 0.1)  # 创建气球图片
                a += 1

                balloons_lefts = Balloon_left(self.answer_images, self, answer_id)  # 创建气球
                self.answer_ids_left = random.choice(b)
                balloons_lefts.rect.x = num  # 初始化气球x坐标
                self.balloons_left.add(balloons_lefts)  # 加入精灵组
                self.balloon_number_left += 1

    def create_balloon_right(self):
        """创建气球"""
        if self.balloon_number_right != 4:  # 检查气球数量是否为4
            balloon_number_x = [440, 440 + 90, 440 + 90 + 100, 440 + 90 + 100 + 90]  # 设置气球初始x轴坐标
            a = 0
            b = random.sample([i for i in range(0, self.answer_num)], 4)  # 从一个指定范围内的数字中随机选择4个不重复的数字
            for num in balloon_number_x:  # 创建气球
                answer_id = b[a]  # 获取答案id
                self.answer_images = pygame.transform.rotozoom(self.answer_image[b[a]], 0, 0.1)  # 创建气球图片
                a += 1

                balloons_rights = Balloon_right(self.answer_images, self, answer_id)  # 创建气球
                self.answer_ids_right = random.choice(b)
                balloons_rights.rect.x = num  # 初始化气球x坐标
                self.balloons_right.add(balloons_rights)  # 加入精灵组
                self.balloon_number_right += 1

    def create_answer_left(self):
        """创建题目"""
        if not self.topic_show_left:
            self.topic_id_left = self.answer_ids_left
        self.screen.blit(self.topic[self.topic_id_left], (0, 500))  # 显示题目
        self.topic_show_left = True

    def create_answer_right(self):
        """创建题目"""
        if not self.topic_show_right:
            self.topic_id_right = self.answer_ids_right
        self.screen.blit(self.topic[self.topic_id_right], (400, 500))  # 显示题目
        self.topic_show_right = True

    def remove_balloon_left(self):
        for balloon in self.balloons_left:
            self.balloons_left.remove(balloon)
            self.balloon_number_left = 0
            self.topic_show_left = False
            self.step_left = 0

    def remove_balloon_right(self):
        for balloon in self.balloons_right:
            self.balloons_right.remove(balloon)
            self.balloon_number_right = 0
            self.topic_show_right = False
            self.step_right = 0

    def _check_balloon_y(self):
        for balloon in self.balloons_left:
            if balloon.rect.y >= 510:
                self.score_left -= 1
                break
        for balloon in self.balloons_left:
            if balloon.rect.y >= 510:
                self.remove_balloon_left()
        for balloon in self.balloons_right:
            if balloon.rect.y >= 510:
                self.score_right -= 1
                break
        for balloon in self.balloons_right:
            if balloon.rect.y >= 510:
                self.remove_balloon_right()

    def update_balloon(self):
        self.balloons_left.update()
        self.balloons_right.update()
        self.step_left += float(200 / (510 / self.balloon_speed_left))
        self.step_right += float(200 / (510 / self.balloon_speed_right))
        self._check_balloon_y()

    def check_moues(self, x, y):
        for balloon in self.balloons_left:
            if balloon.rect.y <= y <= balloon.rect.y + 59:
                if balloon.rect.x <= x <= balloon.rect.x + 85:
                    balloon.check_answer()
        for balloon in self.balloons_right:
            if balloon.rect.y <= y <= balloon.rect.y + 59:
                if balloon.rect.x <= x <= balloon.rect.x + 85:
                    balloon.check_answer()
        if self.if_game_over:
            if 500 <= x <= 500 + 200:
                if 380 <= y <= 380 + 100:
                    self.remove_balloon_left()
                    self.create_balloon_left()
                    self.score = 0
                    self.if_game_over = False

    def reset_balloon_left(self):
        self.score_left += 1
        self.remove_balloon_left()
        self.set_balloon_speed_left()

    def reset_balloon_right(self):
        self.score_right += 1
        self.remove_balloon_right()
        self.set_balloon_speed_right()

    def set_show_score_left(self):
        self.score_text_tmp = " 得分：" + str(self.score_left)
        self.font = pygame.font.Font("c:/windows/Fonts/simhei.ttf", 30)
        self.score_text_left = self.font.render(self.score_text_tmp, True, (255, 0, 0))

    def set_show_score_right(self):
        self.score_text_tmp = " 得分：" + str(self.score_right)
        self.font = pygame.font.Font("c:/windows/Fonts/simhei.ttf", 30)
        self.score_text_right = self.font.render(self.score_text_tmp, True, (255, 0, 0))

    def set_show_time(self):
        self.time_text_tmp = str(self.time)
        self.font = pygame.font.Font("c:/windows/Fonts/simhei.ttf", 30)
        self.time_text = self.font.render(self.time_text_tmp, True, (0, 0, 0))

    def set_time(self):
        if not self.if_time_threading:
            self.if_time_threading = True
            self.time_thread = threading.Thread(target=self.set_time_num)
            self.time_thread.start()

    def game_over(self):
        if self.time == 0:
            if self.score_left > self.score_right:
                self.if_left_win = True
            elif self.score_right > self.score_left:
                self.if_right_win = True

    def set_balloon_speed_left(self):
        if self.score_left == 10:
            self.balloon_speed_left = 3 + 1
        elif self.score_left == 20:
            self.balloon_speed_left = 3 + 1 + 0.8
        elif self.score_left == 30:
            self.balloon_speed_left = 3 + 1 + 0.8 + 0.6
        elif self.score_left == 40:
            self.balloon_speed_left = 3 + 1 + 0.8 + 0.6 + 0.4
        elif self.score_left == 50:
            self.balloon_speed_left = 3 + 1 + 0.8 + 0.6 + 0.4 + 0.2

    def set_balloon_speed_right(self):
        if self.score_right == 10:
            self.balloon_speed_right = 3 + 1
        elif self.score_right == 20:
            self.balloon_speed_right = 3 + 1 + 0.8
        elif self.score_right == 30:
            self.balloon_speed_right = 3 + 1 + 0.8 + 0.6
        elif self.score_right == 40:
            self.balloon_speed_right = 3 + 1 + 0.8 + 0.6 + 0.4
        elif self.score_right == 50:
            self.balloon_speed_right = 3 + 1 + 0.8 + 0.6 + 0.4 + 0.2

    def set_time_num(self):
        while self.game_run:
            self.time -= 1
            time.sleep(1)
            if self.if_game_over:
                break