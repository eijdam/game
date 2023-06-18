import pygame
import random
import cv2

import player
from player import *


class Win:
    def __init__(self):
        pygame.init()
        # dimenzie
        self.screen_width = 1920
        self.screen_height = 1080
        # vytvorenie
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        # load videa
        self.background_frames()
        # font a velkost YOU WIN
        self.font = pygame.font.Font(None, 72)
        # font a velkost tlacidla
        self.button_font = pygame.font.Font(None, 48)
        # pismena
        self.letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        # casovac a pismena
        self.letter_index = 0
        self.timer = 5
        self.interval = 1000
        self.update_indexes = []
        # vymenna pismen z originalnych na nahodne a potom spat
        self.last_letter_update_time = pygame.time.get_ticks()
        # staty premennych
        self.running = True
        self.frame_index = 0
        self.last_tick = pygame.time.get_ticks()
        self.cursor_radius = 10
        self.cursor_color = (255, 255, 255)
        self.cursor_alpha = 0
        self.player = player.Player(self)
        self.text = ""
        self.text_and_button_win()

    def background_frames(self):
        cap = cv2.VideoCapture('resources/videos/vhs.mp4')
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  # zle nacitane video som musel rotatenut
            frames.append(pygame.surfarray.make_surface(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        cap.release()
        self.background_frames = frames

    def text_and_button_win(self):
        self.text = "YOU WIN"
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = text_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - 100))
        self.text_surface = text_surface

        # SPAWN button
        button_text = "QUIT"
        button_surface = self.button_font.render(button_text, True, (255, 255, 255))
        self.button_rect = button_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 2 + 50))
        self.button_surface = button_surface

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    self.running = False

    def update_text_win(self):
        self.timer += pygame.time.get_ticks() - self.last_tick
        self.last_tick = pygame.time.get_ticks()

        if self.timer > self.interval:
            self.timer -= self.interval
            num_indexes_to_update = random.randint(1, 2)
            self.update_indexes = random.sample([i for i in range(len(self.text)) if self.text[i] != " "],
                                                num_indexes_to_update)

        if pygame.time.get_ticks() - self.last_letter_update_time > 2000:
            self.text = "YOU WIN"
            self.update_indexes = []
            self.last_letter_update_time = pygame.time.get_ticks()
        new_text = ""
        for i in range(len(self.text)):
            if i == self.text.index(" "):
                new_text += self.text[i]
            elif i in self.update_indexes:
                new_text += random.choice(self.letters)
            else:
                new_text += self.text[i]
        self.text = new_text
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))

    def update(self):
        self.update_text_win()

        self.letter_index = (self.letter_index + 1) % len(self.text)
        if self.background_frames:
            self.screen.blit(self.background_frames[self.frame_index], (0, 0))
            self.frame_index = (self.frame_index + 1) % len(self.background_frames)

        self.screen.blit(self.text_surface, self.text_rect)
        self.screen.blit(self.button_surface, self.button_rect)
        self.draw_cursor()
        pygame.display.flip()

    def draw_cursor(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.cursor = pygame.Surface((self.cursor_radius * 2, self.cursor_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.cursor, self.cursor_color + (self.cursor_alpha,), (self.cursor_radius, self.cursor_radius), self.cursor_radius)
        self.screen.blit(self.cursor, (self.mouse_pos[0] - self.cursor_radius, self.mouse_pos[1] - self.cursor_radius))
        pygame.draw.circle(self.screen, self.cursor_color, self.mouse_pos, self.cursor_radius, 0)

    def run_win(self):
        while self.running:
            self.events()
            self.update()

