# -*- coding: utf-8 -*-
import pygame
import threading
import random
from time import sleep
from threading import Thread
import sys
from Balloons import BalloonLeft, BalloonRight
from extract_files_with_id import extract_files_with_id
from QATwoPlayer import QATwoPlayer


class BalloonsTwoPlayer:
    def __init__(self, clock, scene, level):
        """初始化Balloons类"""
        self.screen = scene.screen
        self.scene = scene
        pygame.display.set_caption('Balloon_two_player')
        self.clock = clock
        self.balloon_number = [0, 0]
        self.topic_show = [False, False]
        self.topic_id = 0
        self.score = [0, 0]
        self.step = [0, 0]
        self.length = 200
        self.balloon_speed_left = 0.6
        self.balloon_speed_right = 0.6
        self.time = 10
        self.if_time_threading = False
        self.if_left_win = False
        self.if_right_win = False
        self.if_deuce_win = False
        self.level = level
        self.balloons_left = pygame.sprite.Group()
        self.balloons_right = pygame.sprite.Group()

        pygame.mixer.music.load('Musics/musics.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

        self.game_run = True
        self.if_game_over = False
        self.if_create_balloon_over = True

    def run_game(self):
        """定义游戏主程序"""

        self.load_image()
        while self.game_run:
            self._check_event()
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
            self.clock.tick(60)

    def update_screen(self):
        """更新屏幕"""
        if not self.if_game_over:
            self.screen.fill((135, 180, 255))
            self.screen.blit(self.bg, (0, 0))
            self.balloons_left.draw(self.screen)
            self.balloons_right.draw(self.screen)
            self.create_answer_left()
            self.create_answer_right()
            self.screen.blit(self.score_text_left, (70, 50))
            pygame.draw.rect(self.screen, (192, 192, 192), (90, 0, self.length + 10, 20))
            pygame.draw.rect(self.screen, (251, 174, 63), (90, 0, self.step[0] % self.length + 15, 20))
            self.screen.blit(self.picture, (self.step[0] % self.length + 90 - 5, 0))
            pygame.draw.line(self.screen, 'black', (400, 0), (400, 800), 5)
            self.screen.blit(self.score_text_right, (420, 50))
            pygame.draw.rect(self.screen, (192, 192, 192), (490, 0, self.length + 10, 20))
            pygame.draw.rect(self.screen, (251, 174, 63), (490, 0, self.step[1] % self.length + 15, 20))
            self.screen.blit(self.picture, (self.step[1] % self.length + 490 - 5, 0))
            pygame.draw.rect(self.screen, (255, 255, 0), (305, 0, 180, 30))
            self.screen.blit(self.time_text, (385, 0))

        if self.if_left_win:
            self.screen.blit(self.win, (75, 200))
            # self.screen.blit(self.lost, (400, 200))
            self.if_game_over = True
            pygame.mixer.music.stop()
            self.screen.blit(self.next_level, (550, 500))
            self.screen.blit(self.return_select_sLevel, (330, 500))
            self.screen.blit(self.return_main_scene, (110, 500))

        if self.if_right_win:
            self.screen.blit(self.win, (475, 200))
            # self.screen.blit(self.lost, (0, 200))
            self.if_game_over = True
            pygame.mixer.music.stop()
            self.screen.blit(self.next_level, (550, 500))
            self.screen.blit(self.return_select_sLevel, (330, 500))
            self.screen.blit(self.return_main_scene, (110, 500))

        if self.if_deuce_win:
            self.screen.blit(self.deuce, (200, 100))
            self.if_game_over = True
            pygame.mixer.music.stop()
            self.screen.blit(self.next_level, (550, 500))
            self.screen.blit(self.return_select_sLevel, (330, 500))
            self.screen.blit(self.return_main_scene, (110, 500))

        self.screen.blit(self.return_, (10, 10))

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
        # self.start_game = pygame.image.load('image/start_game.png')
        self.picture_tmp = pygame.image.load('image/balloon.png')
        self.picture = pygame.transform.scale(self.picture_tmp, (20, 20))

        self.topic = []  # 动态加载题库图片 684 * 40
        self.topic_tmp, self.topic_num = extract_files_with_id(f'image/{self.level}', 1)
        for i in range(0, self.topic_num):
            topic_img_tmp = pygame.image.load(self.topic_tmp[i])
            topic_img = pygame.transform.scale(topic_img_tmp, (400, 40))
            self.topic.append(topic_img)

        self.answer_image = []  # 动态加载答案图片
        self.answer_tmp, self.answer_num = extract_files_with_id(f'image/{self.level}', 2)
        for i in range(0, self.answer_num):
            answer_img_tmp = pygame.image.load(self.answer_tmp[i])
            answer_img = pygame.transform.rotozoom(answer_img_tmp, 0, 0.6)
            self.answer_image.append(answer_img)

        self.win_tmp = pygame.image.load('image/win2.png')
        self.win = pygame.transform.scale(self.win_tmp, (250, 250))
        self.lost = pygame.image.load('image/lost.png')
        self.deuce_tmp = pygame.image.load('image/game_deuce.png')
        self.deuce = pygame.transform.scale(self.deuce_tmp, (400, 300))
        self.next_level_tmp = pygame.image.load('image/next_level.png')
        self.next_level = pygame.transform.rotozoom(self.next_level_tmp, 0, 0.5)
        self.return_main_scene_tmp = pygame.image.load('image/return_main_scene.png')
        self.return_main_scene = pygame.transform.rotozoom(self.return_main_scene_tmp, 0, 0.5)
        self.return_select_sLevel_tmp = pygame.image.load('image/return_select_aLevel.png')
        self.return_select_sLevel = pygame.transform.rotozoom(self.return_select_sLevel_tmp, 0, 0.5)
        self.return_tmp = pygame.image.load("./image/return.png")
        self.return_ = pygame.transform.scale(self.return_tmp, (80, 80))

    def create_balloon_left(self):
        """创建气球"""
        if self.balloon_number[0] != 4:  # 检查气球数量是否为4
            balloon_number_x = [40, 130, 230, 320]  # 设置气球初始x轴坐标
            a = 0
            b = random.sample([i for i in range(0, self.answer_num)], 4)  # 从一个指定范围内的数字中随机选择4个不重复的数字
            for num in balloon_number_x:  # 创建气球
                answer_id = b[a]  # 获取答案id
                self.answer_images = pygame.transform.rotozoom(self.answer_image[b[a]], 0, 0.1)  # 创建气球图片
                a += 1

                balloons_lefts = BalloonLeft(self.answer_images, self, answer_id)  # 创建气球
                self.answer_ids_left = random.choice(b)
                balloons_lefts.rect.x = num  # 初始化气球x坐标
                self.balloons_left.add(balloons_lefts)  # 加入精灵组
                self.balloon_number[0] += 1

    def create_balloon_right(self):
        """创建气球"""
        if self.balloon_number[1] != 4:  # 检查气球数量是否为4
            balloon_number_x = [440, 440 + 90, 440 + 90 + 100, 440 + 90 + 100 + 90]  # 设置气球初始x轴坐标
            a = 0
            b = random.sample([i for i in range(0, self.answer_num)], 4)  # 从一个指定范围内的数字中随机选择4个不重复的数字
            for num in balloon_number_x:  # 创建气球
                answer_id = b[a]  # 获取答案id
                self.answer_images = pygame.transform.rotozoom(self.answer_image[b[a]], 0, 0.1)  # 创建气球图片
                a += 1

                balloons_rights = BalloonRight(self.answer_images, self, answer_id)  # 创建气球
                self.answer_ids_right = random.choice(b)
                balloons_rights.rect.x = num  # 初始化气球x坐标
                self.balloons_right.add(balloons_rights)  # 加入精灵组
                self.balloon_number[1] += 1

    def create_answer_left(self):
        """创建题目"""
        if not self.topic_show[0]:
            self.topic_id_left = self.answer_ids_left
        self.screen.blit(self.topic[self.topic_id_left], (0, 500))  # 显示题目
        self.topic_show[0] = True

    def create_answer_right(self):
        """创建题目"""
        if not self.topic_show[1]:
            self.topic_id_right = self.answer_ids_right
        self.screen.blit(self.topic[self.topic_id_right], (400, 500))  # 显示题目
        self.topic_show[1] = True

    def remove_balloon_left(self):
        for balloon in self.balloons_left:
            self.balloons_left.remove(balloon)
            self.balloon_number[0] = 0
            self.topic_show[0] = False
            self.step[0] = 0

    def remove_balloon_right(self):
        for balloon in self.balloons_right:
            self.balloons_right.remove(balloon)
            self.balloon_number[1] = 0
            self.topic_show[1] = False
            self.step[1] = 0

    def _check_balloon_y(self):
        for balloon in self.balloons_left:
            if balloon.rect.y >= 510:
                self.score[0] -= 1
                break
        for balloon in self.balloons_left:
            if balloon.rect.y >= 510:
                self.remove_balloon_left()
        for balloon in self.balloons_right:
            if balloon.rect.y >= 510:
                self.score[1] -= 1
                break
        for balloon in self.balloons_right:
            if balloon.rect.y >= 510:
                self.remove_balloon_right()

    def update_balloon(self):
        if self.if_create_balloon_over:
            self.t1 = Thread(target=self.update_balloons)
            self.t1.start()
            self.if_create_balloon_over = True

    def update_balloons(self):
        self.balloons_left.update()
        self.balloons_right.update()
        self.step[0] += float(200 / (510 / self.balloon_speed_left))
        self.step[1] += float(200 / (510 / self.balloon_speed_right))
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
            if 110 <= x <= 110+170:
                if 500 <= y <= 500+60:
                    self.scene.set_main_scene()
            if 330 <= x <= 330+170:
                if 500 <= y <= 500+60:
                    self.scene.set_selecta_level(2)
            if 550 <= x <= 550+170:
                if 500 <= y <= 500+60:
                    self.scene.scenes = QATwoPlayer(self.clock, self.scene)
                    self.scene.run_game()
        if 10 <= x <= 90 and 10 <= y <= 90:
            pygame.mixer.music.stop()
            self.scene.set_main_scene()

    def reset_balloon_left(self):
        self.score[0] += 1
        self.balloon_speed_right += 0.01
        self.remove_balloon_left()
        self.set_balloon_speed_left()

    def reset_balloon_right(self):
        self.score[1] += 1
        self.balloon_speed_left += 0.01
        self.remove_balloon_right()
        self.set_balloon_speed_right()

    def set_show_score_left(self):
        self.score_text_tmp = " 得分：" + str(self.score[0])
        self.font = pygame.font.Font("c:/windows/Fonts/simhei.ttf", 30)
        self.score_text_left = self.font.render(self.score_text_tmp, True, (255, 0, 0))

    def set_show_score_right(self):
        self.score_text_tmp = " 得分：" + str(self.score[1])
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
            if self.score[0] > self.score[1]:
                self.if_left_win = True
            elif self.score[1] > self.score[0]:
                self.if_right_win = True
            elif self.score[0] == self.score[1]:
                self.if_deuce_win = True

    def set_balloon_speed_left(self):
        if self.score[0] == 10:
            self.balloon_speed_left = 0.6 + 0.5
        elif self.score[0] == 20:
            self.balloon_speed_left = 0.6 + 0.5 + 0.4
        elif self.score[0] == 30:
            self.balloon_speed_left = 0.6 + 0.5 + 0.4 + 0.3
        elif self.score[0] == 40:
            self.balloon_speed_left = 0.6 + 0.5 + 0.4 + 0.3 + 0.2
        elif self.score[0] == 50:
            self.balloon_speed_left = 0.6 + 0.5 + 0.4 + 0.3 + 0.2 + 0.1

    def set_balloon_speed_right(self):
        if self.score[1] == 10:
            self.balloon_speed_right = 0.6 + 0.5
        elif self.score[1] == 20:
            self.balloon_speed_right = 0.6 + 0.5 + 0.4
        elif self.score[1] == 30:
            self.balloon_speed_right = 0.6 + 0.5 + 0.4 + 0.3
        elif self.score[1] == 40:
            self.balloon_speed_right = 0.6 + 0.5 + 0.4 + 0.3 + 0.2
        elif self.score[1] == 50:
            self.balloon_speed_right = 0.6 + 0.5 + 0.4 + 0.3 + 0.2 + 0.1

    def set_time_num(self):
        while self.game_run:
            self.time -= 1
            sleep(1)
            if self.if_game_over:
                break
