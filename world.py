import graphical_object as GO
import bonus
import pygame
import random
import spawner
import player
import block
import enemy
import json
import get_images
pygame.init()

black = (0, 0, 0)
gray = (99, 99, 99)

font = pygame.font.SysFont(None, 50)

class World():
    def __init__(self, menu, respawn_points=((0, 0), (384, 0), (768, 0)), count_of_players=1, levelnumber=0, enemies=[0 for x in range(20)], _type="1player"):
        file = open("files/player_data.json", "r")
        player_data = json.load(file)
        self.stat = [{"Score" : 0, "Enemies" : [0, 0, 0, 0]} for i in range(count_of_players)]
        self.type = _type
        self.enemies_list = enemies
        self.enemies_with_bonuses = []
        self.menu = menu
        self.W = 1920
        self.H = 1080
        self.game_window_pos = [
            self.W / 2 - 416,
            self.H / 2 - 416
            ]
        self.game_window_pos2 = [
            self.W / 2 + 416,
            self.H / 2 + 416
            ]
        self.reset_blocks = []
        self.count_of_players = count_of_players
        self.levelnumber = levelnumber
        self.time_wait = 190 - self.levelnumber * 4 - (self.count_of_players - 1) * 20
        self.respawn_points = respawn_points
        self.player_respawn_points = ((256, 768), (512, 768))
        self.enemies = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.bonus = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.field = [[block.Block((x, y), "air", self) for y in range(26)]for x in range(26)]
        self.spawner = spawner.Spawner(respawn_points, self.enemies_list, self)
        if self.type != "constructor":
            pl = player.Player(self.player_respawn_points[0], 0, 1 * (player_data["Upgrade"] > 1) + 1, self)
            pl.upgrade = player_data["Upgrade"]
            self.players.add(pl)
        if count_of_players == 1:
            self.player_health = {"player" : player_data["Health"]}
        else:
            self.player_health = {"player" : player_data["Health"], "player2" : 2}
            pl2 = player.Player(self.player_respawn_points[1], 0, 1, self, number="player2")
            self.players.add(pl2)
        self.killed_players = []
        self.movelist = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        self.steps = 0
        self.clock = 0
        self.base_timer = 0
        self.score = player_data["Score"]
        self.bestscore = player_data["BestScore"]
        file.close()
        self.timer = -1
        self.tag = None
        self.start_pos = 0
        self.mousetag = False
        if self.type != "constructor":
            s = pygame.mixer.Sound("files/sounds/level_start.mp3")
            self.channel2 = s.play()
        self.worksound = pygame.mixer.Sound("files/sounds/tank_work.mp3")
        self.channel = self.worksound.play(loops=9000)
        self.channel.pause()
        self.gameoversound = pygame.mixer.Sound("files/sounds/level_end_gameover.mp3")
        self.pause = False

    def update(self, events):
        if not self.pause:#обновление всего
            if self.steps <= 240 or self.type == "constructor" or self.tag == "win":
                self.channel.pause()
            else:
                self.channel.unpause()
            if self.clock != 0:
                self.clock -= 1
            if self.type != "constructor":
                self.spawner.update(self.time_wait, self.count_of_players)
            self.enemies.update(self.steps, self.clock)
            if self.base_timer != 0:
                self.base_timer -= 1
            if self.base_timer == 1:
                for i in self.reset_blocks:
                    self.field[i["X"]][i["Y"]] = self.decode_block(i["res2"], (i["X"], i["Y"]))
            if self.base_timer < 240 and self.base_timer != 0:
                if (self.base_timer // 20) % 2:
                    for i in self.reset_blocks:
                        self.field[i["X"]][i["Y"]] = self.decode_block(i["res1"], (i["X"], i["Y"]))
                else:
                    for i in self.reset_blocks:
                        self.field[i["X"]][i["Y"]] = self.decode_block(i["res2"], (i["X"], i["Y"]))
            self.players.update(self.steps)
            self.bullets.update()
            self.explosions.update(self.steps)
            if self.killed_players != []:
                for elem in self.killed_players:
                    if self.player_health[elem] > 0:
                        if elem == "player":
                            self.players.add(player.Player(self.player_respawn_points[0], 0, 1, self, number=elem))
                        elif elem == "player2":
                            self.players.add(player.Player(self.player_respawn_points[1], 0, 1, self, number=elem))
                        self.player_health[elem] -= 1
                    else:
                        self.game_over()
                    self.killed_players.remove(elem)
            if self.timer > 0:
                self.timer -= 1
            elif self.timer == 0:
                if self.tag == "win":
                    self.win2()
                elif self.tag == "game_over":
                    self.game_over2()
            if self.type == "constructor":
                mousepos = pygame.mouse.get_pos()
                W = pygame.display.Info().current_w
                H = pygame.display.Info().current_h
                wh = H * (832 / 1080) / 2
                gwp = [
                    W / 2 - wh,
                    H / 2 - wh
                ]
                gwp2 = [
                    W / 2 + wh,
                    H / 2 + wh
                ]
                mouse_collision = mousepos[0] > gwp2[0] or mousepos[0] < gwp[0] or mousepos[1] > gwp2[1] or mousepos[1] < gwp[1]
                mousedown = pygame.mouse.get_pressed()[0]
                if not mousedown:
                    self.mousetag = False
                if mousedown and (not mouse_collision) and (not self.mousetag):
                    self.setblock()
                    self.mousetag = True
        #------------проверка выхода, пауза, звуки------------
        self.steps += 1
        RET = False
        TAB = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    RET = True
                else:
                    RET = False
                if event.key == pygame.K_TAB:
                    TAB = True
                else:
                    TAB = False
                    
        if TAB:
            self.stop_sounds()
            self.close_level()
            self.menu[0] = "main menu"
        elif RET and self.type != "constructor":
            if self.pause == 0:
                self.stop_sounds()
                self.pause = 1
            else:
                self.pause = 0
                self.channel2.unpause()

    def stop_sounds(self):
        self.channel.pause()
        if self.type != "constructor":
            self.channel2.pause()
        for p in self.players:
            p.channel.pause()

    def get_data(self):
        hisc = self.bestscore
        if self.score > self.bestscore:
            hisc = self.score
        a = {
            "HiScore" : hisc,
            "Stage" : self.levelnumber,
            "Player1" : {
                "Enemies" : self.stat[0]["Enemies"],
                "Score" : self.stat[0]["Score"]
            }
        }
        return(a)

    def draw(self, screen):
        screen.fill(gray)
        pygame.draw.rect(screen, black, (self.game_window_pos[0], self.game_window_pos[1], 832, 832))
        for x in range(26):
            for y in range(26):
                if self.field[x][y].type != "trees":
                    self.field[x][y].draw(screen)
        self.enemies.draw(screen)
        self.players.draw(screen)
        self.bullets.draw(screen)
        for i in self.players: i.draw(screen)
        for x in range(26):
            for y in range(26):
                if self.field[x][y].type == "trees":
                    self.field[x][y].draw(screen)
        if (self.steps // 10) % 2:
            self.bonus.draw(screen)
        self.explosions.draw(screen)
        if self.type != "constructor":
            texture = get_images.get_symbol_image(14)
            for i in range(self.spawner.max_enemies - self.spawner.enemy_number):
                screen.blit(texture, (self.game_window_pos[0] + 864 +  32 * (i % 2), self.game_window_pos[1] + 32 + 32 * (i // 2)))
            screen.blit(get_images.get_symbol_image(17), (self.game_window_pos[0] + 864, self.game_window_pos[1] + 32 * 15))#I
            screen.blit(get_images.get_symbol_image(37, color_changes=[{"from" : (0, 0, 0), "to" : (99, 99, 99)}, {"from" : (255, 255, 255), "to" : (0, 0, 0)}]), (self.game_window_pos[0] + 896, self.game_window_pos[1] + 32 * 15))#P
            screen.blit(get_images.get_symbol_image(15), (self.game_window_pos[0] + 864, self.game_window_pos[1] + 32 * 16))#player
            screen.blit(get_images.get_text_image(
                str(self.player_health["player"]),
                color_changes=[
                    {"from" : (0, 0, 0), "to" : (99, 99, 99)},
                    {"from" : (255, 255, 255), "to" : (0, 0, 0)}
                    ]
                ),
                (self.game_window_pos[0] + 896, self.game_window_pos[1] + 32 * 16)
            )#player health
            if self.count_of_players == 2:
                screen.blit(get_images.get_symbol_image(16), (self.game_window_pos[0] + 864, self.game_window_pos[1] + 32 * 18))#II
                screen.blit(get_images.get_symbol_image(37, color_changes=[{"from" : (0, 0, 0), "to" : (99, 99, 99)}, {"from" : (255, 255, 255), "to" : (0, 0, 0)}]), (self.game_window_pos[0] + 896, self.game_window_pos[1] + 32 * 18))#P
                screen.blit(get_images.get_symbol_image(15), (self.game_window_pos[0] + 864, self.game_window_pos[1] + 32 * 19))#player
                screen.blit(get_images.get_text_image(
                    str(self.player_health["player"]),
                    color_changes=[
                        {"from" : (0, 0, 0), "to" : (99, 99, 99)},
                        {"from" : (255, 255, 255), "to" : (0, 0, 0)}
                    ]
                    ),
                    (self.game_window_pos[0] + 896, self.game_window_pos[1] + 32 * 19)
                )#player2 health
            screen.blit(get_images.get_symbol_image(18), (self.game_window_pos[0] + 864, self.game_window_pos[1] + 32 * 21))#flag1
            screen.blit(get_images.get_symbol_image(19), (self.game_window_pos[0] + 896, self.game_window_pos[1] + 32 * 21))#flag2
            screen.blit(get_images.get_symbol_image(20), (self.game_window_pos[0] + 864, self.game_window_pos[1] + 32 * 22))#flag3
            screen.blit(get_images.get_symbol_image(21), (self.game_window_pos[0] + 896, self.game_window_pos[1] + 32 * 22))#flag4
            string = str(self.levelnumber)
            if len(string) == 1:
                string = " " + string
            screen.blit(get_images.get_text_image(
                string,
                color_changes=[
                    {"from" : (0, 0, 0), "to" : (99, 99, 99)},
                    {"from" : (255, 255, 255), "to" : (0, 0, 0)}
                ]
                ),
                (self.game_window_pos[0] + 864, self.game_window_pos[1] + 32 * 23)
            )#level number
        if self.start_pos <= self.H / 2:#Анимация в начале уровня
            pygame.draw.rect(screen, gray, (0, self.H / 2 + self.start_pos, self.W, self.H / 2))
            pygame.draw.rect(screen, gray, (0, 0 - self.start_pos, self.W, self.H / 2))
            self.start_pos += 12
        if self.pause and self.steps % 30 < 15:
            screen.blit(get_images.get_graphical_object_image("pause", 0, size=4), (self.W / 2 - 80, self.game_window_pos[1] + 32 * 13 + 4))

    def setblock(self):
        mousepos = pygame.mouse.get_pos()
        W = pygame.display.Info().current_w
        H = pygame.display.Info().current_h
        wh = H * (832 / 1080) / 2
        gwp = [
            W / 2 - wh,
            H / 2 - wh
        ]
        gwp2 = [
            W / 2 + wh,
            H / 2 + wh
        ]
        blockpos = [
            int((mousepos[0] - gwp[0]) // ((gwp2[0] - gwp[0]) / 26)),
            int((mousepos[1] - gwp[1]) // ((gwp2[1] - gwp[1]) / 26))
        ]
        if blockpos[0] > 25:
            blockpos[0] = 25
        if blockpos[1] > 25:
            blockpos[1]  = 25
        if self.field[blockpos[0]][blockpos[1]].type == "air":
            self.field[blockpos[0]][blockpos[1]].type = "cement"
        elif self.field[blockpos[0]][blockpos[1]].type == "cement":
            self.field[blockpos[0]][blockpos[1]].type = "trees"
        elif self.field[blockpos[0]][blockpos[1]].type == "trees":
            self.field[blockpos[0]][blockpos[1]].type = "water"
        elif self.field[blockpos[0]][blockpos[1]].type == "water":
            self.field[blockpos[0]][blockpos[1]].type = "brick"
            self.field[blockpos[0]][blockpos[1]].damage = "1111"
        elif self.field[blockpos[0]][blockpos[1]].type == "brick":
            self.field[blockpos[0]][blockpos[1]].type = "ice"
        elif self.field[blockpos[0]][blockpos[1]].type == "ice":
            self.field[blockpos[0]][blockpos[1]].type = "air"
        self.field[blockpos[0]][blockpos[1]].change_image()

    def game_over(self):
        if self.timer == -1:
            self.timer = 300
            self.explosions.add(GO.GraphicalObject((self.W / 2, self.H), "game over", display_size=(self.W, self.H)))
        self.tag = "game_over"
        self.gameoversound.play()

    def game_over2(self):
        self.stop_sounds()
        file = open("files/player_data.json", "w")
        best = self.bestscore
        if self.score > self.bestscore:
            best = self.score
        data = {
            "Health" : 2,
            "Upgrade" : 0,
            "BestScore" : best,
            "Score" : 0,
            "MaxLevel" : 0
        }
        json.dump(data, file)
        file.close()
        self.menu[0] = "score"

    def win(self):
        if self.timer == -1:
            self.timer = 300
        self.tag = "win"

    def win2(self):
        self.stop_sounds()
        file = open("files/player_data.json", "r")
        last_max_level = json.load(file)["MaxLevel"]
        file.close()
        
        file = open("files/player_data.json", "w")
        for pl in self.players:
            up = pl.upgrade
        if self.levelnumber > last_max_level:
            level = self.levelnumber
        else:
            level = last_max_level
        best = self.bestscore
        if self.score > self.bestscore:
            best = self.score
        data = {
            "Health" : self.player_health["player"],
            "Upgrade" : up,
            "BestScore" : best,
            "Score" : self.score,
            "MaxLevel" : level
        }
        json.dump(data, file)
        file.close()
        self.menu[0] = "score"

    def close_level(self):
        if self.type == "constructor":
            self.save_level("level13")
        self.menu[0] = "main menu"

    def kill_all(self):
        for i in self.enemies:
            i.die("bonus")

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
        ret = block.Block(pos, blocktype, self)
        if "BaseType" in code:
            ret.basetype = code["BaseType"]
        if "Damage" in code:
            ret.damage = code["Damage"]
        if "IsBreak" in code:
            ret.is_break = code["IsBreak"]
        ret.change_image()
        return(ret)

    def armor_base(self):
        self.base_timer = 600
        for i in self.reset_blocks:
            self.field[i["X"]][i["Y"]] = self.decode_block(i["res1"], (i["X"], i["Y"]))

    def save_level(self, name):
        file = open(f"files/levels/{name}.json", "w")
        level = {}
        blocks = [[0 for y in range(26)]for x in range(26)]
        for x in range(26):
            for y in range(26):
                if self.field[x][y].type == "air":
                    num = 0
                elif self.field[x][y].type == "trees":
                    num = 1
                elif self.field[x][y].type == "water":
                    num = 2
                elif self.field[x][y].type == "ice":
                    num = 3
                elif self.field[x][y].type == "cement":
                    num = 4
                elif self.field[x][y].type == "brick":
                    num = 5
                elif self.field[x][y].type == "base":
                    num = 6
                blocks[x][y] = {"BlockType" : num}
        level_enemies = [0 for x in range(20)]
        removed_blocks = [{"X" : 0, "Y" : 0, "To" : {"BlockType" : 0}},
                            {"X" : 1, "Y" : 0, "To" : {"BlockType" : 0}},
                            {"X" : 0, "Y" : 1, "To" : {"BlockType" : 0}},
                            {"X" : 1, "Y" : 1, "To" : {"BlockType" : 0}},
                            {"X" : 12, "Y" : 0, "To" : {"BlockType" : 0}},
                            {"X" : 13, "Y" : 0, "To" : {"BlockType" : 0}},
                            {"X" : 12, "Y" : 1, "To" : {"BlockType" : 0}},
                            {"X" : 13, "Y" : 1, "To" : {"BlockType" : 0}},
                            {"X" : 25, "Y" : 0, "To" : {"BlockType" : 0}},
                            {"X" : 24, "Y" : 0, "To" : {"BlockType" : 0}},
                            {"X" : 24, "Y" : 1, "To" : {"BlockType" : 0}},
                            {"X" : 25, "Y" : 1, "To" : {"BlockType" : 0}},
                            {"X" : 12, "Y" : 24, "To" : {"BlockType" : 6, "BaseType" : "00"}},
                            {"X" : 13, "Y" : 24, "To" : {"BlockType" : 6, "BaseType" : "10"}},
                            {"X" : 12, "Y" : 25, "To" : {"BlockType" : 6, "BaseType" : "01"}},
                            {"X" : 13, "Y" : 25, "To" : {"BlockType" : 6, "BaseType" : "11"}},
                            {"X" : 11, "Y" : 25, "To" : {"BlockType" : 5}},
                            {"X" : 11, "Y" : 24, "To" : {"BlockType" : 5}},
                            {"X" : 11, "Y" : 23, "To" : {"BlockType" : 5}},
                            {"X" : 12, "Y" : 23, "To" : {"BlockType" : 5}},
                            {"X" : 13, "Y" : 23, "To" : {"BlockType" : 5}},
                            {"X" : 14, "Y" : 23, "To" : {"BlockType" : 5}},
                            {"X" : 14, "Y" : 24, "To" : {"BlockType" : 5}},
                            {"X" : 14, "Y" : 25, "To" : {"BlockType" : 5}},
                            {"X" : 8, "Y" : 25, "To" : {"BlockType" : 0}},
                            {"X" : 9, "Y" : 25, "To" : {"BlockType" : 0}},
                            {"X" : 8, "Y" : 24, "To" : {"BlockType" : 0}},
                            {"X" : 9, "Y" : 24, "To" : {"BlockType" : 0}},
                            {"X" : 16, "Y" : 25, "To" : {"BlockType" : 0}},
                            {"X" : 16, "Y" : 24, "To" : {"BlockType" : 0}},
                            {"X" : 17, "Y" : 25, "To" : {"BlockType" : 0}},
                            {"X" : 17, "Y" : 24, "To" : {"BlockType" : 0}},
                            {"X" : 10, "Y" : 25, "To" : {"BlockType" : 0}},
                            {"X" : 10, "Y" : 24, "To" : {"BlockType" : 0}},
                            {"X" : 10, "Y" : 23, "To" : {"BlockType" : 0}},
                            {"X" : 10, "Y" : 22, "To" : {"BlockType" : 0}},
                            {"X" : 11, "Y" : 22, "To" : {"BlockType" : 0}},
                            {"X" : 12, "Y" : 22, "To" : {"BlockType" : 0}},
                            {"X" : 13, "Y" : 22, "To" : {"BlockType" : 0}},
                            {"X" : 14, "Y" : 22, "To" : {"BlockType" : 0}},
                            {"X" : 15, "Y" : 22, "To" : {"BlockType" : 0}},
                            {"X" : 15, "Y" : 23, "To" : {"BlockType" : 0}},
                            {"X" : 15, "Y" : 24, "To" : {"BlockType" : 0}},
                            {"X" : 15, "Y" : 25, "To" : {"BlockType" : 0}},
                            ]
        reset_blocks = [
            {"X" : 11, "Y" : 25, "res1" : {"BlockType" : 4}, "res2" : {"BlockType" : 5}},
            {"X" : 11, "Y" : 24, "res1" : {"BlockType" : 4}, "res2" : {"BlockType" : 5}},
            {"X" : 11, "Y" : 23, "res1" : {"BlockType" : 4}, "res2" : {"BlockType" : 5}},
            {"X" : 12, "Y" : 23, "res1" : {"BlockType" : 4}, "res2" : {"BlockType" : 5}},
            {"X" : 13, "Y" : 23, "res1" : {"BlockType" : 4}, "res2" : {"BlockType" : 5}},
            {"X" : 14, "Y" : 23, "res1" : {"BlockType" : 4}, "res2" : {"BlockType" : 5}},
            {"X" : 14, "Y" : 24, "res1" : {"BlockType" : 4}, "res2" : {"BlockType" : 5}},
            {"X" : 14, "Y" : 25, "res1" : {"BlockType" : 4}, "res2" : {"BlockType" : 5}},
            ]
        level["Blocks"] = blocks
        level["RemovedBlocks"] = removed_blocks
        level["ResetBlocks"] = reset_blocks
        level["Enemies"] = level_enemies
        level["EnemiesRespawnPoints"] = self.respawn_points
        level["PlayersRespawnPoints"] = self.player_respawn_points
        level["EnemiesWithBonuses"] = [4, 11, 18]
        json.dump(level, file)
        file.close()
