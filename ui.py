from symbol import Symbol as smb
import get_images
import world
import pygame
import json
import block
pygame.init()

tanks = pygame.image.load("files/images/tanks.png")
stage = pygame.Surface((40, 8))
stage.blit(tanks, (-328, -176))
stage = pygame.transform.scale(stage, (160, 32))

def get_number(num, size=32):
    img = pygame.Surface((8, 8))
    imgx = 328
    imgy = 184
    imgx += 8 * (num % 5)
    imgy += 8 * (num > 4)
    img.blit(tanks, (-imgx, -imgy))
    img = pygame.transform.scale(img, (size, size))
    return(img)

'''
0 - 9 -- 0 - 9
10 - _
11 - SPACE
12 - copyright
13 - ,
22 - A
23 - B
24 - C
25 - D
26 - E
27 - F
28 - G
29 - H
30 - I
31 - J
32 - K
33 - L
34 - M
35 - N
36 - 0
37 - P
38 - Q
39 - R
40 - S
41 - T
42 - U
43 - V
44 - W
45 - X
46 - Y
47 - Z
48 - "-"
'''

def add_symbols(symbols):
    symbols.add(smb(30, (0, 1)))#I
    symbols.add(smb(48, (1, 1)))#-
    symbols.add(smb(29, (8, 1)))#H
    symbols.add(smb(30, (9, 1)))#I
    symbols.add(smb(48, (10, 1)))#-
    symbols.add(smb(12, (2, 23)))#copyright
    symbols.add(smb(1, (4, 23)))#1
    symbols.add(smb(9, (5, 23)))#9
    symbols.add(smb(8, (6, 23)))#8
    symbols.add(smb(0, (7, 23)))#0
    symbols.add(smb(35, (9, 23)))#N
    symbols.add(smb(22, (10, 23)))#A
    symbols.add(smb(34, (11, 23)))#M
    symbols.add(smb(24, (12, 23)))#C
    symbols.add(smb(36, (13, 23)))#O
    symbols.add(smb(13, (14, 23)))#,
    symbols.add(smb(2, (15, 23)))#2
    symbols.add(smb(0, (16, 23)))#0
    symbols.add(smb(2, (17, 23)))#2
    symbols.add(smb(4, (18, 23)))#4
    symbols.add(smb(27, (20, 23)))#F
    symbols.add(smb(22, (21, 23)))#A
    symbols.add(smb(39, (22, 23)))#R
    symbols.add(smb(34, (23, 23)))#M
    symbols.add(smb(26, (24, 23)))#E
    symbols.add(smb(39, (25, 23)))#R
    symbols.add(smb(10, (26, 23)))#_
    symbols.add(smb(2, (27, 23)))#2
    symbols.add(smb(0, (28, 23)))#0
    symbols.add(smb(1, (29, 23)))#1
    symbols.add(smb(0, (30, 23)))#0
    symbols.add(smb(24, (9, 18)))#C
    symbols.add(smb(36, (10, 18)))#O
    symbols.add(smb(35, (11, 18)))#N
    symbols.add(smb(40, (12, 18)))#S
    symbols.add(smb(41, (13, 18)))#T
    symbols.add(smb(39, (14, 18)))#R
    symbols.add(smb(42, (15, 18)))#U
    symbols.add(smb(24, (16, 18)))#C
    symbols.add(smb(41, (17, 18)))#T
    symbols.add(smb(30, (18, 18)))#I
    symbols.add(smb(36, (19, 18)))#O
    symbols.add(smb(35, (20, 18)))#N
    symbols.add(smb(2, (9, 16)))#2
    symbols.add(smb(37, (11, 16)))#P
    symbols.add(smb(33, (12, 16)))#L
    symbols.add(smb(22, (13, 16)))#A
    symbols.add(smb(46, (14, 16)))#Y
    symbols.add(smb(26, (15, 16)))#E
    symbols.add(smb(39, (16, 16)))#R
    symbols.add(smb(40, (17, 16)))#S
    symbols.add(smb(1, (9, 14)))#1
    symbols.add(smb(37, (11, 14)))#P
    symbols.add(smb(33, (12, 14)))#L
    symbols.add(smb(22, (13, 14)))#A
    symbols.add(smb(46, (14, 14)))#Y
    symbols.add(smb(26, (15, 14)))#E
    symbols.add(smb(39, (16, 14)))#R

