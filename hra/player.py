import pygame as pg
pg.mixer.init()

from settings import *
from map import *
from win import *
from object_renderer import *
import math
from win import *
from lose import *


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.health = 2
        self.win = False
        self.lose = False


    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        num_key_pressed = -1
        if keys[pg.K_w]:
            num_key_pressed += 1
            dx += speed_cos
            dy += speed_sin
            self.check_win()
        if keys[pg.K_s]:
            num_key_pressed += 1
            dx += -speed_cos
            dy += -speed_sin
            self.check_win()
        if keys[pg.K_a]:
            num_key_pressed += 1
            dx += speed_sin
            dy += -speed_cos
            self.check_win()
        if keys[pg.K_d]:
            num_key_pressed += 1
            dx += -speed_sin
            dy += speed_cos
            self.check_win()

        self.check_wall_collision(dx, dy)
        self.angle %= math.tau

    def show_health(self):
        if self.health >= 1:
            pg.draw.rect(self.game.screen, 'red', (20, 1000, 100, 30))
            if self.health == 2:
                pg.draw.rect(self.game.screen, 'red', (140, 1000, 100, 30))

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy
        
    def check_door_collision(self):
        tile_value = self.game.map.world_map[int(self.x)][int(self.y)]
        if tile_value == 4:
            self.game.object_renderer.win()  # Call the win() method in ObjectRenderer

    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                    (self.x * 100 + WIDTH * math.cos(self.angle),
                     self.y * 100 + WIDTH * math. sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        pg.init()
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        self.movement()
        self.mouse_control()

    def stop_npc_sounds(self):
        if self.game.npc:
            self.game.npc.stop_sounds()


    def check_defeat(self):
        if self.health < 1:
            self.stop_npc_sounds()  #stopnutie zvukov
            self.lose = True
            lose = Lose()
            lose.run_lose()
            self.game.npc.stop_sounds()

    def check_win(self):
        if self.x >= 13.80 and self.x <= 14 and self.y >= 23.1 and self.y <= 24:
            self.stop_npc_sounds()  #stopnutie zvukov
            self.win = True
            win = Win()
            win.run_win()
            self.game.npc.stop_sounds()

    def get_damage(self, damage):
        self.health -= damage
        self.check_defeat()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
