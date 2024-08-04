import random
import enemy
import pygame
pygame.init()

class Spawner():
    def __init__(self, respawn_points, enemies, game_world):
        self.time = 0
        self.respawn = respawn_points
        self.respawn_point = 0
        self.enemy_number = 0
        self.world = game_world
        self.enemies = enemies
        self.max_enemies = len(enemies)

    def update(self, time_wait, players=1):
        count_of_enemies = len(self.world.enemies)
        if count_of_enemies < 4 and self.time == 0:
            self.time = 0.01
        if self.time > 0:
            self.time += 1
        if self.time >= time_wait:
            self.spawn()
            self.time = 0
        if self.enemy_number >= self.max_enemies and len(self.world.enemies) == 0:
            self.world.win()

    def spawn(self):
        if self.enemy_number < self.max_enemies:
            self.world.enemies.add(enemy.Enemy(
                self.respawn[self.respawn_point],
                random.randint(0, 3),
                "#" + str(self.enemy_number),
                self.world,
                tanktype=self.enemies[self.enemy_number],
                have_bonus=self.enemy_number in self.world.enemies_with_bonuses
                )
            )
            self.enemy_number += 1
            if self.respawn_point == 0:
                self.respawn_point = 2
            elif self.respawn_point == 1:
                self.respawn_point = 0
            elif self.respawn_point == 2:
                self.respawn_point = 1
