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
import time

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
camera = False

def check_move():
    global checkers_list_correct, checkers_list_after, before_count, after_count
    bad_move = pygame.image.load('assets/bad_move.png')

    screen.blit(bad_move, (0, 0))
    pygame.display.flip()
    pygame.display.update()
    pygame.mixer.music.load('assets/Error.mp3')
    pygame.mixer.music.play(0)
    while checkers_list_correct != checkers_list_after:
        print('WRONG MOVE')
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

    pygame.mixer.music.stop()


#Menu
menu_image = pygame.image.load("assets/menu.png")
button = pygame.image.load("assets/button.png")
settings_button = pygame.image.load("assets/button.png")
exit_button = pygame.image.load("assets/button.png")
settings_warning = pygame.image.load('assets/camera_warning.png')

white = (255,255,255)
highlight_color = (104, 46, 5)
menu = True
menu_font = pygame.font.Font("assets/GROBOLD.ttf", 20)
small_menu_font = pygame.font.Font("assets/GROBOLD.ttf", 15)
start_game_text = menu_font.render("Start game", True, white)
settings_text = menu_font.render("Settings", True, white)
quit_text = menu_font.render("Quit", True, white)

#menu settings
menu_settings = pygame.image.load("assets/settings.png")
settings = False
accept_button = pygame.image.load("assets/small_button.png")
accept_text = menu_font.render("Accept", True, white)
return_button = pygame.image.load("assets/return.png")
back_text = small_menu_font.render("Back", True, white)
current_ip = ""

textinput_font = pygame.font.Font("assets/GROBOLD.ttf", 22)

while True:
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button.get_rect(topleft=(780, 220)).collidepoint(x, y):
                    print("start game")
                    if camera:
                        menu = False
                    else:
                        screen.blit(settings_warning, (0, 0))
                        pygame.display.flip()
                        pygame.display.update()
                        time.sleep(2)
                elif button.get_rect(topleft=(780, 350)).collidepoint(x, y):
                    print("settings")
                    textinput = pygame_textinput.TextInput(initial_string=current_ip, font_family="assets/GROBOLD.ttf",
                                                           font_size=22, text_color=(255, 255, 255), max_string_length=20)
                    settings = True
                    while settings:
                        events = pygame.event.get()
                        textinput.update(events)
                        for event in events:
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                x, y = event.pos
                                print(x, y)
                                if accept_button.get_rect(topleft=(880, 500)).collidepoint(x, y):
                                    pattern = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{2,5}$")
                                    if pattern.match(textinput.get_text()):
                                        textinput.set_text_color((0, 255, 0))
                                        current_ip = textinput.get_text()
                                        url = 'http://' + current_ip + '/shot.jpg'
                                        camera = True
                                    else:
                                        textinput.set_text_color((255, 0, 0))
                                    print(textinput.get_text())
                                elif return_button.get_rect(topleft=(1120, 550)).collidepoint(x, y):
                                    settings = False

                        x, y = pygame.mouse.get_pos()
                        if accept_button.get_rect(topleft=(880, 500)).collidepoint(x, y):
                            accept_text = menu_font.render("Accept", True, highlight_color)
                        elif return_button.get_rect(topleft=(1120, 550)).collidepoint(x, y):
                            back_text = small_menu_font.render("Back", True, highlight_color)
                        else:
                            accept_text = menu_font.render("Accept", True, white)
                            back_text = small_menu_font.render("Back", True, white)

                        input_text_size = textinput_font.size(textinput.get_text())

                        screen.blit(menu_settings, (0, 0))
                        screen.blit(textinput.get_surface(), (927 - int(input_text_size[0] / 2), 410))
                        screen.blit(accept_button, (880, 500))
                        screen.blit(accept_text, (900, 520))
                        screen.blit(return_button, (1120, 550))
                        screen.blit(back_text, (1150, 558))
                        pygame.display.flip()

                elif button.get_rect(topleft=(780, 480)).collidepoint(x, y):
                        print("exit")
                        pygame.quit()
                        quit()

        x, y = pygame.mouse.get_pos()
        if button.get_rect(topleft=(780, 220)).collidepoint(x, y):
            start_game_text = menu_font.render("Start game", True, highlight_color)
        elif button.get_rect(topleft=(780, 350)).collidepoint(x, y):
            settings_text = menu_font.render("Settings", True, highlight_color)
        elif button.get_rect(topleft=(780, 480)).collidepoint(x, y):
            quit_text = menu_font.render("Quit", True, highlight_color)
        else:
            start_game_text = menu_font.render("Start game", True, white)
            settings_text = menu_font.render("Settings", True, white)
            quit_text = menu_font.render("Quit", True, white)

        screen.blit(menu_image, (0, 0))
        screen.blit(button, (780, 220))
        screen.blit(settings_button, (780, 350))
        screen.blit(exit_button, (780, 480))

        screen.blit(start_game_text, (870, 260))
        screen.blit(settings_text, (883, 390))
        screen.blit(quit_text, (900, 520))

        pygame.display.flip()
        clock.tick(60)
        pygame.display.update()

    #telefon
    imgResp = urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, 1)

    #laptop
    #ret, img = cap.read()

    dst, crop_rect = board.find_edges_and_perspective_transform(img)

    checkers_list_before = board.find_checkers(dst)
    if len(checkers_list_after) == 0:
        checkers_list_after = board.find_checkers(dst)

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
                    winner = virtual_board.gameover_check(checkers_list_correct)
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu = True
        elif event.type == pygame.QUIT:
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

    winner = virtual_board.gameover_check(checkers_list_correct)

    if winner == 'red_win' or winner == 'white_win':
        if winner == 'red_win':
            winner_image = pygame.image.load('assets/red_win_1.png')
        elif winner == 'white_win':
            winner_image = pygame.image.load('assets/white_win_1.png')
        return_button_win = pygame.image.load('assets/return_1.png')
        screen.blit(winner_image, (0, 0))
        screen.blit(return_button_win, (450, 450))
        pygame.display.flip()
        pygame.display.update()

        win = True
        while win:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu = True
                        win = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    print(x, y)
                    if return_button_win.get_rect(topleft=(450, 450)).collidepoint(x, y):
                        menu = True
                        win = False
                        checkers_list_before = []
                        checkers_list_after = []
                        checkers_list_correct = []
                        checkers_list = []
                        before_count = 0
                        after_count = 0

    #clock.tick(60)

    if ord('q') == cv2.waitKey(10):
        exit(0)
