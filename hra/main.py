import pygame as pg
import sys

from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from npc import *
from object_handler import *
from pathfinding import *
from menu import *
from win import *
from lose import *


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.new_game()
        self.npc = NPC(self)

    def new_game(self):
        self.map = Map(self)
        self.player = player.Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.pathfinding = PathFinding(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.draw()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        pg.display.flip()

    def draw(self):
        self.object_renderer.draw()
        self.player.show_health()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            if self.player.lose or self.player.win:
                break


if __name__ == '__main__':
    menu = Menu()
    menu.run()
