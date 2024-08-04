import get_images
import pygame
pygame.init()

class Symbol(pygame.sprite.Sprite):
    def __init__(self, sftype, pos, color_changes=[]):
        pygame.sprite.Sprite.__init__(self)
        self.W = 1920
        self.H = 1080
        self.game_window_pos = [
            self.W / 2 - 416,
            self.H / 2 - 416
            ]
        self.type = sftype
        self.image = get_images.get_symbol_image(sftype, color_changes=color_changes)
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0] * 32 + self.game_window_pos[0]
        self.rect.y = self.pos[1] * 32 + self.game_window_pos[1]