def add_symbols_score(symbols, data):
    ch = [{"from" : (255, 255, 255), "to" : (181, 49, 33)}]
    ch2 = [{"from" : (0, 0, 0), "to" : (181, 49, 33)}, {"from" : (99, 99, 99), "to" : (0, 0, 0)}]
    
    symbols.add(smb(29, (6, 1), ch))#H
    symbols.add(smb(30, (7, 1), ch))#I
    symbols.add(smb(48, (8, 1), ch))#-
    symbols.add(smb(40, (9, 1), ch))#S
    symbols.add(smb(24, (10, 1), ch))#C
    symbols.add(smb(36, (11, 1), ch))#O
    symbols.add(smb(39, (12, 1), ch))#R
    symbols.add(smb(26, (13, 1), ch))#E

    symbols.add(smb(40, (10, 3)))#S
    symbols.add(smb(41, (11, 3)))#T
    symbols.add(smb(22, (12, 3)))#A
    symbols.add(smb(28, (13, 3)))#G
    symbols.add(smb(26, (14, 3)))#E

    symbols.add(smb(17, (1, 5), ch2))#I
    symbols.add(smb(48, (2, 5), ch))#-
    symbols.add(smb(37, (3, 5), ch))#P
    symbols.add(smb(33, (4, 5), ch))#L
    symbols.add(smb(22, (5, 5), ch))#A
    symbols.add(smb(46, (6, 5), ch))#Y
    symbols.add(smb(26, (7, 5), ch))#E
    symbols.add(smb(39, (8, 5), ch))#R

