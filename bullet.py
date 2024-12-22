import graphical_object as GO
import pygame
import get_images
from collision import collision
pygame.init()

def change_string(string, elem, number_elem):
    string = string[:number_elem] + str(elem) + string[number_elem + 1:]
    return(string)

def break_brick(damage, rotate):
    """
    damage = "
        1(0, 0)#0
        1(1, 0)#1
        1(0, 1)#2
        1(1, 1)#3
        "
    """
    if rotate == 0:
        if damage[2] == "0" and damage[3] == "0":
            damage = change_string(damage, 0, 0)
            damage = change_string(damage, 0, 1)
        else:
            damage = change_string(damage, 0, 2)
            damage = change_string(damage, 0, 3)
    elif rotate == 1:
        if damage[1] == "0" and damage[3] == "0":
            damage = change_string(damage, 0, 0)
            damage = change_string(damage, 0, 2)
        else:
            damage = change_string(damage, 0, 1)
            damage = change_string(damage, 0, 3)
    elif rotate == 2:
        if damage[0] == "0" and damage[1] == "0":
            damage = change_string(damage, 0, 2)
            damage = change_string(damage, 0, 3)
        else:
            damage = change_string(damage, 0, 0)
            damage = change_string(damage, 0, 1)
    elif rotate == 3:
        if damage[0] == "0" and damage[2] == "0":
            damage = change_string(damage, 0, 1)
            damage = change_string(damage, 0, 3)
        else:
            damage = change_string(damage, 0, 0)
            damage = change_string(damage, 0, 2)
    return(damage)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, rotate, speed, tank_type, game_world, have_break_cement=0):
        pygame.sprite.Sprite.__init__(self)
        #настройка спрайта
        self.world = game_world
        self.pos = pos
        self.rotate = rotate
        self.speed = speed
        self.image = get_images.get_bullet_image(self.rotate)
        self.image.fill((0, 255, 0))
        self.number = tank_type
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.have_break_cement = have_break_cement
        self.ret = 1#возвращать ли пулю игроку
        if "player" in self.number:
            s = pygame.mixer.Sound("files/sounds/bullet_shoot.mp3")
            s.play()

    def update(self):
        #сдвиг
        self.image = get_images.get_bullet_image(self.rotate)
        self.rect.x += self.world.movelist[self.rotate][0] * self.speed
        self.rect.y += self.world.movelist[self.rotate][1] * self.speed
        collide_list = collision(self, "bullet")
        collide = collide_list[0]
        if collide:
            if collide_list[2] != []:#уничтожение блоков
                for b in collide_list[2]:
                    if b.type == "cement":
                        if self.have_break_cement:
                            b.type = "air"
                            b.change_image()
                            if "player" in self.number:
                                sound = pygame.mixer.Sound("files/sounds/bullet_hit_bricks.mp3")
                                sound.play()
                        else:
                            if "player" in self.number:
                                sound = pygame.mixer.Sound("files/sounds/bullet_hit_cement.mp3")
                                sound.play()
                    elif b.type == "brick":
                        if "player" in self.number:
                            sound = pygame.mixer.Sound("files/sounds/bullet_hit_bricks.mp3")
                            sound.play()
                        if self.have_break_cement:
                            b.type = "air"
                            b.change_image()
                        else:
                            block_damage = b.damage
                            block_damage = break_brick(block_damage, self.rotate)
                            b.damage = block_damage
                            b.change_image()
                            b.update()
                    elif b.type == "base":
                        sound = pygame.mixer.Sound("files/sounds/player_death.mp3")
                        sound.play()
                        b.is_break = 1
                        b.change_image()
                        b.update()
            if not "player" in self.number:#если пуля выпущена врагом
                for e in self.world.enemies:
                    if e.number == self.number:
                        e.bullets += 1
                if collide_list[1] != None and "player" in collide_list[1].number:
                    for p in self.world.players:
                        if not p.shield and p.number == collide_list[1].number:
                            self.world.killed_players.append(p.number)
                            p.die()
            else:#если пуля выпущена игроком
                for p in self.world.players:
                    if self.ret and p.number == self.number:
                        p.bullets += 1
                if str(type(collide_list[1])) == "<class 'enemy.Enemy'>":
                    for e in self.world.enemies:
                        if e.number == collide_list[1].number:
                            e.die()
                            self.world.stat[self.number == "player2"]["Enemies"][e.type] += 1
                            self.world.stat[self.number == "player2"]["Score"] += (e.type + 1) * 100
            if str(type(collide_list[1])) != "<class 'bullet.Bullet'>":
                self.world.explosions.add(GO.GraphicalObject((self.rect.x + 10, self.rect.y + 10), "explosion"))
            self.kill()
