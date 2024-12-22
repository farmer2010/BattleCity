import pygame
pygame.init()

tanks = pygame.image.load("files/images/tanks.png")
symbols = pygame.image.load("files/images/symbols.png")

symbols_list = {
    "0" : 0,
    "1" : 1,
    "2" : 2,
    "3" : 3,
    "4" : 4,
    "5" : 5,
    "6" : 6,
    "7" : 7,
    "8" : 8,
    "9" : 9,
    "_" : 10,
    " " : 11,
    "@" : 12,
    "," : 13,
    "#" : 14,
    "$" : 15,
    "." : 16,
    ":" : 17,
    "%" : 18,
    "^" : 19,
    "&" : 20,
    "*" : 21,
    "a" : 22,
    "b" : 23,
    "c" : 24,
    "d" : 25,
    "e" : 26,
    "f" : 27,
    "g" : 28,
    "h" : 29,
    "i" : 30,
    "j" : 31,
    "k" : 32,
    "l" : 33,
    "m" : 34,
    "n" : 35,
    "o" : 36,
    "p" : 37,
    "q" : 38,
    "r" : 39,
    "s" : 40,
    "t" : 41,
    "u" : 42,
    "v" : 43,
    "w" : 44,
    "x" : 45,
    "y" : 46,
    "z" : 47,
    "-" : 48,
    "<" : 49,
    "!" : 50,
    ">" : 51,
    "^" : 52
}

def get_break_block_image(damage, size=32):
    img = pygame.Surface((8, 8))
    imgx = 256
    imgy = 64
    for i in range(len(damage)):
        x = i % 2
        y = i > 1
        if int(damage[i]):
            surf = pygame.Surface((4, 4))
            surfx = imgx + x * 4
            surfy = imgy + y * 4
            surf.blit(tanks, (-surfx, -surfy))
            img.blit(surf, (x * 4, y * 4))
    img = pygame.transform.scale(img, (size, size))
    img.set_colorkey((0, 0, 0))
    return(img)

def get_block_image(blocktype, mode, size=32):
    img = pygame.Surface((8, 8))
    imgx = 256
    imgy = 64
    imgy += blocktype * 8
    imgx += mode * 8
    img.blit(tanks, (-imgx, -imgy))
    img = pygame.transform.scale(img, (size, size))
    img.set_colorkey((0, 0, 0))
    return(img)

def get_bullet_image(rotate, size=20):
    img = pygame.Surface((5, 5))
    imgx = 320
    imgy = 107
    imgx += rotate * 5
    img.blit(tanks, (-imgx, -imgy))
    img = pygame.transform.scale(img, (size, size))
    img.set_colorkey((0, 0, 0))
    return(img)

def get_tank_image(color, tanktype, rotate, track, size=64):
    img = pygame.Surface((16, 16))
    imgx = 0
    imgy = 0
    if color == "yellow":
        imgx = 0
        imgy = 0
    elif color == "gray":
        imgx = 128
        imgy = 0
    elif color == "green":
        imgx = 0
        imgy = 128
    elif color == "purple":
        imgx = 128
        imgy = 128
    imgy += tanktype * 16
    imgx += rotate * 32
    imgx += track * 16
    img.blit(tanks, (-imgx, -imgy))
    img = pygame.transform.scale(img, (size, size))
    img.set_colorkey((0, 0, 0))
    return(img)

def get_base_image(mode, is_break, size=32):
    img = pygame.Surface((8, 8))
    imgx = 304
    imgy = 32
    imgy += int(mode[1]) * 8
    imgx += int(mode[0]) * 8
    if is_break == 1:
        imgx += 16
    img.blit(tanks, (-imgx, -imgy))
    img = pygame.transform.scale(img, (size, size))
    img.set_colorkey((0, 0, 0))
    return(img)

def get_bonus_image(mode, size=64):
    img = pygame.Surface((16, 16))
    imgx = 256
    imgy = 112
    imgx += mode * 16
    img.blit(tanks, (-imgx, -imgy))
    img = pygame.transform.scale(img, (size, size))
    img.set_colorkey((0, 0, 0))
    return(img)

def get_graphical_object_image(sftype, mode, size=64):
    img = pygame.Surface((16, 16))
    if sftype == "score":
        imgx = 288
        imgy = 160
    elif sftype == "shield":
        imgx = 256
        imgy = 144
    elif sftype == "explosion":
        imgx = 256
        imgy = 128
    elif sftype == "big_explosion":
        img = pygame.Surface((32, 32))
        size = 128
        imgx = 304
        imgy = 128
    elif sftype == "spawn":
        imgx = 256
        imgy = 96
    elif sftype == "game over":
        img = pygame.Surface((32, 16))
        imgx = 288
        imgy = 184
    elif sftype == "pause":
        img = pygame.Surface((40, 8))
        imgx = 288
        imgy = 176
    
    imgx += mode * (16 + 16 * (sftype == "big_explosion"))
    img.blit(tanks, (-imgx, -imgy))
    if sftype != "game over" and sftype != "pause":
        img = pygame.transform.scale(img, (size, size))
    elif sftype == "game over":
        img = pygame.transform.scale(img, (32 * size, 16 * size))
    else:
        img = pygame.transform.scale(img, (40 * size, 8 * size))
    img.set_colorkey((0, 0, 0))
    return(img)

def set_color(img, c_from, c_to):
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            color = img.get_at((x, y))
            if color == c_from:
                img.set_at((x, y), c_to)

def get_symbol_image(mode, size=32, color_changes=[]):
    img = pygame.Surface((8, 8))
    imgx = (mode % 8) * 8
    imgy = (mode // 8) * 8
    img.blit(symbols, (-imgx, -imgy))
    img = pygame.transform.scale(img, (size, size))
    if color_changes != []:
        for i in range(len(color_changes)):
            set_color(img, pygame.Color(color_changes[i]["from"][0], color_changes[i]["from"][1], color_changes[i]["from"][2]), pygame.Color(color_changes[i]["to"][0], color_changes[i]["to"][1], color_changes[i]["to"][2]))
    return(img)

def get_text_image(text, size=32, color_changes=[]):
    img = pygame.Surface((8 * len(text), 8))
    for i in range(len(text)):
        symb = get_symbol_image(symbols_list[text[i]], size=8)
        img.blit(symb, (i * 8, 0))
    if color_changes != []:
        for i in range(len(color_changes)):
            set_color(img, pygame.Color(color_changes[i]["from"][0], color_changes[i]["from"][1], color_changes[i]["from"][2]), pygame.Color(color_changes[i]["to"][0], color_changes[i]["to"][1], color_changes[i]["to"][2]))
    img = pygame.transform.scale(img, (size * len(text), size))
    return(img)
    
