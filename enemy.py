import graphical_object as GO
import bonus
import pygame
import random as r
import bullet
import get_images
from collision import collision
import sensor
pygame.init()

def f(x):
    num = (many_floor(x / 32) * 32) - x
    return(num)

def many_floor(number):
    rnumber = round(number)
    if rnumber <= number:
        rnumber += 1
    return(rnumber)

def change_rotate(stage):#сменить направление на случайное
    if stage == 0:
        return(r.randint(0, 3))

def cmd_change_rotate(rotate):#повернуть
    if r.randint(0, 1):#с шансом 1/2 сменить направление на случайное
        return(change_rotate(0))
    else:#иначе
        if r.randint(0, 1):#с шансом 1/2 повернуть по часовой стрелке
            rotate += 1
        else:#иначе повернуть против часовой стрелки
            rotate -= 1
        return(rotate % 4)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, rotate, number, game_world, tanktype=0, have_bonus=0):
        pygame.sprite.Sprite.__init__(self)
        self.type = tanktype
        self.have_bonus = have_bonus
        self.world = game_world
        self.track = 0
        self.pos = pos
        self.rotate = rotate
        self.number = number
        self.bullets = 1
        self.invisible = True
        if self.type == 1:
            self.speed = 1
        else:
            self.speed = 2
        if self.type == 3:
            self.health = 4
        else:
            self.health = 1
        self.timer = 0
        self.index = 0
        self.rot = 1
        self.image = get_images.get_graphical_object_image("spawn", self.index)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] + self.world.game_window_pos[0]
        self.rect.y = pos[1] + self.world.game_window_pos[1]
        self.movesound = pygame.mixer.Sound("files/sounds/tank_move.mp3")
        self.diesound = pygame.mixer.Sound("files/sounds/enemy_death.mp3")
        self.bonussound = pygame.mixer.Sound("files/sounds/bullet_hit_bonustank.mp3")
        self.armorsound = pygame.mixer.Sound("files/sounds/bullet_hit_armortank.mp3")
        if self.have_bonus == 1:
            for x in self.world.bonus:
                x.kill()

    def shoot(self):
        if self.bullets != 0:
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
            self.world.bullets.add(bullet.Bullet((bx, by), self.rotate, 8 + 8 * (self.type == 2), self.number, self.world))#создать пулю

    def die(self, i="standart"):
        if i == "standart":
            if self.have_bonus == 1:
                self.bonussound.play()
                self.have_bonus = 0
                self.world.bonus.add(bonus.Bonus(self.world))
            self.health -= 1
            if self.health <= 0:
                self.world.explosions.add(GO.GraphicalObject((self.rect.x + 32, self.rect.y + 32), "score", mode=self.type))
                self.world.explosions.add(GO.GraphicalObject((self.rect.x + 32, self.rect.y + 32), "big_explosion"))
                self.world.score += (self.type + 1) * 100
                self.kill()
                self.diesound.play()
            else:
                self.armorsound.play()
        else:
            self.world.explosions.add(GO.GraphicalObject((self.rect.x + 32, self.rect.y + 32), "big_explosion"))
            self.world.score += (self.type + 1) * 100
            self.diesound.play()
            self.kill()

    def update(self, steps, is_update):
        if self.timer > 80:
            if self.have_bonus and (steps // 10) % 2:
                color = "purple"
            elif not self.have_bonus:
                if self.type == 3:
                    if self.health == 4:
                        if steps % 2 == 0:
                            color = "green"
                        else:
                            color = "gray"
                    elif self.health == 3:
                        if steps % 2 == 0:
                            color = "yellow"
                        else:
                            color = "gray"
                    elif self.health == 2:
                        if steps % 2 == 0:
                            color = "yellow"
                        else:
                            color = "green"
                    elif self.health == 1:
                        color = "gray"
                else:
                    color = "gray"
            else:
                color = "gray"
            self.image = get_images.get_tank_image(color, 4 + self.type, self.rotate, self.track)

            if not is_update:
                W = self.world.W
                H = self.world.H
                world_scale = 832
                collide = False
                fx = self.rect.x - self.world.game_window_pos[0]
                fy = self.rect.y - self.world.game_window_pos[1]
                sens_x = 0
                sens_y = 0

                #настройка сенсора
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
                my_sensor = sensor.Sensor((sens_x, sens_y), self.number, self.world)
                collidelist = collision(my_sensor, "enemy")
                
                if self.invisible:
                    collide = collidelist[0]
                else:
                    collide = collidelist[0] or collidelist[1]
                if self.invisible and not collidelist[1]:
                    self.invisible = False
                if steps % self.speed == 0:
                    if self.track == 0:
                        self.track = 1
                    else:
                        self.track = 0
                    self.rect.x += self.world.movelist[self.rotate][0] * 4
                    self.rect.y += self.world.movelist[self.rotate][1] * 4
                    if collide:
                        self.rect.x += self.world.movelist[(self.rotate + 2) % 4][0] * 4
                        self.rect.y += self.world.movelist[(self.rotate + 2) % 4][1] * 4
                
                pos = [self.rect.x - self.world.game_window_pos[0], self.rect.y - self.world.game_window_pos[1]]
                
                if pos[0] % 32 == 0 and pos[1] % 32 == 0 and r.randint(1, 16) == 1:
                    self.rotate = change_rotate(0)
                elif collide and r.randint(1, 4) == 1:
                    if pos[0] % 32 != 0 or pos[1] % 32 != 0:
                        self.rotate += 2
                        self.rotate = self.rotate % 4
                    else:
                        self.rotate = cmd_change_rotate(self.rotate)
                #стрельба
                if r.randint(1, 32) == 1:
                    self.shoot()
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
