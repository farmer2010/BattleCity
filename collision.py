import block
import pygame
pygame.init()

def border_collision(sprite):
    if sprite.rect.x > sprite.world.game_window_pos2[0] - sprite.image.get_width():
        return(True)
    elif sprite.rect.x < sprite.world.game_window_pos[0]:
        return(True)
    elif sprite.rect.y > sprite.world.game_window_pos2[1] - sprite.image.get_height():
        return(True)
    elif sprite.rect.y < sprite.world.game_window_pos[1]:
        return(True)
    return(False)

def block_collision(sprite, detectors=("cement", "water", "brick", "base")):
    spos = [#блок, в котором находится пуля
        int((sprite.rect.x - sprite.world.game_window_pos[0]) // 32),
        int((sprite.rect.y - sprite.world.game_window_pos[1]) // 32)
    ]
    for x in range(spos[0], spos[0] + 2):
        for y in range(spos[1], spos[1] + 2):
            if x >= 0 and x < 26 and y >= 0 and y < 26:
                for i in range(len(detectors)):
                    if pygame.sprite.collide_rect(sprite.world.field[x][y], sprite) and sprite.world.field[x][y].type == detectors[i]:
                        return(True)
    return(False)

def enemy_collision(sprite):
    for d in sprite.world.enemies:#проверка столкновений с врагами
        if pygame.sprite.collide_rect(d, sprite) and d.timer > 80:
            return(True)
    return(False)

def player_collision(sprite):
    for s in sprite.world.players:
        if pygame.sprite.collide_rect(s, sprite) and sprite.number != s.number:
            return([True, s])
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
        if pygame.sprite.collide_rect(d, sprite) and d.number != sprite.number and d.timer > 80:
            tank_ret = True
    #проверка столкновения с блоками
    if block_collision(sprite):
        ret = True
    return((ret, tank_ret))

def collision_for_bullet(sprite):
    ret = False
    obj = None
    bl = []
    #проверка столкновения с границей
    if border_collision(sprite): ret = True
    #проверка столкновения с блоками
    spos = [#блок, в котором находится пуля
        int((sprite.rect.x - sprite.world.game_window_pos[0]) // 32),
        int((sprite.rect.y - sprite.world.game_window_pos[1]) // 32)
    ]
    for x in range(spos[0], spos[0] + 2):
        for y in range(spos[1], spos[1] + 2):
            if x >= 0 and x < 26 and y >= 0 and y < 26:
                if sprite.world.field[x][y].type == "brick" or (sprite.world.field[x][y].type == "base" and sprite.world.field[x][y].is_break == 0) or sprite.world.field[x][y].type == "cement":
                    if pygame.sprite.collide_rect(sprite, sprite.world.field[x][y]):
                        ret = True
                        bl.append(sprite.world.field[x][y])
    if "player" in sprite.number:#если пулю выпустил игрок
        #проверка столкновений с врагами
        for e in sprite.world.enemies:
            if pygame.sprite.collide_rect(e, sprite) and e.timer > 80:
                ret = True
                obj = e
                break
        #проверка столкновений с другим игроком
        for s in sprite.world.players:
            if pygame.sprite.collide_rect(s, sprite) and sprite.number != s.number:
                ret = True
        #проверка столкновения с пулями
        for b in sprite.world.bullets:
            if pygame.sprite.collide_rect(b, sprite) and b.number != sprite.number:
                ret = True
                obj = b
                break
    else:#если пулю выпустил не игрок
        #проверка столкновения с игроком
        a = player_collision(sprite)
        if a[0]:
            ret = True
            obj = a[1]
    return([ret, obj, bl])

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
