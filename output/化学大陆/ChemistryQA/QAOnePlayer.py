# coding=gbk
import time
from random import sample
from threading import Thread
import pygame
import json
import sys
import os


class QAOnePlayer:
    def __init__(self, clock, scene):
        self.screen = scene.screen
        self.scene = scene
        pygame.display.set_caption('Chemistry Q&A one player')
        self.clock = clock
        self.main_path = os.path.abspath('.')
        self.topics_num = sample([1, 2, 3, 4, 5], 5)
        self.topics_num_id = 0
        self.fraction = [0, 0]
        self.time = 90
        self.score = 0
        self.topic_errors = 0
        self.statr_num = 0
        self.a = True

        self.if_game_run = True
        self.if_topic_show = False
        self.if_set_topic = False
        self.if_good = False
        self.if_error = False
        self.if_ok = False
        self.if_win = False
        self.if_stop = False
        self.if_wait = False
        self.if_time_threading = False

        with open(f'{self.main_path}/topics_one_player.json', encoding='utf-8') as f:
            data = json.load(f)
        self.topics_nums = data['num']
        self.cut_of_line = int(data['num'] * 0.4)
        self.cut_of_line2 = int(data['num'] * 0.6)

        self.Font = pygame.font.Font(f'{self.main_path}/Fonts/simsun.ttc', 18)
        pygame.mixer.music.load(f'{self.main_path}/Musics/musics.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    def run_game(self):
        self.load_image()

        while self.if_game_run:
            self.set_player_win()
            self.set_show_time()
            self.set_time()
            self.set_topic_id()
            self.compute_start()
            self.if_time()
            if self.if_win:
                pygame.mixer.music.stop()

            self._check_event()
            self.update_screen()
            self.create_topic()
            pygame.display.update()
            self.clock.tick(60)

    def load_image(self):
        self.bg = pygame.image.load(f'{self.main_path}/image/bg.png')  # 800*600
        # self.player1 = pygame.image.load(f'{self.main_path}/image/player1.png')  # 80*120
        self.answer_box_tmp = pygame.image.load(f'{self.main_path}/image/AnswerBox.png')  # 400*300
        self.answer_box = pygame.transform.rotozoom(self.answer_box_tmp, 0, 1)  # 280*210
        self.button_pairs_tmp = pygame.image.load(f'{self.main_path}/image/button_pairs.png')  # 200*200
        self.button_pairs = pygame.transform.rotozoom(self.button_pairs_tmp, 0, 0.3)  # 60*60
        self.button_error_tmp = pygame.image.load(f'{self.main_path}/image/button_error.png')  # 200*200
        self.button_error = pygame.transform.rotozoom(self.button_error_tmp, 0, 0.3)  # 60*60
        self.good = pygame.image.load(f'{self.main_path}/image/good.png')  # 120*158
        self.error = pygame.image.load(f'{self.main_path}/image/error.png')  # 160*160
        self.scoreboard = pygame.image.load(f'{self.main_path}/image/scoreboard.png')  # 500*375
        self.start = pygame.image.load(f'{self.main_path}/image/start.png')
        self.return_main_scene_tmp = pygame.image.load('image/return_main_scene.png')  # 340*120
        self.return_main_scene = pygame.transform.rotozoom(self.return_main_scene_tmp, 0, 0.7)  # 238*84
        self.return_tmp = pygame.image.load("./image/return.png")
        self.return_ = pygame.transform.scale(self.return_tmp, (80, 80))

    def update_screen(self):
        self.screen.fill((135, 180, 255))
        self.screen.blit(self.bg, (0, 0))
        # self.screen.blit(self.player1, (150, 440))
        # self.screen.blit(self.player2, (560, 440))
        self.screen.blit(self.answer_box, (200, 40))
        self.screen.blit(self.button_pairs, (250, 480))
        self.screen.blit(self.button_error, (475, 480))
        pygame.draw.rect(self.screen, (255, 255, 0), (305, 0, 180, 30))
        self.screen.blit(self.return_, (10, 10))
        if self.if_good:
            self.screen.blit(self.good, (350, 100))
        if self.if_error:
            self.screen.blit(self.error, (350, 100))
        if self.if_win:
            self.screen.blit(self.scoreboard, (150, 100))
            self.screen.blit(pygame.font.Font("./Fonts/simsun.ttc", 70).render(str(self.score), True, (0, 0, 0)),
                             (370, 310))
            self.screen.blit(self.return_main_scene, (281, 490))
        self.screen.blit(self.time_text, (385, 0))
        if self.statr_num == 1:
            self.screen.blit(self.start, (280, 250))
        if self.statr_num == 2:
            self.screen.blit(self.start, (280, 250))
            self.screen.blit(self.start, (370, 250))
        if self.statr_num == 3:
            self.screen.blit(self.start, (280, 250))
            self.screen.blit(self.start, (370, 250))
            self.screen.blit(self.start, (460, 250))

    def _check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.if_game_over = True
                self.if_stop = True
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                moues_x, moues_y = pygame.mouse.get_pos()
                self.check_moues(moues_x, moues_y)
            elif event.type == pygame.K_p:
                self.if_stop = True
                pygame.quit()
                sys.exit()

    def check_moues(self, x, y):
        if not self.if_good and not self.if_error and not self.if_win:
            if 250 < x < 310:
                if 480 < y < 540:
                    self.check_answer(0, 0)
                    t5 = Thread(target=self.wait)
                    t5.start()
            if 475 < x < 535:
                if 480 < y < 540:
                    self.check_answer(1, 0)
                    t6 = Thread(target=self.wait)
                    t6.start()
        if self.if_win:
            if 281 < x < 469:
                if 490 < y < 574:
                    self.scene.set_main_scene()
        if 10 <= x <= 90 and 10 <= y <= 90:
            pygame.mixer.music.stop()
            self.scene.set_main_scene()

    def create_topic(self):
        if not self.if_wait:
            try:
                topic = self.topics['topic']
                self.topic_if = self.topics['if']
                text_lines = topic.split('\n')
                text_surfaces = [self.Font.render(line, True, (0, 0, 0)) for line in text_lines]
                for i, line_surface in enumerate(text_surfaces):
                    self.screen.blit(line_surface, (210, 60 + i * 40))
            except IndexError:
                self.if_ok = True

    def check_answer(self, answer, position):
        if position == 0 and not self.if_wait:  # left
            if answer == int(self.topic_if):
                self.fraction[0] += 1
                t1 = Thread(target=self.set_good, args='0')
                t1.start()
                self.score += 1
            else:
                t3 = Thread(target=self.set_error, args='0')
                t3.start()
                self.topic_errors += 1
        self.if_topic_show = False

    def set_good(self, player_id):
        if int(player_id) == 0:
            self.if_good = True
            self.if_wait = True
            time.sleep(3)
            self.if_good = False
            self.if_wait = False

    def set_error(self, player_id):
        if int(player_id) == 0:
            self.if_error = True
            self.if_wait = True
            time.sleep(3)
            self.if_error = False
            self.if_wait = False

    def wait(self):
        time.sleep(3)

    def set_player_win(self):
        if self.if_ok:
            if self.if_stop:
                self.if_win = True

    def set_time(self):
        if not self.if_time_threading:
            self.if_time_threading = True
            self.time_thread = Thread(target=self.start_time)
            self.time_thread.start()

    def start_time(self):
        while self.if_game_run:
            self.time -= 1
            time.sleep(1)
            if self.if_stop:
                break

    def set_show_time(self):
        self.time_text_tmp = str(self.time)
        self.font = pygame.font.Font("./Fonts/simsun.ttc", 30)
        self.time_text = self.font.render(self.time_text_tmp, True, (0, 0, 0))

    def if_time(self):
        if self.time == 0:
            self.if_stop = True
            self.if_win = True

    def set_topic_id(self):
        if not self.if_topic_show:
            with open(f'{self.main_path}/topics_one_player.json', encoding='utf-8') as f:
                data = json.load(f)
            if self.a:
                self.topic_num = data["num"]
                self.topics_num = sample(range(1, self.topic_num + 1), self.topic_num)
                self.a = False
            self.topics = data[str(self.topics_num[self.topics_num_id])]
            self.topics_num_id += 1
            self.if_topic_show = True

    def compute_start(self):
        if self.if_win:
            if self.if_ok:
                if self.topic_errors > self.cut_of_line:
                    self.statr_num = 2
                elif self.topic_errors > self.cut_of_line2:
                    self.statr_num = 1
                else:
                    self.statr_num = 3
            else:
                if self.topic_errors == 0:
                    self.statr_num = 3
                elif self.topic_errors > self.topics_nums * 0.4:
                    self.statr_num = 2
                else:
                    self.statr_num = 1
