import operator

import numpy as np
import cv2

#Przedziały kolorów dla przestrzeni HSV
l_green = np.array([50, 60, 60])
u_green = np.array([80, 255, 255])

l_red = np.array([169, 100, 100])
u_red = np.array([189, 255, 255])

l_white = np.array([0, 0, 150])
u_white = np.array([180, 50, 255])

l_yellow = np.array([22, 93, 0])
u_yellow = np.array([45, 255, 255])

l_blue = np.array([94, 80, 2])
u_blue = np.array([126, 255, 255])



def find_edges_and_perspective_transform(image):
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)
#    cv2.imshow("thresh", thresh)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
#    print(len(contours))
    cv2.drawContours(image, contours, 1, (0, 255, 0), 3)
#    cv2.imshow("test", image)
    polygon = contours[1]
#    print(polygon)
    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in
                                     polygon]), key=operator.itemgetter(1))
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in
                                 polygon]), key=operator.itemgetter(1))
    bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in
                                    polygon]), key=operator.itemgetter(1))
    top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in
                                  polygon]), key=operator.itemgetter(1))

    crop_rect = [polygon[top_left][0], polygon[top_right][0], polygon[bottom_right][0], polygon[bottom_left][0]]

    top_left, top_right, bottom_right, bottom_left = crop_rect[0], crop_rect[1], crop_rect[2], crop_rect[3]

    dst = np.array([top_left, top_right, bottom_left, bottom_right], dtype='float32')
    pts2 = np.float32([[0, 0], [600, 0], [0, 600], [600, 600]])
    m = cv2.getPerspectiveTransform(dst, pts2)
    image2 = cv2.warpPerspective(image, m, (600, 600))
#    cv2.imshow("image", image2)
    return image2, crop_rect


def find_checkers(image):
    board_fields = [None] * 64

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #Maski dla kolorów
    mask_w = cv2.inRange(hsv, l_white, u_white)
#    cv2.imshow("white", mask_w)
    mask_r = cv2.inRange(hsv, l_red, u_red)
#    cv2.imshow("red", mask_r)
    mask_y = cv2.inRange(hsv, l_yellow, u_yellow)
#    cv2.imshow("yellow", mask_y)
    mask_b = cv2.inRange(hsv, l_blue, u_blue)
#    cv2.imshow("blue", mask_b)

    median = cv2.medianBlur(image, 5)
    gray = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)

    #Znajdowanie okręgów(pionków)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=35, param2=25, minRadius=25, maxRadius=45)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            cv2.circle(image, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
            #cv2.circle(image, (circle[0], circle[1]), 2, (0, 0, 255), 3)

            #print(circle[0], circle[1], image[circle[1], circle[0]])
            #R = int(image[circle[1], circle[0]][2])
            #G = int(image[circle[1], circle[0]][1])
            #B = int(image[circle[1], circle[0]][0])
            #cv2.putText(image, 'X', (circle[0], circle[1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (B, G, R))

            #Obszar wokół środka okręgu
            x1 = circle[1] - 10
            x2 = circle[1] + 10

            y1 = circle[0] - 10
            y2 = circle[0] + 10

            #Wycinanie obszarów z masek
            area_w = mask_w[x1:x2, y1:y2]
            height_w, width_w = area_w.shape

            area_r = mask_r[x1:x2, y1:y2]
            height_r, width_r = area_r.shape

            area_y = mask_y[x1:x2, y1:y2]
            height_y, width_y = area_y.shape

            area_b = mask_b[x1:x2, y1:y2]
            height_b, width_b = area_b.shape

            # Sprawdzanie kolorów pionków
            if (cv2.countNonZero(area_w) / (height_w * width_w)) > 0.8:
                color = 'WP'
            elif (cv2.countNonZero(area_y) / (height_y * width_y)) > 0.8:
                color = 'WQ'
            elif (cv2.countNonZero(area_b) / (height_b * width_b)) > 0.8:
                color = 'RQ'
            else:
                color = 'RP'


            # Ustawienie pionków na planszy
            fields = find_fields()
            for field in fields:
                if (circle[0] > field[0][0]) and (circle[0] < field[1][0]) and (circle[1] > field[0][1]) and (
                        circle[1] < field[1][1]):
                    position = fields.index(field)
                    board_fields[position] = color
                    break

    return board_fields


def find_fields():
    #Lewy górny róg pierwszego pola
    start_x = 15.5
    start_y = 15.5

    #Kolejne pola
    next = 73.0625

    fields_pos = []

    for j in range(0, 8):
        for i in range(0, 8):
            fields_pos.append([[start_x, start_y], [start_x + next, start_y + next]])
            start_x += next
        start_x = 15.5
        start_y += next

    return fields_pos