class UI():
    def __init__(self, menu, score_data=[]):
        self.menu = menu
        self.symbols = pygame.sprite.Group()
        self.score_data = score_data
        if self.menu == ["main menu"]:
            add_symbols(self.symbols)
        elif self.menu == ["score"]:
            add_symbols_score(self.symbols, self.score_data)
        self.select_level = 1
        self.W = 1920
        self.H = 1080
        self.game_window_pos = [
            self.W / 2 - 416,
            self.H / 2 - 416
        ]
        file = open("files/player_data.json", "r")
        js = json.load(file)
        self.maxlevel = js["MaxLevel"]
        self.score = js["Score"]
        self.bestscore = js["BestScore"]
        self.selection = 0
        self.track = 0
        file.close()
        self.logo = pygame.image.load("files/images/logo.png")
        self.logo = pygame.transform.scale(self.logo, (self.logo.get_width() * 4, self.logo.get_height() * 4))
        self.pts_image = get_images.get_text_image("pts")
        self.score_timer = 0

    def update(self, events):
        left = False
        right = False
        up = False
        down = False
        F1 = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    F1 = True
                else:
                    F1 = False
                if event.key == pygame.K_LEFT:
                    left = True
                else:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = True
                else:
                    right = False
                if event.key == pygame.K_UP:
                    up = True
                else:
                    up = False
                if event.key == pygame.K_DOWN:
                    down = True
                else:
                    down = False
        if self.menu[0] == "select level":
            if left:
                self.select_level -= 1
            if right:
                self.select_level += 1
            if self.select_level < 0:
                self.select_level = 0
            if self.select_level > 12:
                self.select_level = 12
            if self.select_level > self.maxlevel + 1:
                self.select_level = self.maxlevel + 1
            if F1:
                self.menu[0] = "game"#запуск игры
        elif self.menu[0] == "main menu":
            self.track += 1
            self.track %= 6
            if F1 and self.selection == 0:#1 игрок
                self.menu[0] = "select level"
            if F1 and self.selection == 1:#2 игрока
                self.menu[0] = "select level"
            if F1 and self.selection == 2:#конструктор
                self.menu[0] = "game"#запуск игры
            if up:
                self.selection -= 1
                if self.selection < 0:
                    self.selection = 0
            if down:
                self.selection += 1
                if self.selection > 2:
                    self.selection = 2
        elif self.menu[0] == "score":#подсчет очков
            pass

    def draw(self, screen):
        if self.menu[0] == "main menu":
            screen.fill((0, 0, 0))
            self.symbols.draw(screen)
            screen.blit(get_images.get_tank_image("yellow", 0, 3, self.track > 2), (6 * 32 + self.game_window_pos[0], self.selection * 64 + 14 * 32 - 16 + self.game_window_pos[1]))
            screen.blit(get_images.get_text_image(str(self.score)), (2 * 32 + self.game_window_pos[0], 1 * 32 + self.game_window_pos[1]))
            screen.blit(get_images.get_text_image(str(self.bestscore)), (11 * 32 + self.game_window_pos[0], 1 * 32 + self.game_window_pos[1]))
            screen.blit(self.logo, (1 * 32 + self.game_window_pos[0], 3 * 32 + self.game_window_pos[1]))
        elif self.menu[0] == "select level":
            screen.fill((99, 99, 99))
            screen.blit(stage, (self.W / 2 - 80, self.H / 2 - 16))
            screen.blit(get_images.get_text_image(str(self.select_level), color_changes=[{"from" : (0, 0, 0), "to" : (99, 99, 99)}, {"from" : (255, 255, 255), "to" : (0, 0, 0)}]), (self.W / 2 - 80 + 192, self.H / 2 - 16))
        elif self.menu[0] == "score":
            screen.fill((0, 0, 0))
            self.symbols.draw(screen)
            hi_score_image = get_images.get_text_image(str(self.score_data["HiScore"]), color_changes=[{"from" : (255, 255, 255), "to" : (156, 74, 0)}])
            screen.blit(hi_score_image, (22 * 32 + self.game_window_pos[0] - hi_score_image.get_width(), 32 + self.game_window_pos[1]))
            pl1_score_image = get_images.get_text_image(str(self.score_data["Player1"]["Score"]), color_changes=[{"from" : (255, 255, 255), "to" : (156, 74, 0)}])
            screen.blit(pl1_score_image, (9 * 32 + self.game_window_pos[0] - pl1_score_image.get_width(), 7 * 32 + self.game_window_pos[1]))
            st_image = get_images.get_text_image(str(self.score_data["Stage"]))
            screen.blit(st_image, (18 * 32 + self.game_window_pos[0] - st_image.get_width(), 3 * 32 + self.game_window_pos[1]))
            screen.blit(self.pts_image, (6 * 32 + self.game_window_pos[0], 10 * 32 + self.game_window_pos[1]))
            screen.blit(self.pts_image, (6 * 32 + self.game_window_pos[0], 13 * 32 + self.game_window_pos[1]))
            screen.blit(self.pts_image, (6 * 32 + self.game_window_pos[0], 16 * 32 + self.game_window_pos[1]))
            screen.blit(self.pts_image, (6 * 32 + self.game_window_pos[0], 19 * 32 + self.game_window_pos[1]))
            screen.blit(get_images.get_text_image("total"), (4 * 32 + self.game_window_pos[0], 21 * 32 + self.game_window_pos[1]))
            screen.blit(get_images.get_text_image("________"), (10 * 32 + self.game_window_pos[0], 20 * 32 + self.game_window_pos[1]))
            tot_en_image = get_images.get_text_image(str(sum(self.score_data["Player1"]["Enemies"])))
            screen.blit(tot_en_image, (12 * 32 + self.game_window_pos[0] - tot_en_image.get_width(), 21 * 32 + self.game_window_pos[1]))
            for i in range(4):
                en_score_image = get_images.get_text_image(str(self.score_data["Player1"]["Enemies"][i] * ((i + 1) * 100)))
                screen.blit(en_score_image, (4 * 32 + self.game_window_pos[0] - en_score_image.get_width(), (10 + i * 3) * 32 + self.game_window_pos[1]))
                count_image = get_images.get_text_image(str(self.score_data["Player1"]["Enemies"][i]))
                screen.blit(count_image, (12 * 32 + self.game_window_pos[0] - count_image.get_width(), (10 + i * 3) * 32 + self.game_window_pos[1]))
                screen.blit(get_images.get_tank_image("gray", 4 + i, 0, 0), (13 * 32 + self.game_window_pos[0], (10 + i * 3) * 32 + self.game_window_pos[1] - 8))
                screen.blit(get_images.get_symbol_image(49), (12 * 32 + self.game_window_pos[0] + 4, (10 + i * 3) * 32 + self.game_window_pos[1]))

    def get_world(self):
        file = open(f"files/levels/level{self.select_level}.json", "r")
        level = json.load(file)
        file.close()
        t = "1player"
        if self.selection == 2:
            t = "constructor"
        game_world = world.World(self.menu, enemies=level["Enemies"], levelnumber=self.select_level, _type=t, count_of_players=(self.selection == 1) + 1)
        self.world = game_world
        if self.selection != 2:
            for x in range(26):
                for y in range(26):
                    game_world.field[x][y] = self.decode_block(level["Blocks"][x][y], (x, y))
            for i in range(len(level["RemovedBlocks"])):
                elem = level["RemovedBlocks"][i]
                game_world.field[elem["X"]][elem["Y"]] = self.decode_block(level["RemovedBlocks"][i]["To"], (elem["X"], elem["Y"]))
        game_world.enemies_with_bonuses = level["EnemiesWithBonuses"]
        game_world.reset_blocks = level["ResetBlocks"]
        return(game_world)

    def decode_block(self, code, pos):
        type1 = code["BlockType"]
        if type1 == 0:
            blocktype = "air"
        elif type1 == 1:
            blocktype = "trees"
        elif type1 == 2:
            blocktype = "water"
        elif type1 == 3:
            blocktype = "ice"
        elif type1 == 4:
            blocktype = "cement"
        elif type1 == 5:
            blocktype = "brick"
        elif type1 == 6:
            blocktype = "base"
        ret = block.Block(pos, blocktype, self.world)
        if "BaseType" in code:
            ret.basetype = code["BaseType"]
        if "Damage" in code:
            ret.damage = code["Damage"]
        if "IsBreak" in code:
            ret.is_break = code["IsBreak"]
        ret.change_image()
        return(ret)
