from urllib.request import urlopen
import board
import cv2
import numpy as np
import pygame
import sys
import virtual_board

#telefon
url = 'http://192.168.2.8:8080/shot.jpg'

#laptop
#cap = cv2.VideoCapture(0)

pygame.init()  # essential for pygame
pygame.font.init()  # for text

screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption('Checkers Game')

bg = pygame.image.load("assets/board.png").convert()
rp = pygame.image.load("assets/red_pawn.png")
wp = pygame.image.load("assets/white_pawn.png")
rq = pygame.image.load("assets/red_queen.png")
wq = pygame.image.load("assets/white_queen.png")

# necessary for capping the game at 60FPS
clock = pygame.time.Clock()

while True:
    #telefon
    imgResp = urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, 1)

    # laptop
    # ret, img = cap.read()

    dst = board.find_edges_and_perspective_transform(img)
    checkers_list = board.find_checkers(dst)
    print(checkers_list)

    dst_RGB = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    dst_RGB = np.rot90(dst_RGB)
    dst_RGB = pygame.surfarray.make_surface(dst_RGB)
    dst_RGB = pygame.transform.flip(dst_RGB, True, False)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.blit(bg, (0, 0))
    screen.blit(dst_RGB, (610, 0))

    position = 0
    checkers = virtual_board.find_fields()
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
    clock.tick(60)

    if ord('q') == cv2.waitKey(10):
        exit(0)