#настройка
import pygame
import random as r
import math
import world
import ui

pygame.mixer.pre_init(44100, -16, channels=64, buffer=512)
pygame.init()
keep_going = True
steps = 0
mousedown = False
mousetag = False

W = pygame.display.Info().current_w
H = pygame.display.Info().current_h
screen = pygame.display.set_mode([W, H])
screen2 = pygame.Surface((1920, 1080))
description = "Battle city"
pygame.display.set_caption(description)
timer = pygame.time.Clock()
black = (0, 0, 0)
menu = ["main menu"]
past_menu = ["main menu"]
user_interface = ui.UI(menu)
font = pygame.font.Font("files/font.ttf", 20)
F1 = False
debug = False
seconds = 0
minutes = 0
hours = 0
timer2 = 0
game_world = None
pl1 = None
pl2 = None

while keep_going:
    steps += 1
    timer2 += 1
    events = pygame.event.get()
    F1 = False
    for event in events:
        if event.type == pygame.QUIT:#проверка выхода
            keep_going = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:#-|-
                keep_going = False
            if event.key == pygame.K_F1:
                F1 = True
            else:
                F1 = False       
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousedown = True
        if event.type == pygame.MOUSEBUTTONUP:
            mousetag = False
            mousedown = False
    #
    if menu != past_menu:
        past_menu = [menu[0]]
        if menu == ["score"]:
            user_interface = ui.UI(menu, score_data=game_world.get_data())
        elif menu == ["main"]:
            user_interface = ui.UI(menu)
        elif menu == ["game"]:
            game_world = user_interface.get_world()
            for p in game_world.players:
                if p.number == "player":
                    pl1 = p
                else:
                    pl2 = p
    if menu == ["game"]:#игра
        game_world.update(events)
        game_world.draw(screen2)
    else:
        user_interface.update(events)
        user_interface.draw(screen2)
    if F1:
        if debug == 0:
            debug = 1
        else:
            debug = 0
    screen.fill((255, 255, 255))
    screen.blit(pygame.transform.scale(screen2, (W, H)), (0, 0))
    #screen.blit(screen2, (0, 0))
    fps = int(timer.get_fps())
    if debug:
        str_hours = str(hours)
        if len(str_hours) == 1:
            str_hours = "0" + str_hours
        str_minutes = str(minutes)
        if len(str_minutes) == 1:
            str_minutes = "0" + str_minutes
        str_seconds = str(seconds)
        if len(str_seconds) == 1:
            str_seconds = "0" + str_seconds
        screen.blit(font.render("Fps: " + str(fps) + ", time: " + str_hours + ":" + str_minutes + ":" + str_seconds, False, (0, 255, 0)), (0, 0))
        
        screen.blit(font.render("Width: " + str(W) + ", Height: " + str(H), False, (255, 0, 0)), (0, 25))
        screen.blit(font.render("Game window pos:", False, (255, 0, 0)), (0, 50))
        screen.blit(font.render("X: " + str(int(W / 2 - (H * (832 / 1080) / 2))) + ", Y: " + str(int(H / 2 - (H * (832 / 1080) / 2))), False, (255, 0, 0)), (0, 75))
        
        screen.blit(font.render("Menu: " + menu[0], False, (255, 255, 0)), (0, 100))

        if menu == ["game"] and game_world != None:
            c_players = len(game_world.players)
            c_enemies = len(game_world.enemies)
            c_bonus = len(game_world.bonus)
            c_bullets = len(game_world.bullets)
            c_go = len(game_world.explosions)
            screen.blit(font.render("Objects total: " + str(sum((c_players, c_enemies, c_bonus, c_bullets, c_go))), False, (0, 0, 255)), (0, 125))
            screen.blit(font.render("Enemies: " + str(c_enemies), False, (0, 0, 255)), (0, 150))
            screen.blit(font.render("Players: " + str(c_players), False, (0, 0, 255)), (0, 175))
            screen.blit(font.render("Bullets: " + str(c_bullets), False, (0, 0, 255)), (0, 200))
            screen.blit(font.render("Graphical objects: " + str(c_go), False, (0, 0, 255)), (0, 225))
            screen.blit(font.render("Bonus: " + str(c_bonus), False, (0, 0, 255)), (0, 250))

            screen.blit(font.render("Freeze timer: " + str(game_world.clock), False, (127, 168, 255)), (0, 275))
            screen.blit(font.render("Base reset timer: " + str(game_world.base_timer), False, (127, 168, 255)), (0, 300))
            screen.blit(font.render("Enemies respawn time: " + str(game_world.time_wait), False, (127, 168, 255)), (0, 325))

            screen.blit(font.render("Player I pos: (" + str(pl1.rect.x) + ", " + str(pl1.rect.y) + ")", False, (255, 128, 0)), (0, 350))
            screen.blit(font.render("Player I rotate: " + str(pl1.rotate), False, (255, 128, 0)), (0, 375))
            screen.blit(font.render("Player I bullets: " + str(pl1.bullets), False, (255, 128, 0)), (0, 400))
            screen.blit(font.render("Player I upgrade: " + str(pl1.upgrade), False, (255, 128, 0)), (0, 425))
            screen.blit(font.render("Player I shield timer: " + str(pl1.shield_timer) + ", shield: " + str(pl1.shield), False, (255, 128, 0)), (0, 450))

            if game_world.count_of_players == 2:
                screen.blit(font.render("Player II pos: (" + str(pl2.rect.x) + ", " + str(pl2.rect.y) + ")", False, (90, 0, 255)), (0, 475))
                screen.blit(font.render("Player II rotate: " + str(pl2.rotate), False, (90, 0, 255)), (0, 500))
                screen.blit(font.render("Player II bullets: " + str(pl2.bullets), False, (90, 0, 255)), (0, 525))
                screen.blit(font.render("Player II upgrade: " + str(pl2.upgrade), False, (90, 0, 255)), (0, 550))
                screen.blit(font.render("Player II shield timer: " + str(pl2.shield_timer) + ", shield: " + str(pl2.shield), False, (90, 0, 255)), (0, 575))
    if timer2 >= fps:
        timer2 = 0
        seconds += 1
    if seconds >= 60:
        minutes += 1
        seconds = 0
    if minutes >= 60:
        hours += 1
        minutes = 0
    pygame.display.update()
    timer.tick(60)
pygame.quit()
