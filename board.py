import numpy as np
import cv2

l_green = np.array([50, 60, 60])
u_green = np.array([80, 255, 255])

def find_edges(hsv_image):
    mask = cv2.inRange(hsv_image, l_green, u_green)

    kernel_er = np.ones((6, 6), np.uint8)
    kernel_dil = np.ones((30, 30), np.uint8)
    erosion = cv2.erode(mask, kernel_er, iterations=1)
    dilation = cv2.dilate(erosion, kernel_dil, iterations=1)

    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img =  cv2.drawContours(hsv_image, contours, -1, (128, 255, 187), 3)

    return  img

