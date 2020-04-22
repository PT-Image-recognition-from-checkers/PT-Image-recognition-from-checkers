import numpy as np
import cv2

l_green = np.array([50, 60, 60])
u_green = np.array([80, 255, 255])


def find_edges_and_perspective_transform(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, l_green, u_green)

    kernel_er = np.ones((6, 6), np.uint8)
    kernel_dil = np.ones((30, 30), np.uint8)
    erosion = cv2.erode(mask, kernel_er, iterations=1)
    dilation = cv2.dilate(erosion, kernel_dil, iterations=1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(hsv, contours, -1, (128, 255, 187), 3)

    list_of_edges_points = []

    for i in contours:
        cnt = i
        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        hsv = cv2.line(hsv, (cx, cy), (cx, cy), (128, 255, 187), 5)
        list_of_edges_points.append([cx, cy])

    if (len(list_of_edges_points) == 4):
        pts1 = np.float32(list_of_edges_points)
        pts2 = np.float32([[0, 0], [600, 0], [0, 600], [600, 600]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(image, M, (600, 600))

        return dst
    else:
        return image


def find_checkers(image):
    median = cv2.medianBlur(image, 5)
    gray = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=35, param2=25, minRadius=25, maxRadius=45)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
