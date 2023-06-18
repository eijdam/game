import pygame as pg
from settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
   
    def draw(self):
        if not pg.display.get_init() or not pg.display.get_active():
            return
        self.draw_background()
        self.render_game_objects()

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def draw_background(self):
        
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))
        pg.draw.rect(self.screen, (255, 255, 255), (0, 0, 1920, 540))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/black_brick_wall.png'),
            2: self.get_texture('resources/textures/blacker_brick_wall.png'),
            3: self.get_texture('resources/textures/oblue_wall.png'),
            4: self.get_texture('resources/textures/dvierka.png'),  #ciel
            5: self.get_texture('resources/textures/dblue_wall.png'),
            6: self.get_texture('resources/textures/tblue_wall.png'),
        }
