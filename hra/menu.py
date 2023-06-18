import datetime as dt
from PIL import Image, ImageSequence
from main import *
import pygame as pg

class Menu:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1920, 1080), pg.RESIZABLE)
        pg.display.set_caption("Game")
        self.font1 = pg.font.Font("resources/fonts/vhs.ttf", 50)
        pg.mouse.set_visible(False)
        self.vhs_text = self.font1.render("VHS", True, (255, 255, 255))

        self.cursor_radius = 10
        self.cursor_color = (255, 255, 255)
        self.cursor_alpha = 0

        self.load_assets()

        self.play_button = self.Button(920, 500, "PLAY", True)
        self.quit_button = self.Button(920, 570, "QUIT", True)

        self.counter = 1
        self.clock = pg.time.Clock()

        # Load and play audio file
        self.menu_music = pg.mixer.Sound('resources/sound/soundtrack.mp3')
        self.menu_music.play(-1)

    def load_assets(self):
        self.frames = self.loadGIF("resources/videos/VHSvideo.gif")
        self.background = self.GIFrame(960, 540, self.frames, 0.1)

    def loadGIF(self, filename):
        pilImage = Image.open(filename)
        frames = []
        for frame in ImageSequence.Iterator(pilImage):
            frame = frame.convert('RGBA')
            frame = frame.resize((1920, 1080), resample=Image.BOX)
            pygameImage = pg.image.fromstring(
                frame.tobytes(), frame.size, frame.mode).convert_alpha()
            frames.append(pygameImage)
        return frames

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            date_and_time = dt.datetime.now()
            keys = pg.key.get_pressed()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    self.screen.fill((0, 0, 0))

            self.background.update()
            self.background.draw()

            self.play_button.draw()
            self.quit_button.draw()

            if self.counter >= 59 and self.counter < 120:
                self.screen.blit(self.vhs_text, (1780, 30))
            elif self.counter == 121:
                self.counter = 1

            date_time_string = date_and_time.strftime("%Y-%m-%d %H:%M:%S")
            datetime_text = self.font1.render(date_time_string, True, (255, 255, 255))
            self.screen.blit(datetime_text, (20, 1020))

            if self.play_button.check_click():
                self.menu_music.stop()

                game = Game()
                game.run()
                running = False

            if self.quit_button.check_click():
                running = False

            if keys[pg.K_ESCAPE]:
                running = False

            self.draw_cursor()

            self.counter += 1
            pg.display.update()

        pg.quit()

    def draw_cursor(self):
        mouse_pos = pg.mouse.get_pos()
        cursor = pg.Surface((self.cursor_radius * 2, self.cursor_radius * 2), pg.SRCALPHA)
        pg.draw.circle(cursor, self.cursor_color + (self.cursor_alpha,), (self.cursor_radius, self.cursor_radius), self.cursor_radius)
        self.screen.blit(cursor, (mouse_pos[0] - self.cursor_radius, mouse_pos[1] - self.cursor_radius))
        pg.draw.circle(self.screen, self.cursor_color, mouse_pos, self.cursor_radius, 0)

    class Button:
        def __init__(self, x_pos, y_pos, text, enabled):
            self.text = text
            self.x_pos = x_pos
            self.y_pos = y_pos
            self.enabled = enabled
            self.font1 = pg.font.Font("resources/fonts/vhs.ttf", 50)
            font1 = self.font1
            self.screen = pg.display.set_mode((1920, 1080), pg.RESIZABLE)


        def draw(self):
            button_text = self.font1.render(self.text, True, (255, 255, 255))
            self.screen.blit(button_text, (self.x_pos, self.y_pos))

        def check_click(self):
            mouse_pos = pg.mouse.get_pos()
            left_click = pg.mouse.get_pressed()[0]
            button_rect = pg.rect.Rect((self.x_pos, self.y_pos), (300, 40))
            if left_click and button_rect.collidepoint(mouse_pos):
                return True
            return False

    class GIFrame(pg.sprite.Sprite):
        def __init__(self, x, y, frames, animation_speed):
            super().__init__()
            self.frames = frames
            self.image_index = 0
            self.image = self.frames[self.image_index]
            self.rect = self.image.get_rect(center=(x, y))
            self.animation_speed = animation_speed
            self.last_update_time = pg.time.get_ticks()
            self.screen = pg.display.set_mode((1920, 1080), pg.RESIZABLE)

        def update(self):
            current_time = pg.time.get_ticks()
            if current_time - self.last_update_time > self.animation_speed * 1000:
                self.image_index = (self.image_index + 1) % len(self.frames)
                self.image = self.frames[self.image_index]
                self.last_update_time = current_time

        def draw(self):
            self.screen.blit(self.image, self.rect.topleft)
