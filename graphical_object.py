import get_images
import pygame
pygame.init()

class GraphicalObject(pygame.sprite.Sprite):
    def __init__(self, pos, sftype, mode=0, display_size=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.index = mode
        self.pos = pos
        self.type = sftype
        if self.type != "game over":
            self.image = get_images.get_graphical_object_image(self.type, self.index)
        else:
            self.image = get_images.get_graphical_object_image("game over", 0, size=4)
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]
        #print(self.pos, self.type)
        self.time = 120
        self.display_size = display_size
        if sftype == "game over":
            self.image = get_images.get_graphical_object_image(sftype, 0, 4)

    def update(self, steps, newpos=(1000, 300)):
        if "explosion" in self.type:
            if self.index > 4:
                i = 4
            else:
                i = self.index
            if self.type == "big_explosion" and self.index >= 3:
                self.image = get_images.get_graphical_object_image("big_explosion", i - 3)
            else:
                self.image = get_images.get_graphical_object_image("explosion", i)
            self.rect = self.image.get_rect()
            self.rect.centerx = self.pos[0]
            self.rect.centery = self.pos[1]
            if not steps % 5:
                self.index += 1
            if self.index >= 4 and self.type == "big_explosion":
                self.kill()
            elif self.index > 2 and self.type == "explosion":
                self.kill()
        elif self.type == "shield":
            if not (steps % 2):
                self.index = not self.index
                self.image = get_images.get_graphical_object_image(self.type, self.index)
                self.rect = self.image.get_rect()
            self.pos = newpos
            self.rect.centerx = self.pos[0]
            self.rect.centery = self.pos[1]
        elif self.type == "score":
            self.time -= 1
            if self.time <= 0:
                self.kill()
        elif self.type == "game over":
            if self.pos[1] >= self.display_size[1] / 2:
                self.pos = (self.pos[0], self.pos[1] - 4)
            self.rect.centerx = self.pos[0]
            self.rect.centery = self.pos[1]
