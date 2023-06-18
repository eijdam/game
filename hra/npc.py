import pygame
from sprite_object import *
from random import randint, random
import time

class NPC(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/npc/kotlik.jpg', pos=(10.5, 5.5), scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.idle_images = self.get_images(self.path)
        self.walk_images = self.get_images(self.path)

        self.attack_dist = randint(1, 3)
        self.speed = 0.035
        self.size = 10
        self.health = 100
        self.attack_damage = 1
        self.accuracy = 0.80
        self.alive = True
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False
        self.start_time = 0
        self.last_attack_time = time.time()
        self.attack_cooldown = 10
        self.movement_sound = pygame.mixer.Sound('resources/sound/footstep.mp3')
        self.movement_sound_playing = False
        self.attack_sound = pygame.mixer.Sound('resources/sound/monster.mp3')
        self.attack_sound_playing = False
        self.game = game
        self.first_encounter = True
        self.jumpscare_sound = pygame.mixer.Sound('resources/sound/jumpscare.mp3')
        self.jumpscare_played = False

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            if self.ray_cast_value:
                self.player_search_trigger = True
                if self.dist < self.attack_dist:
                    self.animate(self.walk_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()
            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)

            # Check if it's the first encounter and play jumpscare sound
            if self.first_encounter and self.ray_cast_value and not self.jumpscare_played:
                self.play_jumpscare_sound()
                self.jumpscare_played = True

    def stop_sounds(self):
        pygame.mixer.stop()
        self.movement_sound_playing = False
        self.attack_sound_playing = False

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

            # Play the movement sound only if it's not already playing and attack sound is not playing
            if (dx != 0 or dy != 0) and not self.movement_sound_playing and not self.attack_sound_playing:
                self.movement_sound.play(-1)
                self.movement_sound_playing = True
        else:
            if self.movement_sound_playing:
                self.movement_sound.stop()
                self.movement_sound_playing = False

    def attack(self):
        current_time = time.time()
        time_since_last_attack = current_time - self.last_attack_time

        if time_since_last_attack >= self.attack_cooldown:
            r = random()
            if r < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

                # Play the attack sound only if it's not already playing
                if not self.attack_sound_playing:
                    self.attack_sound.play()
                    self.attack_sound_playing = True
            self.last_attack_time = current_time

            # Stop the movement sound after attack
            if self.movement_sound_playing:
                self.movement_sound.stop()
                self.movement_sound_playing = False

            # Stop the attack sound after playing it once
            if self.attack_sound_playing:
                self.attack_sound_playing = False

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False

    def play_jumpscare_sound(self):
        self.jumpscare_sound.play()

    def draw_ray_cast(self):
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_player_npc():
            pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
                         (100 * self.x, 100 * self.y), 2)

class MarosKotlik(NPC):
    def __init__(self, game, path='resources/sprites/npc/kotlik.jpg', pos=(10.5, 6.5), scale=0.7, shift=0.27, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 0.03
        self.attack_damage = 1
        self.speed = 0.035
        self.accuracy = 0.80
