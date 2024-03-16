# coding=gbk
from time import sleep
from random import sample
from threading import Thread
import pygame
import json
import sys


class QATwoPlayer:
    def __init__(self, clock, scene):
        self.screen = scene.screen
        self.scene = scene
        pygame.display.set_caption('Chemistry Q&A two player')
        self.clock = clock
        self.topics_num_left = sample([1, 2, 3, 4, 5], 5)
        self.topics_num_right = sample([1, 2, 3, 4, 5], 5)
        self.topics_num_left_id = 0
        self.topics_num_right_id = 0
        self.fraction = [0, 0]

        self.if_game_run = True
        self.if_topic_show = [False, False]
        self.if_set_topic = [False, False]
        self.if_good = [False, False]
        self.if_error = [False, False]
        self.if_ok = [False, False]

        self.Font = pygame.font.Font('Fonts/simsun.ttc', 18)
        pygame.mixer.music.load('Musics/musics.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

    def run_game(self):
        self.load_image()

        while self.if_game_run:
            self.update_screen()
            self.create_topic_left()
            self.create_topic_right()
            if self.if_ok[0] and self.if_ok[1]:
                pass

            self._check_event()
            pygame.display.update()
            self.clock.tick(60)

    def load_image(self):
        self.bg = pygame.image.load('image/bg_two_player.png')  # 800*600
        self.player1 = pygame.image.load('image/player1.png')  # 80*120
        self.player2 = pygame.image.load('image/player2.png')  # 80*120
        self.answer_box_tmp = pygame.image.load('image/AnswerBox.png')  # 400*300
        self.answer_box = pygame.transform.rotozoom(self.answer_box_tmp, 0, 0.7)  # 280*210
        self.button_pairs_tmp = pygame.image.load('image/button_pairs.png')  # 200*200
        self.button_pairs = pygame.transform.rotozoom(self.button_pairs_tmp, 0, 0.3)  # 60*60
        self.button_error_tmp = pygame.image.load('image/button_error.png')  # 200*200
        self.button_error = pygame.transform.rotozoom(self.button_error_tmp, 0, 0.3)  # 60*60
        self.good = pygame.image.load('image/good.png')  # 120*158
        self.error = pygame.image.load('image/error.png')  # 160*160
        self.win = pygame.image.load('image/win.png')

    def update_screen(self):
        self.screen.fill((135, 180, 255))
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.player1, (150, 440))
        self.screen.blit(self.player2, (560, 440))
        self.screen.blit(self.answer_box, (60, 30))
        self.screen.blit(self.answer_box, (460, 30))
        self.screen.blit(self.button_pairs, (50, 480))
        self.screen.blit(self.button_error, (275, 480))
        self.screen.blit(self.button_pairs, (450, 480))
        self.screen.blit(self.button_error, (675, 480))
        if self.if_good[0]:
            self.screen.blit(self.good, (150, 100))
        if self.if_good[1]:
            self.screen.blit(self.good, (550, 100))
        if self.if_error[0]:
            self.screen.blit(self.error, (150, 100))
        if self.if_error[1]:
            self.screen.blit(self.error, (550, 100))

    def _check_event(self):
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

    def check_moues(self, x, y):
        if not self.if_good[0] and not self.if_error[0]:
            if 50 < x < 110:
                if 480 < y < 540:
                    self.check_answer(0, 0)
                    t5 = Thread(target=self.wait, args='0')
                    t5.start()
            if 275 < x < 335:
                if 480 < y < 540:
                    self.check_answer(1, 0)
                    t6 = Thread(target=self.wait, args='0')
                    t6.start()
        if not self.if_good[1] and not self.if_error[1]:
            if 450 < x < 510:
                if 480 < y < 540:
                    self.check_answer(0, 1)
                    t7 = Thread(target=self.wait, args='1')
                    t7.start()
            if 675 < x < 735:
                if 480 < y < 540:
                    self.check_answer(1, 1)
                    t8 = Thread(target=self.wait, args='1')
                    t8.start()

    def create_topic_left(self):
        try:
            if not self.if_set_topic[0]:
                with open('topics.json', encoding='utf-8') as f:
                    data = json.load(f)
                self.topics_left = data[str(self.topics_num_left[self.topics_num_left_id])]
                self.topics_num_left_id += 1
                self.if_set_topic[0] = True
            topic = self.topics_left['topic']
            self.topic_if_left = self.topics_left['if']
            text_lines = topic.split('\n')
            text_surfaces = [self.Font.render(line, True, (0, 0, 0)) for line in text_lines]
            for i, line_surface in enumerate(text_surfaces):
                self.screen.blit(line_surface, (80, 60 + i * 40))
        except IndexError:
            print('越界')
            print(self.fraction[0])
            self.if_set_topic[0] = True
            self.if_ok[0] = True

    def create_topic_right(self):
        try:
            if not self.if_set_topic[1]:
                with open('topics.json', encoding='utf-8') as f:
                    data = json.load(f)
                self.topics_right = data[str(self.topics_num_right[self.topics_num_right_id])]
                self.topics_num_right_id += 1
                self.if_set_topic[1] = True
            topic = self.topics_right['topic']
            self.topic_if_right = self.topics_right['if']
            text_lines = topic.split('\n')
            text_surfaces = [self.Font.render(line, True, (0, 0, 0)) for line in text_lines]
            for i, line_surface in enumerate(text_surfaces):
                self.screen.blit(line_surface, (480, 60 + i * 40))
        except IndexError:
            print('越界')
            print(self.fraction[1])
            self.if_set_topic[1] = True
            self.if_ok[1] = True

    def check_answer(self, answer, position):
        if position == 0:  # left
            if answer == int(self.topic_if_left):
                self.fraction[0] += 1
                t1 = Thread(target=self.set_good, args='0')
                t1.start()
            else:
                t3 = Thread(target=self.set_error, args='0')
                t3.start()

        if position == 1:  # right
            if int(self.topic_if_right) == answer:
                self.fraction += 1
                t2 = Thread(target=self.set_good, args='1')
                t2.start()
            else:
                t4 = Thread(target=self.set_error, args='1')
                t4.start()

    def set_good(self, player_id):
        if int(player_id) == 0:
            self.if_good[0] = True
            time.sleep(3)
            self.if_good[0] = False
        if int(player_id) == 1:
            self.if_good[1] = True
            time.sleep(3)
            self.if_good[1] = False

    def set_error(self, player_id):
        if int(player_id) == 0:
            self.if_error[0] = True
            time.sleep(3)
            self.if_error[0] = False
        if int(player_id) == 1:
            self.if_error[1] = True
            time.sleep(3)
            self.if_error[1] = False

    def wait(self, player_id):
        time.sleep(3)
        self.if_set_topic[int(player_id)] = False
