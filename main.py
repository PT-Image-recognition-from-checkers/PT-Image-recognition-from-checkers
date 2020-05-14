from urllib.request import urlopen
import board
import cv2
import numpy as np
import pygame
import sys
import virtual_board
import time
import pygame_textinput
import re


#telefon
url = 'http://192.168.8.200:8080/shot.jpg'

#laptop
#cap = cv2.VideoCapture(0)

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1210, 600))
pygame.display.set_caption('Checkers Game')

bg = pygame.image.load("assets/board.png").convert()
rp = pygame.image.load("assets/red_pawn.png")
wp = pygame.image.load("assets/white_pawn.png")
rq = pygame.image.load("assets/red_queen.png")
wq = pygame.image.load("assets/white_queen.png")

clock = pygame.time.Clock()

global checkers_list_before
global checkers_list_after
checkers_list_before = []
checkers_list_after = []
global checkers_list_correct
checkers_list_correct = []
checkers_list = []
values = None
global before_count
global after_count
before_count = 0
after_count = 0
global img, dst


def check_move():
    global checkers_list_correct, checkers_list_after, before_count, after_count

    while checkers_list_correct != checkers_list_after:
        print('ŁAJL')
        time.sleep(1)
        # KOMPUTER
        # ret, img = cap.read()
        # TELEFON
        imgResp = urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, 1)

        dst, crop_rect = board.find_edges_and_perspective_transform(img)
        comparison1 = crop_rect < values1
        comparison2 = crop_rect > values2
        equal_arrays = comparison1.all()
        equal_arrays1 = comparison2.all()
        checkers_list_after = board.find_checkers(dst)



#Menu
menu_image = pygame.image.load("assets/menu.png")
start_game_button = pygame.image.load("assets/button.png")
settings_button = pygame.image.load("assets/button.png")
exit_button = pygame.image.load("assets/button.png")

white = (255,255,255)
highlight_color = (104, 46, 5)
menu = True
menu_font = pygame.font.Font("assets/GROBOLD.ttf", 20)
start_game_text = menu_font.render("Start game", True, white)
settings_text = menu_font.render("Settings", True, white)
quit_text = menu_font.render("Quit", True, white)


while True:

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_game_button.get_rect(topleft=(780, 220)).collidepoint(x, y):
                    print("start game")
                    menu = False
                elif start_game_button.get_rect(topleft=(780, 350)).collidepoint(x, y):
                    print("settings")

                elif start_game_button.get_rect(topleft=(780, 480)).collidepoint(x, y):
                    print("exit")
                    pygame.quit()
                    quit()

        x, y = pygame.mouse.get_pos()
        if start_game_button.get_rect(topleft=(780, 220)).collidepoint(x, y):
            start_game_text = menu_font.render("Start game", True, highlight_color)
        elif start_game_button.get_rect(topleft=(780, 350)).collidepoint(x, y):
            settings_text = menu_font.render("Settings", True, highlight_color)
        elif start_game_button.get_rect(topleft=(780, 480)).collidepoint(x, y):
            quit_text = menu_font.render("Quit", True, highlight_color)
        else:
            start_game_text = menu_font.render("Start game", True, white)
            settings_text = menu_font.render("Settings", True, white)
            quit_text = menu_font.render("Quit", True, white)


        screen.blit(menu_image, (0, 0))
        screen.blit(start_game_button, (780, 220))
        screen.blit(settings_button, (780, 350))
        screen.blit(exit_button, (780, 480))

        screen.blit(start_game_text, (870, 260))
        screen.blit(settings_text, (883, 390))
        screen.blit(quit_text, (900, 520))

        pygame.display.flip()
        clock.tick(30)
        pygame.display.update()

    #telefon
    imgResp = urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, 1)

    #laptop
    #ret, img = cap.read()

    dst, crop_rect = board.find_edges_and_perspective_transform(img)

    checkers_list_before = board.find_checkers(dst)
    if 'RP' not in checkers_list_before or 'WP' not in checkers_list_before or 'RQ' not in checkers_list_before or 'WQ' not in checkers_list_before:
        checkers_list_before = checkers_list_after
        if len(checkers_list_correct) == 0:
            checkers_list_correct = checkers_list_after

    if values is None:
        values = np.array(list(crop_rect), dtype='float32')
        values1 = values + 30
        values2 = values - 30

    comparison1 = crop_rect < values1
    comparison2 = crop_rect > values2
    equal_arrays = comparison1.all()
    equal_arrays1 = comparison2.all()

    while not equal_arrays and not equal_arrays1:
        before_count = 0
        after_count = 0
        time.sleep(1)
        #KOMPUTER
        #ret, img = cap.read()
        #TELEFON
        imgResp = urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, 1)

        dst, crop_rect = board.find_edges_and_perspective_transform(img)
        comparison1 = crop_rect < values1
        comparison2 = crop_rect > values2
        equal_arrays = comparison1.all()
        equal_arrays1 = comparison2.all()
        checkers_list_after = board.find_checkers(dst)

        for i in range(len(checkers_list_before)):
            if checkers_list_before[i] is not None:
                before_count += 1
            if checkers_list_after[i] is not None:
                after_count += 1

    if len(checkers_list_after) != 0:
        if checkers_list_after != checkers_list_before and before_count != 0:
            print(before_count, after_count)
            if before_count == after_count:
                move, _ = virtual_board.move(checkers_list_before, checkers_list_after)
                if move:
                   print('PRAWIDŁOWY RUCH')
                   checkers_list_correct = checkers_list_after
                   print(checkers_list_correct)
                   virtual_board.gameover_check(checkers_list_correct)
                elif not move:
                    print('NIEPRAWIDŁOWY RUCH')
                    check_move()
                before_count = 0
                after_count = 0

            else:
                capture = virtual_board.capture(checkers_list_before, checkers_list_after)
                if capture:
                   print('PRAWIDŁOWE BICIE')
                   checkers_list_correct = checkers_list_after
                   virtual_board.gameover_check(checkers_list_correct)
                elif not capture:
                    print('NIEPRAWIDŁOWE BICIE')
                    check_move()
                before_count = 0
                after_count = 0

    #cv2.imshow("dst", dst)
    checkers_list = board.find_checkers(dst)

    dst_RGB = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    #cv2.imshow("dst_RGB", dst_RGB)
    dst_RGB = np.rot90(dst_RGB)
    dst_RGB = pygame.surfarray.make_surface(dst_RGB)
    dst_RGB = pygame.transform.flip(dst_RGB, True, False)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill((77, 40, 0))
    screen.blit(bg, (0, 0))
    screen.blit(dst_RGB, (610, 0))

    position = 0
    checkers = virtual_board.find_fields()
    if checkers_list is not None:
        for ch in checkers_list:
            if ch == 'RP':
                screen.blit(rp, (checkers[position][0][0], checkers[position][0][1]))
                position += 1
            elif ch == 'WP':
                screen.blit(wp, (checkers[position][0][0], checkers[position][0][1]))
                position += 1
            elif ch == 'WQ':
                screen.blit(wq, (checkers[position][0][0], checkers[position][0][1]))
                position += 1
            elif ch == 'RQ':
                screen.blit(rq, (checkers[position][0][0], checkers[position][0][1]))
                position += 1
            else:
                position += 1

    pygame.display.update()
    #clock.tick(60)

    if ord('q') == cv2.waitKey(10):
        exit(0)
