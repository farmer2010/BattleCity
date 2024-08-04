import graphical_object as GO
import pygame
import get_images
from collision import collision
pygame.init()

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
            if not "player" in self.number:
                for z in self.world.enemies:
                    if z.number == self.number:
                        z.bullets += 1
                    if collide_list[1] == "player" or collide_list[1] == "player2":
                        for f in self.world.players:
                            if not f.shield and f.number == collide_list[1]:
                                self.world.killed_players.append(f.number)
                                f.die()
            else:
                for f in self.world.players:
                    if self.ret and f.number == self.number:
                        f.bullets += 1
                for v in self.world.enemies:
                    if v.number == collide_list[1]:
                        v.die()
                        self.world.stat[self.number == "player2"]["Enemies"][v.type] += 1
                        self.world.stat[self.number == "player2"]["Score"] += (v.type + 1) * 100
            self.world.explosions.add(GO.GraphicalObject((self.rect.x + 10, self.rect.y + 10), "explosion"))
            self.kill()
