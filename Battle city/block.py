import pygame
import get_images
pygame.init()

class Block(pygame.sprite.Sprite):
    def __init__(self, pos, block_type, game_world, damage="1111", basetype="00", is_break=0):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.world = game_world
        self.type = block_type
        if block_type == "cement":
            self.image = get_images.get_block_image(1, 0)
        elif block_type == "brick":
            self.damage = damage
            self.image = get_images.get_break_block_image(self.damage)
        elif block_type == "trees":
            self.image = get_images.get_block_image(1, 1)
        elif block_type == "water":
            self.image = get_images.get_block_image(2, 1)
        elif block_type == "ice":
            self.image = get_images.get_block_image(1, 2)
        elif block_type == "air":
            self.image = pygame.Surface((32, 32))
        elif block_type == "base":
            self.image = get_images.get_base_image(basetype, is_break)
            self.basetype = basetype
            self.is_break = is_break
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * 32 + self.world.game_window_pos[0]
        self.rect.y = pos[1] * 32 + self.world.game_window_pos[1]
        self.time = 1

    def update(self):
        if self.type == "brick":
            if self.damage == "0000":
                self.type = "air"
        elif self.type == "base":
            if self.is_break == 1:
                self.world.game_over()
                if self.basetype == "00":
                    try:
                        self.world.field[self.pos[0] + 1][self.pos[1]].is_break = 1
                        self.world.field[self.pos[0] + 1][self.pos[1]].change_image()
                    finally:
                        try:
                            self.world.field[self.pos[0]][self.pos[1] + 1].is_break = 1
                            self.world.field[self.pos[0]][self.pos[1] + 1].change_image()
                        finally:
                            try:
                                self.world.field[self.pos[0] + 1][self.pos[1] + 1].is_break = 1
                                self.world.field[self.pos[0] + 1][self.pos[1] + 1].change_image()
                            except:
                                a = 1#pass
                elif self.basetype == "10":
                    try:
                        self.world.field[self.pos[0] - 1][self.pos[1]].is_break = 1
                        self.world.field[self.pos[0] - 1][self.pos[1]].change_image()
                    finally:
                        try:
                            self.world.field[self.pos[0]][self.pos[1] + 1].is_break = 1
                            self.world.field[self.pos[0]][self.pos[1] + 1].change_image()
                        finally:
                            try:
                                self.world.field[self.pos[0] - 1][self.pos[1] + 1].is_break = 1
                                self.world.field[self.pos[0] - 1][self.pos[1] + 1].change_image()
                            except:
                                a = 1#pass
                elif self.basetype == "01":
                    try:
                        self.world.field[self.pos[0]][self.pos[1] - 1].is_break = 1
                        self.world.field[self.pos[0]][self.pos[1] - 1].change_image()
                    finally:
                        try:
                            self.world.field[self.pos[0] + 1][self.pos[1] - 1].is_break = 1
                            self.world.field[self.pos[0] + 1][self.pos[1] - 1].change_image()
                        finally:
                            try:
                                self.world.field[self.pos[0] + 1][self.pos[1]].is_break = 1
                                self.world.field[self.pos[0] + 1][self.pos[1]].change_image()
                            except:
                                a = 1#pass
                elif self.basetype == "11":
                    try:
                        self.world.field[self.pos[0]][self.pos[1] - 1].is_break = 1
                        self.world.field[self.pos[0]][self.pos[1] - 1].change_image()
                    finally:
                        try:
                            self.world.field[self.pos[0] - 1][self.pos[1] - 1].is_break = 1
                            self.world.field[self.pos[0] - 1][self.pos[1] - 1].change_image()
                        finally:
                            try:
                                self.world.field[self.pos[0] - 1][self.pos[1]].is_break = 1
                                self.world.field[self.pos[0] - 1][self.pos[1]].change_image()
                            except:
                                a = 1#pass

    def draw(self, screen):
        if self.type == "water":
            self.time += 1
            self.time %= 60
            if self.time % 30 == 0:
                self.image = get_images.get_block_image(2, 1 + self.time // 30)
        if self.type != "air":
            screen.blit(self.image, self.rect)

    def change_image(self):
        if self.type == "cement":
            self.image = get_images.get_block_image(1, 0)
        elif self.type == "brick":
            self.image = get_images.get_break_block_image(self.damage)
        elif self.type == "trees":
            self.image = get_images.get_block_image(1, 1)
        elif self.type == "water":
            self.image = get_images.get_block_image(2, 1)
        elif self.type == "ice":
            self.image = get_images.get_block_image(1, 2)
        elif self.type == "air":
            self.image = pygame.Surface((32, 32))
        elif self.type == "base":
            self.image = get_images.get_base_image(self.basetype, self.is_break)
