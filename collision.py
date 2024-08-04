import block
import pygame
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

def border_collision(sprite):
    if sprite.rect.x > sprite.world.game_window_pos2[0] - sprite.image.get_width():
        return(True)
    elif sprite.rect.x < sprite.world.game_window_pos[0]:
        return(True)
    elif sprite.rect.y > sprite.world.game_window_pos2[1] - sprite.image.get_height():
        return(True)
    elif sprite.rect.y < sprite.world.game_window_pos[1]:
        return(True)

def block_collision(sprite, detectors=("cement", "water", "brick", "base")):
    for x in range(26):
        for y in range(26):
            for i in range(len(detectors)):
                if pygame.sprite.collide_rect(sprite.world.field[x][y], sprite) and sprite.world.field[x][y].type == detectors[i]:
                    return(True)
    return(False)

def enemy_collision(sprite):
    for d in sprite.world.enemies:#проверка столкновений с врагами
        if pygame.sprite.collide_rect(d, sprite):
            return(True)
    return(False)

def player_collision(sprite):
    for s in sprite.world.players:
        if pygame.sprite.collide_rect(s, sprite) and sprite.number != s.number:
            return([True, s.number])
    return([False, None])

def collision_for_player(sprite):
    #проверка столкновения с границей
    if border_collision(sprite):
        return(True)
    #проверка столкновения с врагами
    if enemy_collision(sprite):
        return(True)
    #проверка столкновения с блоками
    if block_collision(sprite):
        return(True)
    #проверка столкновений с другими игроками
    for s in sprite.world.players:
        if pygame.sprite.collide_rect(s, sprite) and sprite.number != s.number:
            return(True)
    return(False)

def collision_for_enemy(sprite):
    ret = False
    tank_ret = False
    #проверка столкновения с границей
    if border_collision(sprite):
        ret = True
    #проверка столкновения с игроком
    if player_collision(sprite)[0]:
        tank_ret = True
    #проверка столкновения с другими врагами
    for d in sprite.world.enemies:
        if pygame.sprite.collide_rect(d, sprite) and d.number != sprite.number:
            tank_ret = True
    #проверка столкновения с блоками
    if block_collision(sprite):
        ret = True
    return((ret, tank_ret))

def collision_for_bullet(sprite):
    ret = False
    killed = None
    #проверка столкновения с границей
    if border_collision(sprite):
        ret = True
    #проверка столкновения с блоками
    for x in range(26):
        for y in range(26):
            if sprite.world.field[x][y].type == "cement":
                if pygame.sprite.collide_rect(sprite.world.field[x][y], sprite):
                    ret = True
                    if sprite.have_break_cement:
                        sprite.world.field[x][y].type = "air"
                        sprite.world.field[x][y].change_image()
            elif sprite.world.field[x][y].type == "brick":
                if pygame.sprite.collide_rect(sprite.world.field[x][y], sprite):#уничтожение кирпичного блока
                    block_damage = sprite.world.field[x][y].damage
                    block_damage = break_brick(block_damage, sprite.rotate)
                    sprite.world.field[x][y].damage = block_damage
                    sprite.world.field[x][y].change_image()
                    sprite.world.field[x][y].update()
                    ret = True
            elif sprite.world.field[x][y].type == "base":
                if pygame.sprite.collide_rect(sprite.world.field[x][y], sprite):
                    sound = pygame.mixer.Sound("files/sounds/player_death.mp3")
                    sound.play()
                    sprite.world.field[x][y].is_break = 1
                    sprite.world.field[x][y].change_image()
                    sprite.world.field[x][y].update()
                    ret = True
    if "player" in sprite.number:#если пулю выпустил игрок
        #проверка столкновений врагами
        for e in sprite.world.enemies:
            if pygame.sprite.collide_rect(e, sprite):
                ret = True
                killed = e.number
                break
        for s in sprite.world.players:
            if pygame.sprite.collide_rect(s, sprite) and sprite.number != s.number:
                ret = True
        for b in sprite.world.bullets:
            if b.number != sprite.number:
                if pygame.sprite.collide_rect(b, sprite):
                    ret = True
                    b.kill()
                    for f in sprite.world.players:
                        if f.number == b.number:
                            f.bullets += 1
    else:#если пулю выпустил не игрок
        #проверка столкновения с игроком
        a = player_collision(sprite)
        if a[0]:
            ret = True
            killed = a[1]
            #print(killed)
    return([ret, killed])

def bonus_collision(sprite, bonus_list):
    for i in bonus_list:
        if pygame.sprite.collide_rect(sprite, i):
            i.die()
            return(i.type)
    return(None)

def collision(sprite, sftype):
    if "player" in sftype:#если игрок
        return(collision_for_player(sprite))
    elif sftype == "enemy":#если враг
        return(collision_for_enemy(sprite))
    elif sftype == "bullet":#если пуля
        return(collision_for_bullet(sprite))
    elif sftype == "ice":
        #проверка столкновения игрока со льдом
        return(block_collision(sprite, detectors=("ice", "a")))
    elif sftype == "bonus":
        return(bonus_collision(sprite, sprite.world.bonus))
