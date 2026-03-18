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

class UI():
    def __init__(self, menu, score_data=[]):
        self.menu = menu
        self.score_data = score_data
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
        self.select_level = 1
        if self.menu[0] == "score":
            self.select_level = score_data["NextLevel"]
        self.selection = 0
        self.track = 0
        file.close()
        self.logo = pygame.image.load("files/images/logo.png")
        self.logo = pygame.transform.scale(self.logo, (self.logo.get_width() * 4, self.logo.get_height() * 4))
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
            if self.select_level > 35:
                self.select_level = 35
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
            if self.score_timer == 10 or self.score_timer == 25 or self.score_timer == 40 or self.score_timer == 55:
                score_sound = pygame.mixer.Sound("files/sounds/level_end_score.mp3")
                score_sound.play()
            self.score_timer += 1
            if self.score_timer == 200:
                self.menu[0] = "select level"

    def draw(self, screen):
        if self.menu[0] == "main menu":
            screen.fill((0, 0, 0))
            screen.blit(get_images.get_tank_image("yellow", 0, 3, self.track > 2), (6 * 32 + self.game_window_pos[0], self.selection * 64 + 14 * 32 - 16 + self.game_window_pos[1]))
            screen.blit(get_images.get_text_image("i- " + str(self.score)), (0 * 32 + self.game_window_pos[0], 0 * 32 + self.game_window_pos[1]))
            screen.blit(get_images.get_text_image("hi- " + str(self.bestscore)), (9 * 32 + self.game_window_pos[0], 0 * 32 + self.game_window_pos[1]))
            screen.blit(get_images.get_text_image("1 player"), (9 * 32 + self.game_window_pos[0], 14 * 32 + self.game_window_pos[1]))
            screen.blit(get_images.get_text_image("2 players"), (9 * 32 + self.game_window_pos[0], 16 * 32 + self.game_window_pos[1]))
            screen.blit(get_images.get_text_image("consruction"), (9 * 32 + self.game_window_pos[0], 18 * 32 + self.game_window_pos[1]))
            screen.blit(get_images.get_text_image("@1985 namco,2025 farmer_2010"), (4 * 32 + self.game_window_pos[0], 23 * 32 + self.game_window_pos[1]))
            screen.blit(self.logo, (1 * 32 + self.game_window_pos[0], 3 * 32 + self.game_window_pos[1]))
        elif self.menu[0] == "select level":
            screen.fill((99, 99, 99))
            screen.blit(stage, (self.W / 2 - 80, self.H / 2 - 16))
            screen.blit(get_images.get_text_image(str(self.select_level), color_changes=[{"from" : (0, 0, 0), "to" : (99, 99, 99)}, {"from" : (255, 255, 255), "to" : (0, 0, 0)}]), (self.W / 2 - 80 + 192, self.H / 2 - 16))
        elif self.menu[0] == "score":
            screen.fill((0, 0, 0))
            hi_score_image = get_images.get_text_image(str(self.score_data["HiScore"]), color_changes=[{"from" : (255, 255, 255), "to" : (156, 74, 0)}])
            screen.blit(hi_score_image, (22 * 32 + self.game_window_pos[0] - hi_score_image.get_width(), 32 + self.game_window_pos[1]))
            pl1_score_image = get_images.get_text_image(str(self.score_data["Player1"]["Score"]), color_changes=[{"from" : (255, 255, 255), "to" : (156, 74, 0)}])
            screen.blit(pl1_score_image, (9 * 32 + self.game_window_pos[0] - pl1_score_image.get_width(), 7 * 32 + self.game_window_pos[1]))
            st_image = get_images.get_text_image(str(self.score_data["Stage"]))
            screen.blit(st_image, (18 * 32 + self.game_window_pos[0] - st_image.get_width(), 3 * 32 + self.game_window_pos[1]))
            screen.blit(get_images.get_text_image("total"), (4 * 32 + self.game_window_pos[0], 21 * 32 + self.game_window_pos[1]))
            screen.blit(get_images.get_text_image("________"), (10 * 32 + self.game_window_pos[0], 20 * 32 + self.game_window_pos[1]))
            tot_en_image = get_images.get_text_image(str(sum(self.score_data["Player1"]["Enemies"])))
            screen.blit(tot_en_image, (12 * 32 + self.game_window_pos[0] - tot_en_image.get_width(), 21 * 32 + self.game_window_pos[1]))
            for i in range(4):
                if self.score_timer >= 10 + i * 15:
                    en_score_image = get_images.get_text_image(str(self.score_data["Player1"]["Enemies"][i] * ((i + 1) * 100)))
                    screen.blit(en_score_image, (5 * 32 + self.game_window_pos[0] - en_score_image.get_width(), (10 + i * 3) * 32 + self.game_window_pos[1]))
                    count_image = get_images.get_text_image(str(self.score_data["Player1"]["Enemies"][i]))
                    screen.blit(count_image, (12 * 32 + self.game_window_pos[0] - count_image.get_width(), (10 + i * 3) * 32 + self.game_window_pos[1]))
                screen.blit(get_images.get_text_image("pts"), (6 * 32 + self.game_window_pos[0], (10 + i * 3) * 32 + self.game_window_pos[1]))
                screen.blit(get_images.get_tank_image("gray", 4 + i, 0, 0), (13 * 32 + self.game_window_pos[0], (10 + i * 3) * 32 + self.game_window_pos[1] - 8))
                screen.blit(get_images.get_symbol_image(49), (12 * 32 + self.game_window_pos[0] + 4, (10 + i * 3) * 32 + self.game_window_pos[1]))
                if "Player2" in self.score_data:
                    screen.blit(get_images.get_symbol_image(51), (15 * 32 + self.game_window_pos[0], (10 + i * 3) * 32 + self.game_window_pos[1]))
                    screen.blit(get_images.get_text_image("pts"), (24 * 32 + self.game_window_pos[0], (10 + i * 3) * 32 + self.game_window_pos[1]))
                    if self.score_timer >= 10 + i * 15:
                        en_score_image = get_images.get_text_image(str(self.score_data["Player2"]["Enemies"][i] * ((i + 1) * 100)))
                        screen.blit(en_score_image, (23 * 32 + self.game_window_pos[0] - en_score_image.get_width(), (10 + i * 3) * 32 + self.game_window_pos[1]))
                        count_image = get_images.get_text_image(str(self.score_data["Player2"]["Enemies"][i]))
                        screen.blit(count_image, (18 * 32 + self.game_window_pos[0] - count_image.get_width(), (10 + i * 3) * 32 + self.game_window_pos[1]))
            #
            screen.blit(get_images.get_text_image("hi-score", color_changes=[{"from" : (255, 255, 255), "to" : (181, 49, 33)}]),
                (6 * 32 + self.game_window_pos[0], 32 + self.game_window_pos[1]
            ))
            screen.blit(get_images.get_text_image("stage"), (10 * 32 + self.game_window_pos[0], 3 * 32 + self.game_window_pos[1]))
            screen.blit(get_images.get_text_image(".", color_changes=[{"from" : (0, 0, 0), "to" : (181, 49, 33)}, {"from" : (99, 99, 99), "to" : (0, 0, 0)}]),
                (32 + self.game_window_pos[0], 5 * 32 + self.game_window_pos[1]
            ))
            screen.blit(get_images.get_text_image("-player", color_changes=[{"from" : (255, 255, 255), "to" : (181, 49, 33)}]),
                (2 * 32 + self.game_window_pos[0], 5 * 32 + self.game_window_pos[1]
            ))
            if "Player2" in self.score_data:
                screen.blit(get_images.get_text_image(":", color_changes=[{"from" : (0, 0, 0), "to" : (181, 49, 33)}, {"from" : (99, 99, 99), "to" : (0, 0, 0)}]),
                    (19 * 32 + self.game_window_pos[0], 5 * 32 + self.game_window_pos[1]
                ))
                screen.blit(get_images.get_text_image("-player", color_changes=[{"from" : (255, 255, 255), "to" : (181, 49, 33)}]),
                    (20 * 32 + self.game_window_pos[0], 5 * 32 + self.game_window_pos[1]
                ))
                pl2_score_image = get_images.get_text_image(str(self.score_data["Player2"]["Score"]), color_changes=[{"from" : (255, 255, 255), "to" : (156, 74, 0)}])
                screen.blit(pl2_score_image, (27 * 32 + self.game_window_pos[0] - pl2_score_image.get_width(), 7 * 32 + self.game_window_pos[1]))

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
