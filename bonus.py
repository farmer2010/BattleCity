import get_images
import random
import pygame
import graphical_object as GO
pygame.init()

class Bonus(pygame.sprite.Sprite):
    def __init__(self, game_world):
        pygame.sprite.Sprite.__init__(self)
        self.world = game_world
        field = self.world.field
        i = True
        o = 0
        while i:
            o += 1
            blocks = ("ice", "tree", "air")
            pos = (random.randint(0, 24), random.randint(0, 24))
            pos2 = (pos[0] + 1, pos[1])
            pos3 = (pos[0], pos[1] + 1)
            pos4 = (pos[0] + 1, pos[1] + 1)
            if field[pos[0]][pos[1]].type in blocks or field[pos2[0]][pos2[1]].type in blocks or field[pos3[0]][pos3[1]].type in blocks or field[pos4[0]][pos4[1]].type in blocks:
                i = 0
            if o >= 50:
                i = 0
        self.pos = pos
        self.type = random.randint(0, 7)
        if self.type == 6: self.type = 3
        if self.type == 7: self.type = 4
        self.image = get_images.get_bonus_image(self.type)
        self.rect = self.image.get_rect()
        self.rect.x = self.world.game_window_pos[0] + pos[0] * 32
        self.rect.y = self.world.game_window_pos[1] + pos[1] * 32

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def die(self):
        self.world.explosions.add(GO.GraphicalObject((self.rect.x + 32, self.rect.y + 32), "score", mode=4))
        self.kill()
