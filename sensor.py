import block
import pygame
pygame.init()

class Sensor(pygame.sprite.Sprite):#сенсор
    def __init__(self, pos, number, game_world):
        pygame.sprite.Sprite.__init__(self)
        self.number = number
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.world = game_world
