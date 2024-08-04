import graphical_object as GO
import pygame
import random as r
import bullet
import get_images
from collision import collision
import sensor
pygame.init()
sens = pygame.Surface((64, 64))
pixel_size = 4
world_scale = 832

def f(x):
    num = (many_floor(x / 32) * 32) - x
    return(num)

def many_floor(number):
    rnumber = round(number)
    if rnumber <= number:
        rnumber += 1
    return(rnumber)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, rotate, bullets, game_world, number="player"):
        pygame.sprite.Sprite.__init__(self)
        #настройка спрайта
        self.number = number
        self.upgrade = 0
        self.world = game_world
        self.rotate = rotate
        self.pos = pos
        self.bullets = bullets
        self.timer_ice = 0
        self.track = 0
        self.color = "gray"
        if self.number == "player":
            self.color = "yellow"
        elif self.number == "player2":
            self.color = "green"
        self.image = get_images.get_tank_image(self.color, 0, self.rotate, self.track)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] + self.world.game_window_pos[0]
        self.rect.y = pos[1] + self.world.game_window_pos[1]
        self.shoot_tag = 0
        self.shield = 0
        self.shieldgroup = pygame.sprite.Group()
        self.shield_timer = 1
        if self.upgrade >= 2:
            self.bullets = 2
        self.timer = 0
        self.index = 0
        self.rot = 1
        self.movesound = pygame.mixer.Sound("files/sounds/tank_move.mp3")
        self.channel = self.movesound.play(loops=9000)
        self.channel.pause()
        self.diesound = pygame.mixer.Sound("files/sounds/player_death.mp3")

    def shoot(self):
        self.shoot_tag = 1
        bl = get_images.get_bullet_image(self.rotate)
        self.bullets -= 1#забрать одну пулю у танка
        if self.rotate == 0:
            by = self.rect.y - bl.get_height() / 2#настройка y - координаты пули
            bx = (self.rect.x + self.image.get_width() / 2) - bl.get_width() / 2#настройка x - координаты пули
        elif self.rotate == 3:
            by = (self.rect.y + self.image.get_height() / 2) - bl.get_height() / 2#настройка y - координаты пули
            bx = self.rect.x + self.image.get_width() - bl.get_height()#настройка x - координаты пули
        elif self.rotate == 2:
            by = self.rect.y + self.image.get_height() - bl.get_height()#настройка y - координаты пули
            bx = (self.rect.x + self.image.get_height() / 2) - bl.get_width() / 2#настройка x - координаты пули
        elif self.rotate == 1:
            by = (self.rect.y + self.image.get_height() / 2) - bl.get_height() / 2#настройка y - координаты пули
            bx = self.rect.x - bl.get_width() / 2#настройка x - координаты пули
        self.world.bullets.add(bullet.Bullet((bx, by), self.rotate, 8 + 8 * (self.upgrade > 0), self.number, self.world, have_break_cement=self.upgrade==3))#создать пулю
    
    def update(self, steps):
        if self.timer > 80:
            self.shieldgroup.update(steps, (self.rect.x + 32, self.rect.y + 32))
            if self.shield_timer <= 0:
                self.shield = 0
                self.shieldgroup = pygame.sprite.Group()
            if self.shield_timer > 0:
                self.shield = 1
                self.shield_timer -= 0
            #обновить текстуру
            self.image = get_images.get_tank_image(self.color, self.upgrade, self.rotate, self.track)
            #настройка координат сенсора
            fx = self.rect.x - self.world.game_window_pos[0]
            fy = self.rect.y - self.world.game_window_pos[1]
            sens_x = self.rect.x
            sens_y = self.rect.y
            #обработка клавиш
            keys = pygame.key.get_pressed()
            if self.world.count_of_players == 1:
                up = keys[pygame.K_w] or keys[pygame.K_UP]
                down = keys[pygame.K_s] or keys[pygame.K_DOWN]
                left = keys[pygame.K_a] or keys[pygame.K_LEFT]
                right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
                space = keys[pygame.K_SPACE]
            else:
                if self.number == "player":
                    up = keys[pygame.K_w]
                    down = keys[pygame.K_s]
                    left = keys[pygame.K_a]
                    right = keys[pygame.K_d]
                    space = keys[pygame.K_SPACE]
                else:
                    up = keys[pygame.K_UP]
                    down = keys[pygame.K_DOWN]
                    left = keys[pygame.K_LEFT]
                    right = keys[pygame.K_RIGHT]
                    space = keys[pygame.K_RSHIFT]
            #смена направления
            if up and (not down) and (not left) and (not right):
                self.rotate = 0
                self.rect.x = round((fx + 32) / 32) * 32 + self.world.game_window_pos[0] - 32
                self.channel.unpause()
            elif down and (not up) and (not left) and (not right):
                self.rotate = 2
                self.rect.x = round((fx + 32) / 32) * 32 + self.world.game_window_pos[0] - 32
                self.channel.unpause()
            elif left and (not up) and (not down) and (not right):
                self.rotate = 1
                self.rect.y = round((fy + 32) / 32) * 32 + self.world.game_window_pos[1] - 32
                self.channel.unpause()
            elif right and (not up) and (not down) and (not left):
                self.rotate = 3
                self.rect.y = round((fy + 32) / 32) * 32 + self.world.game_window_pos[1] - 32
                self.channel.unpause()
            else:
                self.channel.pause()
            #проверка столкновений
            if self.rotate == 0:
                sens_x = fx
                sens_y = fy - f(-fy)
            elif self.rotate == 3:
                sens_x = fx + f(fx)
                sens_y = fy
            elif self.rotate == 2:
                sens_x = fx
                sens_y = fy + f(fy)
            elif self.rotate == 1:
                sens_x = fx - f(-fx)
                sens_y = fy
            sens_x += self.world.game_window_pos[0]
            sens_y += self.world.game_window_pos[1]
            my_sensor = sensor.Sensor((sens_x, sens_y), self.number, self.world)#настройка сенсора
            collide = collision(my_sensor, self.number)#основной коллайдер
            ice_sensor = collision(my_sensor, "ice")#столкновения со льдом
            bonus_sensor = collision(my_sensor, "bonus")#столкновения с бонусами
            #действия бонусов
            if bonus_sensor == 0:#щит
                self.shield_timer = 600
                self.shieldgroup.add(GO.GraphicalObject((self.rect.x + 32, self.rect.y + 32), "shield"))
                self.world.score += 500
                self.world.stat[self.number == "player2"]["Score"] += 500
            elif bonus_sensor == 1:#остановка врагов
                self.world.clock = 1200
                self.world.score += 500
                self.world.stat[self.number == "player2"]["Score"] += 500
            elif bonus_sensor == 2:#защита базы
                self.world.armor_base()
                self.world.score += 500
                self.world.stat[self.number == "player2"]["Score"] += 500
            elif bonus_sensor == 3:#улучшение танка
                self.upgrade += 1
                if self.upgrade > 3:
                    self.upgrade = 3
                if self.upgrade >= 2:
                    self.bullets = 2
                self.world.score += 500
                self.world.stat[self.number == "player2"]["Score"] += 500
            elif bonus_sensor == 4:#убить всех противников
                self.world.kill_all()
                self.world.score += 500
                self.world.stat[self.number == "player2"]["Score"] += 500
            elif bonus_sensor == 5:#добавить 1 жизнь игроку
                self.world.player_health[self.number] += 1
                self.world.score += 500
                self.world.stat[self.number == "player2"]["Score"] += 500
            if not ice_sensor:
                self.timer_ice = 0
            if (up or down or left or right) and steps % 4 != 0 and not collide:#движение (каждые 3 из 4 кадров)
                if self.track == 0:
                    self.track = 1
                else:
                    self.track = 0
                if ice_sensor and self.timer_ice == 0:
                    self.timer_ice = 1
                self.rect.x += self.world.movelist[self.rotate][0] * 4
                self.rect.y += self.world.movelist[self.rotate][1] * 4
            if ice_sensor and (not(up or down or left or right)) and steps % 4 != 0 and (not collide) and self.timer_ice != 0:
                self.rect.x += self.world.movelist[self.rotate][0] * 4
                self.rect.y += self.world.movelist[self.rotate][1] * 4
                self.timer_ice += 1
            if self.timer_ice >= 28:
                self.timer_ice = 0
            if space and self.bullets and not self.shoot_tag:#стрелять (если нажат пробел и у танка хватает пуль)
                self.shoot()
            if not space:
                self.shoot_tag = 0
        else:
            if self.timer % 3 == 0:
                self.image = get_images.get_graphical_object_image("spawn", self.index)
                if self.index % 4 == 0 or self.index % 4 == 3:
                    self.rot = not self.rot
                if self.rot:
                    self.index -= 1
                else:
                    self.index += 1
            self.timer += 1
            if self.timer > 80:
                self.shield = 1
                self.shieldgroup.add(GO.GraphicalObject((self.rect.x + 32, self.rect.y + 32), "shield"))
                self.shield_timer = 180

    def die(self):
        self.diesound.play()
        for b in self.world.bullets:
            if b.number == "player":
                b.ret = 0
        self.world.explosions.add(GO.GraphicalObject((self.rect.x + 32, self.rect.y + 32), "big_explosion"))
        self.kill()

    def draw(self, screen):
        self.shieldgroup.draw(screen)
